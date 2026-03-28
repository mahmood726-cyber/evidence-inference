import argparse
import copy
import itertools
import json
import logging
import math
import os
import random
import shutil
import sys

from collections import Counter, defaultdict, OrderedDict
from dataclasses import asdict, dataclass
from os.path import join, dirname, abspath
from typing import Callable, Dict, List, Set, Tuple, Union

import numpy as np
import transformers
import torch
import torch.nn as nn
import torch.nn.functional as F

from dacite import from_dict
from scipy import stats
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from transformers import BertTokenizer

# Requires package installation
# sys.path.insert(0, abspath(join(dirname(abspath(__file__)), '..', '..')))

from evidence_inference.preprocess import preprocessor
from evidence_inference.preprocess.preprocessor import (
    PROMPT_ID_COL_NAME,
    LABEL,
    EVIDENCE_COL_NAME,
    EVIDENCE_START,
    EVIDENCE_END,
    STUDY_ID_COL,
)
from evidence_inference.preprocess.representations import (
    Document,
    Sentence,
    Token,
    to_structured,
    retokenize_with_bert
)
from evidence_inference.models.bert_model import initialize_models
from evidence_inference.models.data import (
    Annotation, 
    DecodeInstance,
    get_identifier_sampler,
    identifier_everything_sampler,
    get_classifier_oracle_sampler,
    mask_tokens,
    get_classifier_sampler,
    classifier_everything_sampler,
    mask_sampler
)
from evidence_inference.models.train import (
    make_preds_batch,
    make_preds_epoch,
    train_module
)
from evidence_inference.models.evaluate import (
    locate_known_evidence_snippets,
    oracle_decoding_instances,
    decoding_instances,
    e2e_score,
    decode
)


logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
logger = logging.getLogger(__name__)

