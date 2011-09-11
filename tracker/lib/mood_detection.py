# -*- coding: utf-8 -*-
import nltk
from collections import defaultdict
from tokenizer import tokenizer, WordGramTokenizer
import ngrams
import cPickle
import os
import gzip
from nltk.probability import FreqDist
from tracker.lib.supportedLangs import supportedLangs
import re


class MoodDetectTrainData(list):
    
    tk = WordGramTokenizer()
    
    def addRow(self,text,label,lang):
        
        if not isinstance(text,unicode):
            raise Exception('not unicode')
        
        if not lang in supportedLangs:
            lang = 'other'
        
        data_sub_set = self.tk.tokenize(text,lang)
        data_sub_set['x_lang'] = lang
        
        self.append((data_sub_set,label))
    

class MoodDetectTrainer(object):
    classifier = None
    raw_data = None
    
    
    def __init__(self,classifierClass=nltk.NaiveBayesClassifier,data_file = "mood_traing.dat"):
        self.CLSclassifier = classifierClass
        self.fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../data', data_file)
        
        
    def train(self,TrainData):
        self.raw_data = TrainData
        self.classifier = self.CLSclassifier.train(TrainData)
    
    def save(self):
        file = gzip.open(self.fileName,'wb')
        cPickle.dump(self.raw_data , file, protocol=2)
        file.close()
        
    def load(self):
        if not self.classifier:
            file = gzip.open(self.fileName,'rb')
            TrainData = cPickle.load(file)
            self.classifier = self.CLSclassifier.train(TrainData)
            file.close()
    



class MoodClasses(object):
    positive = 'p'
    negative = 'n'
    neutral = '-'    


class MoodDetect(object):
    
    dumping = 0.65
    
    tk = WordGramTokenizer()
    
    def __init__(self,Trainer):
        self.trainer = Trainer
        self.trainer.load()
    
    
    def setUpSearchPhraseCleaner(self,searchPhrase):
        keywords = searchPhrase.split()
        
        re_str  = ""
        for k in keywords:
            re_str += "%s|" % re.escape(k)
        
        re_str = re_str[:len(re_str)-1]
        self.cleanSearch = re.compile(re_str, re.IGNORECASE)
      
    def cleanSearchPhrase(self,text):
        return  self.cleanSearch.sub('',text)
    
    
    def classify(self,text,lang):
        if not isinstance(text,unicode):
            raise Exception('not unicode')
        
        if not lang in supportedLangs:
            lang = 'other'
            
        text = self.cleanSearchPhrase(text)
        
        m = MoodClasses()
        data_sub_set = self.tk.tokenize(text,lang)
        
        
        if not data_sub_set:
            return  0.0
        
        data_sub_set['x_lang'] = lang
        
        ret = self.trainer.classifier.prob_classify(data_sub_set)
        
        p_score = ret.prob(m.positive)
        n_score = ret.prob(m.negative)
        
        if max(p_score,n_score) <= self.dumping:
            return 0.0
        
        if p_score > n_score:
            return p_score
        
        elif n_score > p_score:
            return n_score*-1.0
        
        else:
            return 0.0
        
        


