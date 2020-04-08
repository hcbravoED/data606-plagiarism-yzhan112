#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 07:22:09 2017

@author: hcorrada
"""
import scipy.optimize as opt
import math
from collections import defaultdict
from plagiarism_lib.hashing import _make_vector_hash

# Choose number of bands for LSH based on threshold t and number of rows
# in minhash signature matrix n
#
# t: desired threshold for candidate detection (double in (0,1))
# n: number of rows in minhash signature matrix
#
# returns: tuple (b, final_t)
#    b: number of bands (integer such that b*r = n)
#    final_t: the final threshold t = (1/b)^(1/r) s.t. b*r=n
#
# Uses Nelder-Mead optimization method to find value b such that
# (1/b)^(b/n) is closest (in least squares) value possible to input threshold t
#
# Example:
#   b, final_t = _choose_nbands(.8, 100)
def _choose_nbands(t, n):
    def _error_fun(x):
        cur_t = (1/x[0])**(x[0]/n)
        return (t-cur_t)**2

    opt_res = opt.minimize(_error_fun, x0=(10), method='Nelder-Mead')
    b = int(math.ceil(opt_res['x'][0]))
    r = int(n / b)
    final_t = (1/b)**(1/r)
    return b, final_t

def _do_lsh(mh_matrix, threshold):
    n = mh_matrix._num_hashes

    # choose the number of bands, and rows per band to use in LSH
    b, _ = _choose_nbands(threshold, n)
    r = int(n / b)
    print ("Using %d bands for %d rows" % (b, n))

    ndocs = len(mh_matrix._docids)

    # generate a random hash function that takes vectors of length r as input
    hash_func = _make_vector_hash(r)

    # initalize list of hashtables, will be populated with one hashtable
    # per band
    buckets = []

    # fill hash tables for each band
    for band in range(b):
        hashtable = defaultdict(list)
        start = r * band
        end = min(start + r, n)
        for i in range(ndocs):
            hashtable[hash_func(mh_matrix._mat[start:end, i])].append(mh_matrix._docids[i])
        buckets.append(hashtable)
    return buckets

def _get_candidates(hashtables):
    candidates = set()
    for hashtable in hashtables:
        for bucket in hashtable.values():
            l = len(bucket)
            if l > 1:
                #print(bucket)
                bucket.sort()
                for i in range(l-1):
                    for j in range(i+1, l):
                        item = (bucket[i], bucket[j])
                        candidates.add(item)
    return list(candidates)

class LSH:
    def __init__(self, threshold):
        self._threshold = threshold
        self._hashtables = None

    def do_lsh(self, mh_matrix):
        self._hashtables = _do_lsh(mh_matrix, self._threshold)

    def get_candidates(self):
        return _get_candidates(self._hashtables)