def load_data(save_dir: str, params: dict, tokenizer, evidence_classes: Dict[str, int]):
    data_file = os.path.join(save_dir, 'datasets.pkl')
    articles_file = os.path.join(save_dir, 'bert_articles.pkl')
    use_abstracts = bool(params.get('use_abstracts', False))
    if os.path.exists(data_file):
        logging.info(f'Resurrecting train/val/test from {data_file}')
        # this is a hack to deal with a previous version of data loading
        train, val, test = torch.load(data_file)
        if len(test) == 0:
            logging.info(f'Test was empty, using val')
            test = val
        return (train, val, test)
    ei_annotations = preprocessor.read_annotations()
    ei_prompts = preprocessor.read_prompts()
    if use_abstracts:
        ei_annotations = ei_annotations[ei_annotations['In Abstract']]
    # TODO these column names should be factored out
    logging.info('joining prompts/annotations')
    joined = ei_annotations.merge(ei_prompts, on=PROMPT_ID_COL_NAME, suffixes=('', '_y'))

    article_ids = set(joined[STUDY_ID_COL].unique())
    if os.path.exists(articles_file):
        logging.info(f'Reading {len(article_ids)} computed articles from {articles_file}')
        bert_articles = torch.load(articles_file)
    else:
        logging.info(f'Reading {len(article_ids)} articles')
        articles = preprocessor.read_in_text_articles(article_ids, abstracts=use_abstracts)
        #tokenizer = BertTokenizer.from_pretrained(params['bert_vocab'])
        logging.info(f'Converting {len(articles)} articles for BERT')
        bert_articles = dict(map(lambda x: (x.get_pmcid(), retokenize_with_bert(to_structured(x), tokenizer)), articles))
        torch.save(bert_articles, articles_file)

    train_file = params['train_data']
    val_file = params['val_data']
    test_file = params['test_data']
    train_ids = preprocessor._read_ids(train_file)
    val_ids = preprocessor._read_ids(val_file)
    test_ids = preprocessor._read_ids(test_file)
    all_ids = train_ids | val_ids | test_ids
    assert len(train_ids & test_ids) == 0
    assert len(train_ids & val_ids) == 0
    target_ids = set(train_ids | val_ids | test_ids)
    train, val, test, skipped = [], [], [], []

    logging.info('Converting prompts')
    prompt_ids = set(joined[PROMPT_ID_COL_NAME].unique())
    skipped_prompts = set()

    for prompt_id in prompt_ids:
        anns = joined[joined[PROMPT_ID_COL_NAME] == prompt_id]
        (docid,) = anns[STUDY_ID_COL].unique()
        docid = str(docid)
        if docid not in bert_articles:
            logging.warn(f'Skipping prompt {prompt_id} for missing document {docid}')
            skipped_prompts.add(prompt_id)
            continue
        (i,) = anns['Intervention'].unique()
        (c,) = anns['Comparator'].unique()
        (o,) = anns['Outcome'].unique()
        spans = anns[[EVIDENCE_START, EVIDENCE_END]]
        label = evidence_classes[stats.mode(anns[LABEL])[0][0]]
        doc = bert_articles[docid]
        sentences = list(doc.sentences)
        evidence_texts = anns[EVIDENCE_COL_NAME]
        ev_spans = []
        for (_, row) in spans.iterrows():
            start = row[EVIDENCE_START]
            end = row[EVIDENCE_END]
            ev_spans.append((start, end))
            ev_chars = set(range(start, end))
            if start == -1: # skip unrecovered evidence spans
                continue
            span = doc.sentence_span(start, end)
            if span is None:
                continue
            for si in range(*span):
                char_range = set(range(sentences[si].start_offset, sentences[si].end_offset))
                intersection = char_range & ev_chars
                # if the size of the intersction with our evidence is:
                # (1) very small AND
                # (2) it does not entirely contain the evidence
                # then we skip this sentence.
                if len(intersection) < .2 * len(char_range) and len(intersection) < .9 * len(ev_chars):
                    continue
                sent = asdict(sentences[si])
                sent['labels'] = sent['labels'] if sent['labels'] else dict()
                sent['labels']['evidence'] = 1
                tokens = sent['tokens']
                for t in tokens:
                    if t.get('labels', None) is None:
                        t['labels'] = dict()
                    if len(set(range(t['start_offset'], t['end_offset'])) & ev_chars) > 0:
                        t['labels']['evidence'] = 1
                    elif 'evidence' not in t:
                        t['labels']['evidence'] = 0
                sent['tokens'] = tuple(tokens)
                sentences[si] = from_dict(data_class=Sentence, data=sent)
        doc_parts = asdict(doc)
        doc_parts['sentences'] = tuple(sentences)
        doc = from_dict(data_class=Document, data=doc_parts)
        evidence_vector = torch.LongTensor([t.labels['evidence'] if t.labels is not None else 0 for t in doc.tokens()])
        ann = Annotation(doc=doc,
                         prompt_id=str(prompt_id),
                         tokenized_sentences=[torch.IntTensor([t.token_id for t in s.tokens]) for s in doc.sentences],
                         i=i,
                         c=c,
                         o=o,
                         evidence_texts=tuple(set(evidence_texts.values)),
                         evidence_spans=tuple(set(ev_spans)),
                         evidence_vector=evidence_vector,
                         significance_class=label).retokenize(tokenizer)

        docid = int(docid)
        if docid in train_ids:
            train.append(ann)
        if docid in val_ids:
            val.append(ann)
        if docid in test_ids:
            test.append(ann)
        if docid not in all_ids:
            skipped.append(docid)
    logging.info(f'Skipped {len(skipped_prompts)} prompts for missing documents')
    logging.info(f'Skipped converting {len(skipped)} ids')
    logging.info(f'Have {len(train)} training instances, {len(val)} validation instances, {len(test)} test instances')
    torch.save([train, val, test], data_file)
    #import ipdb; ipdb.set_trace()
    return train, val, test

