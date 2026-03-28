import os
import random
import logging
import itertools
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import Counter, OrderedDict
from typing import List, Tuple, Callable
from sklearn.metrics import accuracy_score, classification_report

from evidence_inference.models.data import Annotation

logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
logger = logging.getLogger(__name__)

def make_preds_batch(classifier: nn.Module,
                     batch_elements: List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]],
                     sep_token_id: int,
                     device: str=None,
                     criterion: nn.Module=None) -> Tuple[float, List[float], List[int], List[int]]:
    """Batch predictions

    Args:
        classifier: a module that looks like an AttentiveClassifier
        batch_elements: a list of elements to make predictions over. These must be SentenceEvidence objects.
        device: Optional; what compute device this should run on
        criterion: Optional; a loss function
    """
    # delete any "None" padding, if any (imposed by the use of the "grouper")
    sentences, icos, targets = zip(*filter(lambda x: x, batch_elements))
    targets = torch.tensor(targets, dtype=torch.long)
    sep = torch.tensor([sep_token_id], dtype=torch.int)
    queries = [torch.cat([i, sep, c, sep, o]).to(dtype=torch.long) for (i,c,o) in icos]
    sentences = [torch.tensor(s, dtype=torch.long) for s in sentences]
    preds = classifier(queries, sentences)
    targets = targets.to(device=preds.device)
    if criterion:
        loss = criterion(preds, targets)
    else:
        loss = None
    preds = F.softmax(preds).cpu()
    hard_preds = torch.argmax(preds, dim=-1).cpu()
    return loss, preds, hard_preds, targets.cpu()

def make_preds_epoch(classifier: nn.Module,
                     data: List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]],
                     sep_token_id: int,
                     batch_size: int,
                     device: str=None,
                     criterion: nn.Module=None):
    """Predictions for more than one batch.

    Args:
        classifier: a module that looks like an AttentiveClassifier
        data: a list of elements to make predictions over. These must be SentenceEvidence objects.
        batch_size: the biggest chunk we can fit in one batch.
        device: Optional; what compute device this should run on
        criterion: Optional; a loss function
    """
    assert len(data) > 0
    epoch_loss = 0
    epoch_soft_pred = []
    epoch_hard_pred = []
    epoch_truth = []
    batches = _grouper(data, batch_size)
    classifier.eval()
    for batch in batches:
        with torch.no_grad():
            loss, soft_preds, hard_preds, targets = make_preds_batch(classifier, batch, sep_token_id, device, criterion=criterion)
        if loss is not None:
            epoch_loss += loss.sum().item()
        else:
            epoch_loss = None
        epoch_hard_pred.extend(hard_preds)
        epoch_soft_pred.extend(soft_preds.numpy())
        epoch_truth.extend(targets.numpy())
    if epoch_loss is not None:
        epoch_loss /= len(data)
    epoch_hard_pred = [x.item() for x in epoch_hard_pred]
    epoch_truth = [x.item() for x in epoch_truth]
    return epoch_loss, epoch_soft_pred, epoch_hard_pred, epoch_truth

