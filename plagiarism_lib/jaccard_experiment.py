#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 12:40:55 2017

@author: hcorrada
"""

import pandas as pd
import random
import numpy as np

from plagiarism_lib.article_db import ArticleDB
from plagiarism_lib.jaccard import Jaccard

def _setup_fp_dataset(artdb, truth_file):
    with open(truth_file, 'r') as f:
        truth_pairs = [tuple(sorted(line.strip().split()))
                       for line in f]
        # print(truth_pairs)

        true_articles = set()
        for s1, s2 in truth_pairs:
            true_articles.add(s1)
            true_articles.add(s2)

        print(f"true_articles is{true_articles}")
        alldocs = set(artdb._docids)
        # print(f"alldocs is {alldocs}")
        false_candidates = alldocs.difference(true_articles)
        # print(f"false_candidates is {false_candidates}")
        false_partners = random.sample(false_candidates, len(true_articles))
        print(f"false_partners is {false_partners}")
        false_pairs = list(zip(true_articles, false_partners))
        print(f"false_pairs is {false_pairs}")


        alldocs = list(true_articles) + false_partners
        return truth_pairs, false_pairs, alldocs

def _get_kstats(truth_pairs, false_pairs, jacc):
    true_sims = [jacc.get_similarity(x,y) for x,y in truth_pairs]
    false_sims = [jacc.get_similarity(x,y) for x,y in false_pairs]

    tp = np.mean(true_sims)
    fp = np.mean(false_sims)

    return tp, fp

def run_experiment(train_file, truth_file,
                   kvals = [2,5,10,20,40,60,120]):
    artdb = ArticleDB(train_file)
    truth_pairs, false_pairs, alldocs = _setup_fp_dataset(artdb, truth_file)

    tp = []
    fp = []

    for k in kvals:
        print("Processing data for k=", k)
        shingled_data = artdb.shingle_data(k)


        jacc = Jaccard()
        jacc.compute_similarity(shingled_data, docids=alldocs)

        ktp, kfp = _get_kstats(truth_pairs, false_pairs, jacc)
        tp.append(ktp)
        fp.append(kfp)

    df = pd.DataFrame({'k': kvals, 'sim_true': tp, 'sim_false': fp})
    return df
