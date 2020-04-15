#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 12:55:13 2017

@author: hcorrada
"""

from itertools import combinations

def _jaccard_similarity(s1, s2):
    return len(s1.intersection(s2)) / len(s1.union(s2))

class Jaccard:
    def __init__(self):
        self._jaccard_dict = None

    def compute_similarity(self, shingled_data, docids=None):
        if docids is not None:
            shingled_data = [x for x in shingled_data if x[0] in docids]

        ndocs = len(shingled_data)
        self._jaccard_dict = dict()
        #shingled_dic = dict(shingled_data)
        #ndocs = list(map(lambda x: x[0], shingled_data))

        '''
        for c in combinations(ndocs, 2):
            key = sorted(c)
            js = _jaccard_similarity(shingled_dic(c[0]), shingled_dic(c[1]))
            self._jaccard_dict[key] = js
        '''

        for i in range(ndocs-1):
            for j in range(i+1, ndocs):
                (doci, si) = shingled_data[i]
                (docj, sj) = shingled_data[j]

                key = tuple(sorted((doci, docj)))
                js = _jaccard_similarity(si, sj)
                self._jaccard_dict[key] = js


    def get_similarity(self, doci, docj):
        key = tuple(sorted((doci, docj)))
        return self._jaccard_dict[key]
