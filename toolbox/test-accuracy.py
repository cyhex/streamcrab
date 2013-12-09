__author__ = 'gx'

import argparse
import sys

from smm.classifier.textprocessing import feature_extractor
from smm import models


parser = argparse.ArgumentParser(description='Test accuracy of Trained data',
                                 usage='python test-accuracy.py myClassifier datasource.csv')
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
