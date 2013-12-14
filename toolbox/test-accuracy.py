#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

__author__ = 'gx'

import argparse
import argcomplete
import sys
import io
import nltk

from smm.classifier.textprocessing import feature_extractor
from smm.classifier import labels
from smm import models


parser = argparse.ArgumentParser(description='Test accuracy of Trained data',
                                 usage='python test-accuracy.py myClassifier data/testDataSource.csv')
parser.add_argument('name', help='Classifier name')
parser.add_argument('src', help='Data source name ')
args = parser.parse_args()

argcomplete.autocomplete(parser)

models.connect()

if not models.TrainedClassifiers.objects(name=args.name).count():
    print "TrainedClassifier %s do not exists \n" % args.name
    print "Available TrainedClassifiers:"
    print '----------------------------'
    for row in models.TrainedClassifiers.objects():
        print row.name
    sys.exit()



f = io.open(args.src,'r')
gold = []

for l in f.readlines():
    label, text = l.split('\t')
    if label in [labels.negative, labels.positive]:
        gold.append(((feature_extractor(text), label)))


row  = models.TrainedClassifiers.objects(name=args.name).first()
cls = row.get_classifier_ins()

print nltk.classify.accuracy(cls, gold)