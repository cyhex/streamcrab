#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

__author__ = 'gx'

import nltk
import pickle
import argparse
import argcomplete
import sys
import io

from smm.classifier.textprocessing import feature_extractor, TwitterMixin
from smm import models
from smm.classifier import labels
from smm import config
import io

parser = argparse.ArgumentParser(description='Classify collected raw tweets', usage='python train-classifier.py myClassifier 1000')
parser.add_argument('name', help='Classifier name - must be unique')
parser.add_argument('size', type=int, help='Corpus size - how much tweets to classify')
parser.add_argument('-t', '--type', help='Classifier type', default='maxent')
parser.add_argument('-c', '--cutoff', type=float, default=-0.02, required=False, help='Log Likelihood cutoff')
parser.add_argument('-s', '--source', default=None, required=False, help="Classify from csv file")
args = parser.parse_args()

argcomplete.autocomplete(parser)

models.connect()

if not args.source and models.TrainDataRaw.objects(polarity=1).count() < args.size:
    print "There is only %d positive tweeets in DB" % models.TrainDataRaw.objects(polarity=1).count()
    print "Reduce Corpus size or collect more tweets using toolbox/collect-tweets.py"
    sys.exit()

if not args.source and models.TrainDataRaw.objects(polarity=-1).count() < args.size:
    print "There is only %d negative tweeets in DB" % models.TrainDataRaw.objects(polarity=-1).count()
    print "Reduce Corpus size or collect more tweets using toolbox/collect-tweets.py"
    sys.exit()

if not args.source and models.TrainedClassifiers.objects(name = args.name).count():
    print "TrainedClassifier already exists with name %s try to different name" % args.name
    sys.exit()


# TODO: move to parsers
if args.source:
    featureset = []
    f = io.open(args.source)
    c = 0
    for l in f.readlines():
        pos, id, posScore, negScore, synsetTerm, gloss = l.split('\t')

        c += 1

        if c == 1:
            continue

        gloss = TwitterMixin.make_plain(gloss)
        print negScore
        negScore = float(negScore)
        posScore = float(posScore)

        if posScore > negScore:
            label = labels.positive
        elif posScore < negScore:
            label = labels.negative
        else:
            continue

        featureset.append(( feature_extractor(gloss), label))

else:

    featureset = [(feature_extractor(row.text), labels.positive) for row in models.TrainDataRaw.objects(polarity=1)[0:args.size]]
    featureset += [(feature_extractor(row.text), labels.negative) for row in models.TrainDataRaw.objects(polarity=-1)[0:args.size]]

if args.type == 'maxent':
    # Train
    # min_ll - Log Likelihood drop Training iterations if min_ll > -0.02
    cls = nltk.MaxentClassifier.train(featureset, min_ll=args.cutoff)
elif args.type == 'bayes':
    cls = nltk.NaiveBayesClassifier.train(featureset)
else:
    print '%s is not valid classifier type' % args.type
    sys.exit()

# Save
row = models.TrainedClassifiers()
row.name = args.name
row.classifier = pickle.dumps(cls, 1)
row.stats = dict(
    classifier=cls.__class__.__name__,
    tokenizer=config.classifier_tokenizer.__name__,
    sample_size=args.size * 2,
    cutoff=args.cutoff
)

row.save()


print "TrainedClassifier saved with ID: %s  Name: %s" % (row.id, row.name)


# if date size is to big to fit into your ram try to use nltk.apply_features
# --------------------------------------------------------------------------
#
# def apply_features(row):
#   return (feature_extractor(row.text), row.get_label())
#
# featureset = nltk.apply_features(apply_features, models.TrainDataRaw.objects(polarity=1)[0:15])
# featureset += nltk.apply_features(apply_features, models.TrainDataRaw.objects(polarity=-1)[0:15])
