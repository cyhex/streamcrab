# -*- coding: utf-8 -*-
import sys
sys.path.append('../../')
from tracker.lib.mood_detection import MoodDetectTrainer
import nltk
import os,cPickle,gzip

MD = MoodDetectTrainer()
MD.load()

#print MD.classifier.show_most_informative_features(50)

fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../data', 'mood_traing_test_50000.dat')

MDT_data = cPickle.load(gzip.open(fileName,'rb'))

print nltk.classify.accuracy(MD.classifier, MDT_data)