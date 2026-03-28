import random
import math
import torch
from dataclasses import dataclass
from typing import List, Tuple, Union, Callable, Set, Dict
from evidence_inference.preprocess.representations import Document

@dataclass(frozen=False, repr=True, eq=True)
class Annotation:
    doc: Document
    prompt_id: str
    tokenized_sentences: List[List[int]]
    i: Union[str, Tuple[int, ...], torch.IntTensor]
    c: Union[str, Tuple[int, ...], torch.IntTensor]
    o: Union[str, Tuple[int, ...], torch.IntTensor]
    evidence_texts: Tuple[Union[str, List[int]]]
    evidence_spans: Tuple[Tuple[int, int], ...]
    evidence_vector: Union[Tuple[int, ...], torch.IntTensor]
    significance_class: Union[str, int]

    def retokenize(self, bert_tokenizer, do_intern=True) -> 'Annotation':
        def handle_str(s):
            if isinstance(s, str):
                if do_intern:
                    return bert_tokenizer.encode(s, add_special_tokens=False)
                else:
                    return bert_tokenizer.tokenize(s, add_special_tokens=False)
            elif isinstance(s, (list, tuple)) and do_intern:
                ret = []
                for elem in s:
                    ret.extend(handle_str(elem))
                return ret
            else:
                raise ValueError(f'Attempted to retokenize or tokenize untokenizeable instance {s}')
        
        return Annotation(doc=self.doc,
                          prompt_id=self.prompt_id,
                          tokenized_sentences=self.tokenized_sentences,
                          i=tuple(handle_str(self.i)),
                          c=tuple(handle_str(self.c)),
                          o=tuple(handle_str(self.o)),
                          evidence_texts=tuple(handle_str(s) for s in set(map(str.lower, filter(lambda x: isinstance(x, str), self.evidence_texts)))),
                          evidence_spans=self.evidence_spans,
                          evidence_vector=self.evidence_vector,
                          significance_class=self.significance_class)

def get_identifier_sampler(params: dict) -> Callable[[Annotation], List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]]:
    if 'length_ratio' in params['evidence_identifier']:
        return get_length_identifier_sampler(params)
    ratio = params['evidence_identifier']['sampling_ratio']
    # returns sentence text, ico, classification
    def identifier_sampler(ann: Annotation) -> List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]:
        pos = []
        neg = []
        for tokens, sent in zip(ann.tokenized_sentences, ann.doc.sentences):
            i = torch.IntTensor(ann.i)
            c = torch.IntTensor(ann.c)
            o = torch.IntTensor(ann.o)
            if sent.labels is not None and sent.labels['evidence'] == 1:
                pos.append((tokens, (i, c, o), 1))
            else:
                neg.append((tokens, (i, c, o), 0))
        samples = random.sample(neg, k=min(len(neg), int(ratio * len(pos)))) + pos
        random.shuffle(samples)
        return samples
    return identifier_sampler

def get_length_identifier_sampler(params: dict) -> Callable[[Annotation], List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]]:
    ratio = params['evidence_identifier']['sampling_ratio']
    length_ratio = params['evidence_identifier']['length_ratio']
    # returns sentence text, ico, classification
    def identifier_sampler(ann: Annotation) -> List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]:
        pos = []
        neg = []
        for tokens, sent in zip(ann.tokenized_sentences, ann.doc.sentences):
            i = torch.IntTensor(ann.i)
            c = torch.IntTensor(ann.c)
            o = torch.IntTensor(ann.o)
            if sent.labels is not None and sent.labels['evidence'] == 1:
                pos.append((tokens, (i, c, o), 1))
            else:
                neg.append((tokens, (i, c, o), 0))
        #samples = random.sample(neg, k=min(len(neg), int(ratio * len(pos)))) + pos
        #random.shuffle(samples)
        #return samples
        samples = list(pos)
        for p in pos:
            lower_bound = len(pos) * (1 - length_ratio)
            upper_bound = len(pos) * (1 + length_ratio)
            acceptable_negatives = list(filter(lambda n: lower_bound <= len(n[0]) and upper_bound >= len(n[0]), neg))
            if len(acceptable_negatives) > ratio:
                samples.extend(random.sample(acceptable_negatives, k=math.ceil(ratio)))
            else:
                samples.extend(acceptable_negatives)
        random.shuffle(samples)
        return samples
    return identifier_sampler

