__author__ = 'gx'

import argparse
import sys

from smm.classifier.textprocessing import feature_extractor
from smm import models


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
cls = row.get_classifier_ins()
print "exit: ctrl+c \n"
print "Loaded %s" % row.name

try:
    while True:
        txt = raw_input('Classify: ')

        prob = cls.prob_classify(feature_extractor(txt))
        classified_label = cls.classify(feature_extractor(txt))
        print ''
        print "Classification: %s with %0.2f%%" % (classified_label, prob.prob(classified_label) * 100)
        print ""
        cls.explain(feature_extractor(txt))
        print '\n'

except (KeyboardInterrupt, SystemExit, EOFError):
    print ' quiting...\n'