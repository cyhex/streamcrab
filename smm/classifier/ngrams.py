# -*- coding: utf-8 -*-
from collections import defaultdict

def trigrams(oset):
    return ngram(oset,3)

def bigrams(oset):
    return ngram(oset,2)

def unigrams(oset):
    return ngram(oset,1)

def ngram(oset,n):
    
    grams = []
    c = 0
    tc  = len(oset)
    while c < tc-(n-1):
        gt = []
        for i in range(n):
            gt.append(oset[c+i])
        grams.append(''.join(gt))
        c+=1

    return grams

