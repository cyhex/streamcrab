#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

__author__ = 'gx'


import argparse
from smm import models

models.connect()

print ''
print 'Raw Training data:'
print '------------------'
print "Positive %d records" % models.TrainDataRaw.objects(polarity=1).count()
print "Negative %d records" % models.TrainDataRaw.objects(polarity=-1).count()

print '\n'

def print_trained_cls(row):
    h = "TrainedClassifier: %s" % row.name
    print h
    print '-' * len(h)
    print "ID: %s" % row.id
    print "Date: %s" % row.id.generation_time

    for k,v in row.stats.items():
        print "%s : %s" % (k.capitalize(),v)

    print "Training data size %0.2f (MB)" % (row.classifier.length /1024.0/1024.0)


    print '\n'


[print_trained_cls(row) for row in models.TrainedClassifiers.objects()]