def identifier_everything_sampler(ann: Annotation) -> List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]:
    ret = []
    for tokens, sent in zip(ann.tokenized_sentences, ann.doc.sentences):
        i = torch.IntTensor(ann.i)
        c = torch.IntTensor(ann.c)
        o = torch.IntTensor(ann.o)
        if sent.labels is not None and sent.labels['evidence'] == 1:
            cls = 1
        else:
            cls = 0
        ret.append((tokens, (i, c, o), cls))
    return ret


def get_classifier_oracle_sampler(params: dict) -> Callable[[Annotation], List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]]:
    evidence_classes = params['evidence_classifier']['classes']
    ec_map = {x:i for i,x in enumerate(evidence_classes)}
    def classifier_oracle_sampler(ann: Annotation) -> List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]:
        pos = []
        for tokens, sent in zip(ann.tokenized_sentences, ann.doc.sentences):
            i = torch.IntTensor(ann.i)
            c = torch.IntTensor(ann.c)
            o = torch.IntTensor(ann.o)
            if sent.labels is not None and sent.labels['evidence'] == 1:
                pos.append((tokens, (i, c, o), ann.significance_class))
        if len(pos) == 0:
            return pos
        return random.sample(pos, k=1)
    return classifier_oracle_sampler

def mask_tokens(sampler: Callable[[Annotation], List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]],
                pad_token_id: int) -> Callable[[Annotation], List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]]:
    def masked_sampler(ann: Annotation):
        samples = sampler(ann)
        ret = []
        for _, ico, cls in samples:
            ret.append((torch.IntTensor([pad_token_id]), ico, cls))
        return ret
    return masked_sampler

def get_classifier_sampler(params: dict) -> Callable[[Annotation], List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]]:
    evidence_classes = params['evidence_classifier']['classes']
    ec_map = {x:i for i,x in enumerate(evidence_classes)}
    def classification_sampler(ann: Annotation) -> List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]:
        ret = []
        for tokens, sent in zip(ann.tokenized_sentences, ann.doc.sentences):
            i = torch.IntTensor(ann.i)
            c = torch.IntTensor(ann.c)
            o = torch.IntTensor(ann.o)
            if sent.labels is not None and sent.labels['evidence'] == 1:
                ret.append((tokens, (i, c, o), ann.significance_class))
        random.shuffle(ret)
        return ret 
    return classification_sampler

def classifier_everything_sampler(ann: Annotation) -> List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]:
    ret = []
    for tokens, sent in zip(ann.tokenized_sentences, ann.doc.sentences):
        i = torch.IntTensor(ann.i)
        c = torch.IntTensor(ann.c)
        o = torch.IntTensor(ann.o)
        ret.append((tokens, (i, c, o), ann.significance_class))
    return ret 

def mask_sampler(sampler: Callable[[Annotation], List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]],
                 fields_to_mask: Set[str]) -> Callable[[Annotation], List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]]:
    fields_to_tuple_pos = {
        'i': 0,
        'c': 1,
        'o': 2,
    }
    fields_to_mask = {fields_to_tuple_pos[f] for f in fields_to_mask}
    pad = torch.IntTensor([0])
    def get_sampler(ann: Annotation) -> List[Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]]:
        unmasked = sampler(ann)
        ret = []
        for (sent, ico, kls) in unmasked:
            new_ico = []
            for i, ico_elem in enumerate(ico):
                if i in fields_to_mask:
                    new_ico.append(pad)
                else:
                    new_ico.append(ico_elem)
            ret.append((sent, tuple(new_ico), kls))
        return ret
    return get_sampler

@dataclass(frozen=True, repr=True, eq=True)
class DecodeInstance:
    docid: str
    prompt_id: str
    idx: int
    sentence: torch.IntTensor
    ico: Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor]
    identifier_class: int
    classification_class: int

    def to_model_input(self, class_type) -> Tuple[torch.IntTensor, Tuple[torch.IntTensor, torch.IntTensor, torch.IntTensor], int]:
        ico = self.ico
        sent = self.sentence
        if class_type == 'identifier':
            cls = self.identifier_class
        elif class_type == 'classifier':
            cls = self.classification_class
        elif class_type == 'unconditioned_classifier':
            cls = self.classification_class
            ico = (torch.IntTensor([0]), torch.IntTensor([0]), torch.IntTensor([0]))
        elif class_type == 'unconditioned_identifier':
            cls = self.identifier_class
            ico = (torch.IntTensor([0]), torch.IntTensor([0]), torch.IntTensor([0]))
        elif class_type == 'ico_only':
            cls = self.classification_class
            sent = (0,)
        else:
            raise ValueError(f'unknown type {class_type}')
        return (sent, ico, cls)
