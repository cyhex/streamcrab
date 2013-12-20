#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
__author__ = 'gx'

import argparse
import sys

from smm import models
from smm import config

parser = argparse.ArgumentParser(description='Interact directly with Trained data',
                                 usage='python shell-classifier.py myClassifier')
parser.add_argument('name', help='Classifier name')
args = parser.parse_args()

models.connect()

if not models.TrainedClassifiers.objects(name=args.name).count():
    print "TrainedClassifier %s do not exists \n" % args.name
    print "Available TrainedClassifiers:"
    print '----------------------------'
    for row in models.TrainedClassifiers.objects():
        print row.name
    sys.exit()

row = models.TrainedClassifiers.objects(name=args.name).first()
cls = row.get_classifier()
print "exit: ctrl+c \n"
print "Loaded %s" % row.name

try:
    while True:
        txt = raw_input('Classify: ')
        features = config.classifier_tokenizer.getFeatures(txt)
        prob = cls.prob_classify(features)
        classified_label = cls.classify(features)
        print ''
        print "Classification: %s with %0.2f%%" % (classified_label, prob.prob(classified_label) * 100)
        print ""
        cls.explain(features)
        print '\n'

except (KeyboardInterrupt, SystemExit, EOFError):
    print ' quiting...\n'