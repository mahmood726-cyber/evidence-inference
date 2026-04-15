# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 12:15:51 2018

@author: Eric
"""
import glob
import os
import random
from pathlib import Path

import numpy as np


# the locations of the files. Override with EVIDENCE_INFERENCE_ANNOTATIONS env var
# (lessons.md "No hardcoded local paths in deployable code"). Default falls back to
# the repo-relative annotations/ directory which is the version-controlled layout
# distributed with this repository.
_repo_root = Path(__file__).resolve().parent.parent
_default_loc = _repo_root / 'annotations'
loc = os.environ.get('EVIDENCE_INFERENCE_ANNOTATIONS', str(_default_loc))
if not loc.endswith(('/', os.sep)):
    loc = loc + os.sep
loc_files = loc + 'xml_files/*.nxml'
loc_train = loc + 'splits/' + 'train_article_ids.txt'
loc_val   = loc + 'splits/' + 'validation_article_ids.txt'
loc_test  = loc + 'splits/' + 'test_article_ids.txt'

# load in the articles
files = set(list(map(lambda x: int(x.split("\\")[-1].split(".")[0].split("PMC")[1]), glob.glob(loc_files))))

# load in the data
train = np.loadtxt(loc_train, dtype = int, delimiter = " ")
val   = np.loadtxt(loc_val, dtype = int, delimiter = " ")
test  = np.loadtxt(loc_test, dtype = int, delimiter = " ")

# define what we have already done
placed = set(train).union(set(val)).union(set(test))

# what needs to be placed
to_do = list(files - placed)

# Shuffle randomly, and split into 80, 10, 10 splits
random.shuffle(to_do)
tr_split = int(.8 * len(to_do)) # where to end
va_split = int(.9 * len(to_do)) # where to end
to_train = to_do[:tr_split]
to_val   = to_do[tr_split:va_split]
to_test  = to_do[va_split:]

# Notify user of progress
print("Training articles   added: {}".format(len(to_train))) 
print("Validation articles added: {}".format(len(to_val))) 
print("Testing articles    added: {}".format(len(to_test))) 

# append to existing datasets
train = np.append(train, to_train)
val   = np.append(val,   to_val)
test  = np.append(test,  to_test)

# save the new files
np.savetxt(loc_train, train, fmt = "%d", delimiter = " ")
np.savetxt(loc_val,   val,   fmt = "%d", delimiter = " ")
np.savetxt(loc_test,  test,  fmt = "%d", delimiter = " ")

# Notify user of progress
print("Final training   articles: {}".format(len(train))) 
print("Final validation articles: {}".format(len(val))) 
print("Final testing    articles: {}".format(len(test))) 