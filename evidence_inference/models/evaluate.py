import os
import random
import logging
import itertools
import numpy as np
import torch
import torch.nn as nn
from collections import defaultdict
from typing import List, Tuple, Callable, Dict, Set
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score

from evidence_inference.models.data import Annotation, DecodeInstance
from evidence_inference.models.train import make_preds_epoch

logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
logger = logging.getLogger(__name__)

def locate_known_evidence_snippets(data: List[Annotation]) -> Dict[str, Dict[int, Set[str]]]:
    ret = defaultdict(lambda: defaultdict(set)) # docid -> {(prompt_id, sentence_idx)}
    for ann in data:
        for s, sent in enumerate(ann.doc.sentences):
            if sent.labels is not None and sent.labels.get('evidence', 0) == 1:
                ret[ann.doc.docid][s].add(ann.prompt_id)
    out = dict()
    for k,v in ret.items():
        out[k] = dict()
        for k2, v2 in v.items():
            out[k][k2] = v2
    return out

def oracle_decoding_instances(data: List[Annotation]) -> List[DecodeInstance]:
    # TODO this should shift from being "all" by default to being something configurable.
    oracle_instances = [] # entire oracle spans
    for ann in data:
        # note that the oracle here isn't masked!
        for ev_id, ev_text in enumerate(ann.evidence_texts):
            oracle_instances.append(DecodeInstance(docid=ann.doc.docid,
                                                   prompt_id=ann.prompt_id,
                                                   idx=-1 * ev_id,
                                                   sentence=ev_text,
                                                   ico=(torch.IntTensor(ann.i), torch.IntTensor(ann.c), torch.IntTensor(ann.o)),
                                                   identifier_class=1,
                                                   classification_class=ann.significance_class))
    return oracle_instances

def decoding_instances(data: List[Annotation], identifier_transform, classifier_transform) -> List[DecodeInstance]:
    instances = []
    for ann in data:
        id_data = identifier_transform(ann)
        class_data = classifier_transform(ann)
        for s, ((id_tokens, id_ico, id_kls), (cls_tokens, cls_ico, cls_kls)) in enumerate(zip(id_data, class_data)):
            assert torch.all(id_tokens == cls_tokens)
            assert all(torch.all(x == y) for (x,y) in zip(id_ico, cls_ico))
            instances.append(DecodeInstance(docid=ann.doc.docid,
                                            prompt_id=ann.prompt_id,
                                            idx=s,
                                            sentence=id_tokens,
                                            ico=id_ico,
                                            identifier_class=id_kls,
                                            classification_class=cls_kls))
    return instances

def e2e_score(tru, pred, name, evidence_classes):
    acc = accuracy_score(tru, pred)
    f1 = classification_report(tru, pred, output_dict=False, digits=4, target_names=evidence_classes)
    conf_matrix = confusion_matrix(tru, pred, normalize='true')
    logging.info(f'{name} classification accuracy {acc},\nf1:\n{f1}\nconfusion matrix:\n{conf_matrix}\n')