# copied from https://docs.python.org/3/library/itertools.html#itertools-recipes
def _grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def train_module(model: nn.Module,
                 save_dir: str,
                 model_name: str,
                 train: List[Annotation],
                 val: List[Annotation],
                 #documents: Dict[str, List[List[int]]],
                 model_pars: dict,
                 sep_token_id: int,
                 sampler: Callable[[Annotation], List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]],
                 val_sampler: Callable[[Annotation], List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]],
                 optimizer=None,
                 scheduler=None,
                 detokenizer=None) -> Tuple[nn.Module, dict]:
    """Trains a module for evidence identification or classification.
    
    Loosely based on the work done for the ERASER Benchmark: DeYoung et al., 2019

    This method tracks loss on the entire validation set, saves intermediate
    models, and supports restoring from an unfinished state. The best model on
    the validation set is maintained, and the model stops training if a patience
    (see below) number of epochs with no improvement is exceeded.

    As there are likely too many negative examples to reasonably train a
    classifier on everything, every epoch we subsample the negatives.

    Args:
        model: some model like BertClassifier
        save_dir: a place to save intermediate and final results and models.
        model_name: a string for saving information
        train: a List of interned Annotation objects.
        val: a List of interned Annotation objects.
        #documents: a Dict of interned sentences
        model_pars: Arbitrary parameters directory, assumed to contain:
            lr: learning rate
            batch_size: an int
            sampling_method: a string, plus additional params in the dict to define creation of a sampler
            epochs: the number of epochs to train for
            patience: how long to wait for an improvement before giving up.
            max_grad_norm: optional, clip gradients.
        optimizer: what pytorch optimizer to use, if none, initialize Adam
        scheduler: optional, do we want a scheduler involved in learning?
        tensorize_model_inputs: should we convert our data to tensors before passing it to the model?
                                Useful if we have a model that performs its own tokenization (e.g. BERT as a Service)

    Returns:
        the trained evidence identifier and a dictionary of intermediate results.
    """

    logging.info(f'Beginning training {model_name} with {len(train)} annotations, {len(val)} for validation')
    output_dir = os.path.join(save_dir, f'{model_name}')
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    model_save_file = os.path.join(output_dir, f'{model_name}.pt')
    epoch_save_file = os.path.join(output_dir, f'{model_name}_epoch_data.pt')

    if optimizer is None:
        optimizer = torch.optim.Adam(model.parameters(), lr = model_pars['lr'])
    criterion = nn.CrossEntropyLoss(reduction='none')
    batch_size = model_pars['batch_size']
    if 'oracle' in model_name:
        batch_size = batch_size // 2
    epochs = model_pars['epochs']
    patience = model_pars['patience']
    max_grad_norm = model_pars.get('max_grad_norm', None)

    device = next(model.parameters()).device

    # TODO output an AUC where appropriate
    results = {
        # "sampled" losses do not represent the true data distribution, but do represent training data
        'sampled_epoch_train_acc': [],
        'sampled_epoch_train_losses': [],
        'sampled_epoch_train_f1': [],
        'sampled_epoch_val_acc': [],
        'sampled_epoch_val_losses': [],
        'sampled_epoch_val_f1': [],
        # "full" losses do represent the true data distribution
        'full_epoch_val_losses': [],
        'full_epoch_val_f1': [],
        'full_epoch_val_acc': [],
    }
    # allow restoring an existing training run
    start_epoch = 0
    best_epoch = -1
    best_val_loss = float('inf')
    best_val_f1 = float('-inf')
    best_model_state_dict = None
    epoch_data = {}
    if os.path.exists(epoch_save_file):
        model.load_state_dict(torch.load(model_save_file))
        epoch_data = torch.load(epoch_save_file)
        start_epoch = epoch_data['epoch'] + 1
        # handle finishing because patience was exceeded or we didn't get the best final epoch
        if bool(epoch_data.get('done', 0)):
            start_epoch = epochs
        results = epoch_data['results']
        best_epoch = start_epoch
        best_model_state_dict = OrderedDict({k:v.cpu() for k,v in model.state_dict().items()})
        logging.info(f'Restored training from epoch {start_epoch}')
    logging.info(f'Training evidence model from epoch {start_epoch} until epoch {epochs}')
    optimizer.zero_grad()
    sep = torch.tensor(sep_token_id, dtype=torch.int).unsqueeze(0)
    #import ipdb; ipdb.set_trace()
    for epoch in range(start_epoch, epochs):
        epoch_train_data = list(itertools.chain.from_iterable(sampler(t) for t in train))
        assert len(epoch_train_data) > 0
        train_classes = Counter(x[-1] for x in epoch_train_data)
        random.shuffle(epoch_train_data)
        epoch_val_data = list(itertools.chain.from_iterable(sampler(v) for v in val))
        assert len(epoch_val_data) > 0
        val_classes = Counter(x[-1] for x in epoch_val_data)
        random.shuffle(epoch_val_data)
        sampled_epoch_train_loss = 0
        model.train()
        logging.info(f'Training with {len(epoch_train_data) // batch_size} batches with {len(epoch_train_data)} examples')
        logging.info(f'Training classes distribution: {train_classes}, valing class distribution: {val_classes}')
        hard_train_preds = []
        hard_train_truths = []
        optimizer.zero_grad()
        for batch_start in range(0, len(epoch_train_data), batch_size):
            model.train()
            batch_elements = epoch_train_data[batch_start:min(batch_start+batch_size, len(epoch_train_data))]
            # we sample every time to thereoretically get a better representation of instances over the corpus.
            # this might just take more time than doing so in advance.
            sentences, queries, targets = zip(*filter(lambda x: x, batch_elements))
            hard_train_truths.extend(targets)
            #sentences = [s.to(device=device) for s in sentences]
            queries = [torch.cat([i, sep, c, sep, o]).to(dtype=torch.long) for (i,c,o) in queries]
            preds = model(queries, sentences)
            hard_train_preds.extend([x.cpu().item() for x in torch.argmax(preds, dim=-1)])
            targets = torch.tensor(targets, dtype=torch.long, device=device)
            loss = criterion(preds, targets.to(device=preds.device)).sum()
            sampled_epoch_train_loss += loss.item()
            loss = loss / len(preds)
            loss.backward()
            if max_grad_norm:
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
            optimizer.step()
            if scheduler:
                scheduler.step()
            optimizer.zero_grad()
        sampled_epoch_train_loss /= len(epoch_train_data)
        results['sampled_epoch_train_losses'].append(sampled_epoch_train_loss)
        results['sampled_epoch_train_acc'].append(accuracy_score(hard_train_truths, hard_train_preds))
        results['sampled_epoch_train_f1'].append(classification_report(hard_train_truths, hard_train_preds, output_dict=True))
        logging.info(f'Epoch {epoch} sampled training loss {sampled_epoch_train_loss}, acc {results["sampled_epoch_train_acc"][-1]}')

        with torch.no_grad():
            model.eval()
            sampled_epoch_val_loss, _, sampled_epoch_val_hard_pred, sampled_epoch_val_truth = make_preds_epoch(model, epoch_val_data, batch_size, sep_token_id, device, criterion)
            sampled_epoch_val_acc = accuracy_score(sampled_epoch_val_truth, sampled_epoch_val_hard_pred)
            sampled_epoch_val_f1 = classification_report(sampled_epoch_val_truth, sampled_epoch_val_hard_pred, output_dict=True)
            results['sampled_epoch_val_losses'].append(sampled_epoch_val_loss)
            results['sampled_epoch_val_acc'].append(sampled_epoch_val_acc)
            results['sampled_epoch_val_f1'].append(sampled_epoch_val_f1)
            logging.info(f'Epoch {epoch} sampled val loss {sampled_epoch_val_loss}, acc {sampled_epoch_val_acc}, f1: {sampled_epoch_val_f1}')
            # evaluate over *all* of the validation data
            all_val_data = list(itertools.chain.from_iterable(val_sampler(v) for v in val))
            epoch_val_loss, epoch_val_soft_pred, epoch_val_hard_pred, epoch_val_truth = make_preds_epoch(model, all_val_data, batch_size, sep_token_id, device, criterion)
            results['full_epoch_val_losses'].append(epoch_val_loss)
            results['full_epoch_val_acc'].append(accuracy_score(epoch_val_truth, epoch_val_hard_pred))
            results['full_epoch_val_f1'].append(classification_report(epoch_val_truth, epoch_val_hard_pred, output_dict=True))
            logging.info(f'Epoch {epoch} full val loss {epoch_val_loss}, accuracy: {results["full_epoch_val_acc"][-1]}, f1: {results["full_epoch_val_f1"][-1]}')

            full_val_f1 = results['full_epoch_val_f1'][-1]['macro avg']['f1-score']
            #if epoch_val_loss < best_val_loss:
            #if sampled_epoch_val_loss < best_val_loss:
            if full_val_f1 > best_val_f1:
                logging.debug(f'Epoch {epoch} new best model with full val f1 {full_val_f1}')
                #logging.debug(f'Epoch {epoch} new best model with sampled val loss {sampled_epoch_val_loss}')
                best_model_state_dict = OrderedDict({k:v.cpu() for k,v in model.state_dict().items()})
                best_epoch = epoch
                best_val_f1 = full_val_f1
                #best_val_loss = sampled_epoch_val_loss
                torch.save(model.state_dict(), model_save_file)
                epoch_data = {
                    'epoch': epoch,
                    'results': results,
                    'best_val_loss': best_val_loss,
                    'done': 0
                }
                torch.save(epoch_data, epoch_save_file)
        if epoch - best_epoch > patience:
            epoch_data['done'] = 1
            torch.save(epoch_data, epoch_save_file)
            break

    epoch_data['done'] = 1
    epoch_data['results'] = results
    torch.save(epoch_data, epoch_save_file)
    model.load_state_dict(best_model_state_dict)
    model = model.to(device=device)
    model.eval()
    return model, results