def main():
    parser = argparse.ArgumentParser(description="""Trains a pipeline model.

    Loosely based on the pipeline in the ERASER Benchmark, DeYoung et al., 2019
    Step 1 is evidence identification, that is identify if a given sentence is evidence or not
    Step 2 is evidence classification, that is given an evidence sentence, classify the final outcome for the final task (e.g. sentiment or significance).

    These models should be separated into two separate steps, but at the moment:
    * prep data 
    * convert data for evidence identification - in the case of training data we take all the positives and sample some negatives
        * side note: this sampling is *somewhat* configurable and is done on a per-batch/epoch basis in order to gain a broader sampling of negative values.
    * train evidence identification
    * convert data for evidence classification - take all rationales + decisions and use this as input
    * train evidence classification
    * decode first the evidence, then run classification for each split
    
    """, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--output_dir', dest='output_dir', required=True, help='Where shall we write intermediate models + final data to?')
    parser.add_argument('--params', dest='params', required=True, help='JSoN file for loading arbitrary model parameters (e.g. optimizers, pre-saved files, etc.')
    parser.add_argument('--data_only', dest='data_only', required=False, action='store_true', help='Process data only, no training')
    args = parser.parse_args()
    with open(args.params, 'r') as fp:
        logger.info(f'Loading model parameters from {args.params}')
        params = json.load(fp)
        logger.info(f'Params: {json.dumps(params, indent=2, sort_keys=True)}')
    evidence_identifier, evidence_classifier, word_interner, de_interner, evidence_classes, tokenizer = initialize_models(params, '[UNK]')
    oracle_evidence_classifier = copy.deepcopy(evidence_classifier)
    ico_only_evidence_classifier = copy.deepcopy(evidence_classifier)
    unconditioned_oracle_evidence_classifier = copy.deepcopy(evidence_classifier)
    unconditioned_evidence_identifier = copy.deepcopy(evidence_identifier)
    unconditioned_evidence_classifier = copy.deepcopy(evidence_classifier)
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)
        shutil.copyfile(args.params, os.path.join(args.output_dir, os.path.basename(args.params)))
    train, val, test = load_data(args.output_dir, params, tokenizer, evidence_classes)
    assert len(test) > 0
    #train = train[:10]
    #val = train
    #test = train
    logging.info(f'Loaded {len(train)} training instances, {len(val)} valing instances, and {len(test)} testing instances')
    if args.data_only:
        sys.exit(0)
    evidence_classifier, evidence_classifier_training_results = train_module(evidence_classifier.cuda(),
                                                                             args.output_dir,
                                                                             "evidence_classifier",
                                                                             train,
                                                                             val,
                                                                             params['evidence_classifier'],
                                                                             tokenizer.sep_token_id,
                                                                             get_classifier_sampler(params),
                                                                             get_classifier_oracle_sampler(params),
                                                                             detokenizer=de_interner)
    evidence_classifier = evidence_classifier.cpu()
    evidence_identifier, evidence_identifier_training_results = train_module(evidence_identifier.cuda(),
                                                                             args.output_dir,
                                                                             "evidence_identifier",
                                                                             train,
                                                                             val,
                                                                             params['evidence_identifier'],
                                                                             tokenizer.sep_token_id,
                                                                             get_identifier_sampler(params),
                                                                             identifier_everything_sampler,
                                                                             detokenizer=de_interner)
    evidence_identifier = evidence_identifier.cpu()
    if unconditioned_evidence_identifier is not None:
        unconditioned_evidence_identifier, unconditioned_evidence_identifier_training_results = train_module(unconditioned_evidence_identifier.cuda(),
                                                                                                             args.output_dir,
                                                                                                             "unconditioned_evidence_identifier",
                                                                                                             train,
                                                                                                             val,
                                                                                                             params['evidence_identifier'],
                                                                                                             tokenizer.sep_token_id,
                                                                                                             mask_sampler(get_identifier_sampler(params), {'i', 'c', 'o'}),
                                                                                                             mask_sampler(identifier_everything_sampler, {'i', 'c', 'o'}),
                                                                                                             detokenizer=de_interner)
        unconditioned_evidence_identifier = unconditioned_evidence_identifier.cpu()
        unconditioned_evidence_classifier, unconditioned_evidence_classifier_training_results = train_module(unconditioned_evidence_classifier.cuda(),
                                                                                                             args.output_dir,
                                                                                                             "unconditioned_evidence_classifier",
                                                                                                             train,
                                                                                                             val,
                                                                                                             params['evidence_classifier'],
                                                                                                             tokenizer.sep_token_id,
                                                                                                             mask_sampler(get_classifier_sampler(params), {'i', 'c', 'o'}),
                                                                                                             mask_sampler(get_classifier_oracle_sampler(params), {'i', 'c', 'o'}),
                                                                                                             detokenizer=de_interner)
        unconditioned_evidence_classifier = unconditioned_evidence_classifier.cpu()
    for t, d in [('val', val), ('test', test)]:
        logging.info(f"\n\n\n\nConditioned scores {t}\n\n\n\n")
        decode(evidence_identifier.cuda(),
               evidence_classifier.cuda(),
               None,
               #unconditioned_evidence_identifier.cuda() if unconditioned_evidence_identifier else None,
               args.output_dir,
               t,
               d,
               params,
               tokenizer.sep_token_id,
               identifier_everything_sampler,
               classifier_everything_sampler,
               detokenizer=de_interner)
        logging.info(f"\n\n\n\nUnconditioned scores {t}\n\n\n\n")
        decode(unconditioned_evidence_identifier.cuda(),
               unconditioned_evidence_classifier.cuda(),
               None,
               args.output_dir,
               f"{t}_unconditioned",
               d,
               params,
               tokenizer.sep_token_id,
               identifier_everything_sampler,
               classifier_everything_sampler,
               detokenizer=de_interner)
    # TODO fix the data for this so we union evidence sentences across document
    #evidence_identifier = evidence_identifier.cpu()
    #evidence_classifier = evidence_classifier.cpu()

    if oracle_evidence_classifier is not None:
        logging.info('Conditioned oracle evidence classifier')
        oracle_sampler = get_classifier_oracle_sampler(params)
        oracle_evidence_classifier, oracle_evidence_classifier_training_results = train_module(oracle_evidence_classifier.cuda(),
                                                                                               args.output_dir,
                                                                                               "oracle_evidence_classifier",
                                                                                               train,
                                                                                               val,
                                                                                               params['evidence_classifier'],
                                                                                               tokenizer.sep_token_id,
                                                                                               oracle_sampler,
                                                                                               oracle_sampler,
                                                                                               detokenizer=de_interner)
        for n, t in [('val', val), ('test', test)]:
            logging.info(f'Decoding on {n}')
            _, _, oracle_hard_pred, oracle_tru = make_preds_epoch(oracle_evidence_classifier.cuda(),
                                                                  [instance.to_model_input('classifier') for instance in oracle_decoding_instances(t)],
                                                                  tokenizer.sep_token_id, params['evidence_classifier']['batch_size'],
                                                                  device='cuda:0',
                                                                  criterion=None)
            e2e_score(oracle_tru, oracle_hard_pred, 'Conditioned oracle scoring', evidence_classes)
        oracle_evidence_classifier = oracle_evidence_classifier.cpu()
    if unconditioned_oracle_evidence_classifier is not None:
        logging.info('Unconditioned oracle evidence classifier')
        oracle_sampler = get_classifier_oracle_sampler(params)
        unconditioned_oracle_evidence_classifier, unconditioned_oracle_evidence_classifier_training_results = train_module(unconditioned_oracle_evidence_classifier.cuda(),
                                                                                                                           args.output_dir,
                                                                                                                           "unconditioned_oracle_evidence_classifier",
                                                                                                                           train,
                                                                                                                           val,
                                                                                                                           params['evidence_classifier'],
                                                                                                                           tokenizer.sep_token_id,
                                                                                                                           mask_sampler(oracle_sampler, {'i', 'c', 'o'}),
                                                                                                                           mask_sampler(oracle_sampler, {'i', 'c', 'o'}),
                                                                                                                           detokenizer=de_interner)
        for n, t in [('val', val), ('test', test)]:
            logging.info(f'Decoding on {n}')
            _, _, oracle_hard_pred, oracle_tru = make_preds_epoch(unconditioned_oracle_evidence_classifier.cuda(),
                                                                  [instance.to_model_input('unconditioned_classifier') for instance in oracle_decoding_instances(t)],
                                                                  tokenizer.sep_token_id, params['evidence_classifier']['batch_size'],
                                                                  device='cuda:0',
                                                                  criterion=None)
            e2e_score(oracle_tru, oracle_hard_pred, 'Unconditioned oracle scoring', evidence_classes)
        unconditioned_oracle_evidence_classifier = unconditioned_oracle_evidence_classifier.cpu()
    if ico_only_evidence_classifier is not None:
        logging.info('ICO only evidence classifier')
        oracle_sampler = get_classifier_oracle_sampler(params)
        ico_only_evidence_classifier, ico_only_evidence_classifier_training_results = train_module(ico_only_evidence_classifier.cuda(),
                                                                                                   args.output_dir,
                                                                                                   "ico_only_evidence_classifier",
                                                                                                   train,
                                                                                                   val,
                                                                                                   params['evidence_classifier'],
                                                                                                   tokenizer.sep_token_id,
                                                                                                   mask_tokens(oracle_sampler, tokenizer.pad_token_id),
                                                                                                   mask_tokens(oracle_sampler, tokenizer.pad_token_id),
                                                                                                   detokenizer=de_interner)
        for n, t in [('val', val), ('test', test)]:
            logging.info(f'Decoding on {n}')
            _, _, ico_only_hard_pred, ico_only_tru = make_preds_epoch(ico_only_evidence_classifier.cuda(),
                                                                      [instance.to_model_input('ico_only') for instance in oracle_decoding_instances(t)],
                                                                      tokenizer.sep_token_id, params['evidence_classifier']['batch_size'],
                                                                      device='cuda:0',
                                                                      criterion=None)
            e2e_score(ico_only_tru, ico_only_hard_pred, 'ICO only scoring', evidence_classes)
        ico_only_evidence_classifier = ico_only_evidence_classifier.cpu()

if __name__ == '__main__':
    main()