def decode(evidence_identifier: nn.Module,
           evidence_classifier: nn.Module,
           unconditioned_evidence_identifier: nn.Module,
           save_dir: str,
           data_name: str,
           data: List[Annotation],
           model_pars: dict,
           sep_token_id: int,
           identifier_transform: Callable[[Annotation], List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]],
           classifier_transform: Callable[[Annotation], List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]],
           detokenizer=None,
           conditioned: bool=True):
    bad_ids = set(['2206488'])
    data = list(filter(lambda x: x.doc.docid not in bad_ids, data))
    # TODO consider saving the input data as well!
    save_dir = os.path.join(save_dir, 'decode', data_name)
    os.makedirs(save_dir, exist_ok=True)
    instances_save_file = os.path.join(save_dir, f'{data_name}_instances_output.pkl')
    identifier_save_file = os.path.join(save_dir, f'{data_name}_identifier_output.pkl')
    classifier_save_file = os.path.join(save_dir, f'{data_name}_classifier_output.pkl')
    oracle_classifier_save_file = os.path.join(save_dir, f'{data_name}_oracle_classifier_output.pkl')
    unconditioned_identifier_file = os.path.join(save_dir, f'{data_name}_unconditioned_identifier_output.pkl')
    logging.info(f'Decoding {len(data)} documents from {data_name}')
    batch_size = model_pars['evidence_identifier']['batch_size']
    evidence_classes = model_pars['evidence_classifier']['classes']
    criterion = nn.CrossEntropyLoss(reduction='none')
    
    with torch.no_grad():
        if os.path.exists(instances_save_file):
            logging.info(f'Loading instances from {instances_save_file}')
            instances, oracle_instances = torch.load(instances_save_file)
        else:
            logging.info(f'Generating and saving instances to {instances_save_file}')
            oracle_instances = oracle_decoding_instances(data)
            instances = decoding_instances(data, identifier_transform, classifier_transform)
            torch.save((instances, oracle_instances), instances_save_file)
        logging.info(f'Have {len(instances)} instances in our data')
        evidence_identifier.eval()
        evidence_classifier.eval()
        #import ipdb; ipdb.set_trace()
        if os.path.exists(identifier_save_file):
            logging.info(f'Loading evidence identification predictions on {data_name} from {identifier_save_file}')
            id_loss, id_soft_pred, id_hard_pred, id_truth = torch.load(identifier_save_file)
        else:
            logging.info(f'Making evidence identification predictions on {data_name} and saving to {identifier_save_file}')
            decode_target = 'identifier' if conditioned else 'unconditioned_identifier'
            id_loss, id_soft_pred, id_hard_pred, id_truth = make_preds_epoch(evidence_identifier,
                                                                             [instance.to_model_input(decode_target) for instance in instances],
                                                                             sep_token_id,
                                                                             batch_size,
                                                                             device=next(evidence_identifier.parameters()).device,
                                                                             criterion=criterion)
            torch.save((id_loss, id_soft_pred, id_hard_pred, id_truth), identifier_save_file)

        if os.path.exists(classifier_save_file):
            logging.info(f'Loading evidence classification predictions on {data_name} from {classifier_save_file}')
            cls_loss, cls_soft_pred, cls_hard_pred, cls_truth = torch.load(classifier_save_file)
        else:
            logging.info(f'Making evidence classification predictions on {data_name} and saving to {classifier_save_file}')
            decode_target = 'classifier' if conditioned else 'unconditioned_classifier'
            cls_loss, cls_soft_pred, cls_hard_pred, cls_truth = make_preds_epoch(evidence_classifier, 
                                                                                 [instance.to_model_input(decode_target) for instance in instances],
                                                                                 sep_token_id,
                                                                                 batch_size,
                                                                                 device=next(evidence_classifier.parameters()).device,
                                                                                 criterion=criterion)
            torch.save((cls_loss, cls_soft_pred, cls_hard_pred, cls_truth), classifier_save_file)

        if os.path.exists(unconditioned_identifier_file) and unconditioned_evidence_identifier is not None:
            logging.info('Loading unconditioned evidence identification data')
            docid_to_evidence_snippets, unid_soft_pred, unid_hard_pred = torch.load(unconditioned_identifier_file)
        elif unconditioned_evidence_identifier is not None:
            logging.info('Computing unconditioned evidence identification data')
            docid_to_evidence_snippets = locate_known_evidence_snippets(data)
            _, unid_soft_pred, unid_hard_pred, _ = make_preds_epoch(unconditioned_evidence_identifier,
                                                                    [instance.to_model_input('unconditioned_identifier') for instance in instances],
                                                                    sep_token_id,
                                                                    batch_size,
                                                                    device=next(unconditioned_evidence_identifier.parameters()).device,
                                                                    criterion=None)
            torch.save([docid_to_evidence_snippets, unid_soft_pred, unid_hard_pred], unconditioned_identifier_file)
        else:
            docid_to_evidence_snippets = locate_known_evidence_snippets(data)
            unid_soft_pred, unid_hard_pred = None, None

        logging.info('Aggregating information for scoring')
        # not all annotations have evidence due to lossy offset recovery
        annotations_with_evidence = set()
        annotations_without_evidence = set()
        # (prompt, docid) -> (id_truth) for best evidence sentence
        top1_pipeline_id_truth = dict()
        top1_pipeline_unid_truth = dict()
        # (prompt, docid) -> cls prediction for best evidence sentence
        top1_pipeline_cls_prediction = dict()
        # (prompt, docid) -> cls prediction for *every* evidence sentence
        oracle_pipeline_predictions = defaultdict(list)
        # (prompt, docid) -> [soft predictions]
        all_id_predictions = dict()  # list of p(sent=1|ico)
        all_id_truths = dict()
        all_cls_predictions = dict()  # list of p(sig-|ico), p(no sig|ico), p(sig+|ico)
        all_unconditional_id_predictions = dict()  # list of p(sent=1)

        # (prompt, docid) -> (truth, prediction)
        correct_evidence_predictions = dict() # when we get a correct evidence, what does our classification look like?
        incorrect_evidence_predictions = dict() # when we get an incorrect evidence, what does our classification look like?
        no_evidence_predictions = dict() # when we can't know if we get an evidence, what does our classification look like?
        counterfactual_incorrect_evidence_predictions = dict() # when we made an incorrect evidence classification, what does the classification over a correct evidence look like?
        unconditioned_cls = dict() 

        # TODO how many of the identification mistakes are plausible?

        total_length = 0
        #import ipdb; ipdb.set_trace()
        for ann in data:
            doc_length = len(ann.tokenized_sentences)
            key = (ann.prompt_id, ann.doc.docid)
            id_predictions = id_soft_pred[total_length:total_length + doc_length]
            hard_id_predictions = id_hard_pred[total_length:total_length + doc_length]
            #unid_hard_predictions = unid_hard_pred[total_legnth:total_length + len(ann.tokenized_sentences)]
            id_truths = id_truth[total_length:total_length + doc_length]
            has_ev = sum(id_truths) > 0
            if has_ev:
                annotations_with_evidence.add(key)
            else:
                annotations_without_evidence.add(key)
            cls_predictions = cls_hard_pred[total_length:total_length + doc_length]

            best_id_sent_idx = np.argmax([id_pred[1] for id_pred in id_predictions])
            id_tru = id_truth[total_length + best_id_sent_idx]
            cls_tru = cls_truth[total_length + best_id_sent_idx]
            cls_pre = cls_hard_pred[total_length + best_id_sent_idx]

            top1_pipeline_id_truth[key] = id_tru
            top1_pipeline_cls_prediction[key] = (cls_tru, cls_pre)
            if id_tru == 1:
                correct_evidence_predictions[key] = (cls_tru, cls_pre)
            elif has_ev:
                incorrect_evidence_predictions[key] = (cls_tru, cls_pre)
            else:
                no_evidence_predictions[key] = (cls_tru, cls_pre)

            assert len(id_truths) == len(hard_id_predictions)
            for (id_sent_truth, cls_pred) in zip(id_truths, cls_predictions):
                if id_sent_truth == 1:
                    oracle_pipeline_predictions[key].append((ann.significance_class, cls_pred))

            all_id_predictions[key] = [id_pred[1] for id_pred in id_predictions]
            all_id_truths[key] = id_truths
            all_cls_predictions[key] = cls_predictions

            if unid_soft_pred:
                unid_soft_predictions = unid_soft_pred[total_length:total_length + doc_length]
                all_unconditional_id_predictions[key] = [id_pred[1] for id_pred in unid_soft_predictions]
                best_unid_sent_idx = np.argmax(all_unconditional_id_predictions[key])
                top1_pipeline_unid_truth[key] = id_truth[total_length + best_unid_sent_idx]
                unconditioned_cls[key] = (cls_truth[total_length + best_unid_sent_idx], np.argmax(cls_predictions[best_unid_sent_idx]))
            total_length += len(ann.tokenized_sentences)

        assert total_length == len(cls_hard_pred)
        assert total_length == len(id_hard_pred)
        logging.info(f'Of {len(data)} annotations, {len(annotations_with_evidence)} have evidence spans, {len(annotations_without_evidence)} do not')
        
        def id_scores(id_tru, id_soft_preds, top1_values, top1_cls_preds=None, preds_dict=None, preds_truth=None):
            # auc for id prediction
            id_auc = roc_auc_score(id_tru, id_soft_preds)
            # accuracy for top 1 per document
            id_top1_acc = accuracy_score([1] * len(top1_values), list(top1_values))
            # accuracy for all documents/sengences
            id_all_acc = accuracy_score(id_tru, [round(x) for x in id_soft_preds]) # TODO this should just be passed in instead of rounding...
            if preds_dict is not None:
                assert preds_truth is not None
                mrr = 0
                query_count = 0
                for k in preds_truth.keys():
                    pt = zip(preds_dict[k], preds_truth[k])
                    pt = sorted(pt, key=lambda x: x[0], reverse=True)
                    for pos, (_, t) in enumerate(pt):
                        if t == 1:
                            mrr += 1 / (1 + pos)
                            query_count += 1
                            break
                mrr = mrr / query_count
            else:
                mrr = None
            logging.info(f'identification auc {id_auc}, top1 acc: {id_top1_acc}, everything acc: {id_all_acc}, mrr: {mrr}')

            if top1_cls_preds is not None:
                assert preds_dict is not None
                mistakes = defaultdict(lambda: defaultdict(lambda: 0))
                for eyeD, (cls_tru, _) in top1_cls_preds.items():
                    pt = zip(preds_dict[eyeD], preds_truth[eyeD])
                    pt = sorted(pt, key=lambda x: x[0], reverse=True)
                    if pt[0][1] == 1:
                        mistakes[cls_tru]['tp'] += 1
                    else:
                        mistakes[cls_tru]['fp'] += 1
                mistakes_str = []
                for tru, preds in mistakes.items():
                    tp, fp = preds['tp'], preds['fp']
                    frac = tp / (tp + fp)
                    mistakes_str.append(f'cls {tru} evid accuracy {frac}')
                mistakes_str = '  '.join(mistakes_str)
                logging.info(f'Evidence ID accuracy breakdown by classification types {mistakes_str}')
        
        ev_only_id_soft_pred = list(itertools.chain.from_iterable(all_id_predictions[x] for x in annotations_with_evidence))
        ev_only_id_truth = list(itertools.chain.from_iterable(all_id_truths[x] for x in annotations_with_evidence))
        id_scores(ev_only_id_truth, ev_only_id_soft_pred, [top1_pipeline_id_truth[x] for x in annotations_with_evidence], top1_cls_preds=top1_pipeline_cls_prediction, preds_dict=all_id_predictions, preds_truth=all_id_truths)
        #id_scores(id_truth, id_soft_pred, top1_pipeline_id_truth.values())

        # pipeline score
        pipeline_truth, pipeline_pred = zip(*top1_pipeline_cls_prediction.values())
        e2e_score(pipeline_truth, pipeline_pred, 'Pipeline', evidence_classes)

        # oracle classification F1 for cls, picking *just one* evidence
        oracle_truth, oracle_pred = zip(*[random.choice(x) for x in oracle_pipeline_predictions.values()])
        e2e_score(oracle_truth, oracle_pred, 'Oracle (one)', evidence_classes)

        # oracle classification F1 for cls, picking *all* evidence
        oracle_all_truth, oracle_all_pred = zip(*itertools.chain.from_iterable(oracle_pipeline_predictions.values()))
        e2e_score(oracle_all_truth, oracle_all_pred, 'Oracle (all)', evidence_classes)

        # for just the correctly predicted evidence spans, how does our final classification perform?
        # how hard is it when it's "easy" to find the evidence?
        correct_ev_truths, correct_ev_preds = zip(*correct_evidence_predictions.values())
        e2e_score(correct_ev_truths, correct_ev_preds, 'Correct evidence only', evidence_classes)

        # how well does our classifier do when we find an incorrect evidence?
        # for just the incorrectly predicted evidence spans, how does our final classification perform?
        # do we pick up on in document correlations? something else?
        # TODO: check if this is an evidence statement for a different ICO
        # TODO: check if this is an undiscovered evidence statement 
        # TODO: check how far down we need to go to find a known evidence statement for this ICO vs. some other ICO
        incorrect_ev_truths, incorrect_ev_preds = zip(*incorrect_evidence_predictions.values())
        e2e_score(incorrect_ev_truths, incorrect_ev_preds, 'Incorrect evidence only', evidence_classes)

        # for the incorrectly predicgted evidence spans, how would we have done if we used a correct span?
        # how hard is the classification when finding the evidence is hard?
        counterfactual_ev_truths, counterfactual_ev_preds = zip(*[random.choice(oracle_pipeline_predictions[key]) for key in set(incorrect_evidence_predictions.keys())])
        #counterfactual_ev_truths, counterfactual_ev_preds = zip(*[random.choice(oracle_pipeline_predictions[key]) for key in set(incorrect_evidence_predictions.keys()) & set(oracle_pipeline_predictions.keys())])
        e2e_score(counterfactual_ev_truths, counterfactual_ev_preds, 'Counterfactual evidence only', evidence_classes)

        # take the correct + the fixed ones
        # this should be similar to the Oracle score
        augmented_counterfactual_ev_truths = counterfactual_ev_truths + correct_ev_truths
        augmented_counterfactual_ev_preds = counterfactual_ev_preds + correct_ev_preds
        e2e_score(augmented_counterfactual_ev_truths, augmented_counterfactual_ev_preds, 'Augmented counterfactual evidence only', evidence_classes)

        # what happens if we use an unconditioned identifier
        if unconditioned_evidence_identifier is not None:
            logging.info('Unconditional identifier scores (note the classifier is conditional)')
            ev_only_unid_soft_pred = list(itertools.chain.from_iterable(all_unconditional_id_predictions[x] for x in annotations_with_evidence))
            id_scores(ev_only_id_truth, ev_only_unid_soft_pred, [top1_pipeline_unid_truth[x] for x in annotations_with_evidence], top1_cls_preds=top1_pipeline_cls_prediction, preds_dict=all_unconditional_id_predictions, preds_truth=all_id_truths)
            unid_cls_truth, unid_cls_pred = zip(*unconditioned_cls.values())
            e2e_score(unid_cls_truth, unid_cls_pred, "Unconditioned identifier (how important is the ICO to finding the evidence)", evidence_classes)
            # TODO how well does our conditioned evidence identifier recover *any* evidence (as determined by the unconditioned evidence identifier & all the data)

        def detok(sent):
            return ' '.join(detokenizer[x.item() if isinstance(x, torch.Tensor) else x] for x in sent)
        def view(id_predictions, unid_soft_predictions, id_truths, cls_predictions, cls_truths, ann, best, p=False):
            out = []
            out.append(f'ico: {detok(ann.i)} vs. {detok(ann.c)} for {detok(ann.o)}')
            if unid_soft_predictions is None:
                unid_soft_predictions = [torch.tensor([0.0, 0.0]) for _ in id_predictions]
            for idx, (idp, uidp, idt, clsp, clst, sent) in enumerate(zip(id_predictions, unid_soft_predictions, id_truths, cls_predictions, cls_truths, ann.tokenized_sentences)):
                best_marker = '*' if idx == best else ''
                out.append(detok(sent))
                out.append(f'  id pred{best_marker}: {idp[1].item():.3f}, unid id pred: {uidp[1].item():.3f}, id_truth: {idt}')
                out.append(f'  cls pred: {clsp}, cls truth: {clst}')
            if p:
                print('\n'.join(out))
            return '\n'.join(out)

        #import ipdb; ipdb.set_trace()
        total_length = 0
        debug_dir = os.path.join(save_dir, 'debug')
        incorrect_debug_dir = os.path.join(save_dir, 'debug_incorrect')
        os.makedirs(debug_dir, exist_ok=True)
        os.makedirs(incorrect_debug_dir, exist_ok=True)
        for ann in data:
            key = (ann.prompt_id, ann.doc.docid)
            id_predictions = id_soft_pred[total_length:total_length + len(ann.tokenized_sentences)]
            hard_id_predictions = id_hard_pred[total_length:total_length + len(ann.tokenized_sentences)]
            #unid_hard_predictions = unid_hard_pred[total_legnth:total_length + len(ann.tokenized_sentences)]
            if unid_soft_pred is not None:
                unid_soft_predictions = unid_soft_pred[total_length:total_length + len(ann.tokenized_sentences)]
            else:
                unid_soft_predictions = None
            id_truths = id_truth[total_length:total_length + len(ann.tokenized_sentences)]
            cls_predictions = cls_hard_pred[total_length:total_length + len(ann.tokenized_sentences)]

            best_id_sent_idx = np.argmax([id_pred[1] for id_pred in id_predictions])
            id_tru = id_truth[total_length + best_id_sent_idx]
            cls_tru = cls_truth[total_length + best_id_sent_idx]
            cls_trus = cls_truth[total_length:total_length + len(ann.tokenized_sentences)]
            cls_pre = cls_hard_pred[total_length + best_id_sent_idx]

            pretty = view(id_predictions, unid_soft_predictions, id_truths, cls_predictions, cls_trus, ann, best_id_sent_idx, p=False)
            with open(os.path.join(debug_dir, str(ann.doc.docid) + '_' + str(ann.prompt_id) + '.txt'), 'w') as of:
                of.write(pretty)
            if id_tru == 0:
                with open(os.path.join(incorrect_debug_dir, str(ann.doc.docid) + '_' + str(ann.prompt_id) + '.txt'), 'w') as of:
                    of.write(pretty)
            total_length += len(ann.tokenized_sentences)
