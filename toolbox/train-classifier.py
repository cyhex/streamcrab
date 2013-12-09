__author__ = 'gx'

import nltk
import pickle
import argparse
import sys

from smm.classifier.textprocessing import feature_extractor
from smm import models
from smm.classifier import labels
from smm import config

parser = argparse.ArgumentParser(description='Classify collected raw tweets', usage='python train-classifier.py myClassifier 1000')
parser.add_argument('name', help='Classifier name - must be unique')
parser.add_argument('size', type=int, help='Corpus size - how much tweets to classify')
parser.add_argument('-c','--cutoff', type=float, default=-0.02, required=False, help='Log Likelihood cutoff')
args = parser.parse_args()

models.connect()

if models.TrainDataRaw.objects(polarity=1).count() < args.size:
    print "There is only %d positive tweeets in DB" % models.TrainDataRaw.objects(polarity=1).count()
    print "Reduce Corpus size or collect more tweets using toolbox/collect-tweets.py"
    sys.exit()

if models.TrainDataRaw.objects(polarity=-1).count() < args.size:
    print "There is only %d negative tweeets in DB" % models.TrainDataRaw.objects(polarity=-1).count()
    print "Reduce Corpus size or collect more tweets using toolbox/collect-tweets.py"
    sys.exit()

if models.TrainedClassifiers.objects(name = args.name).count():
    print "TrainedClassifier already exists with name %s try to different name" % args.name
    sys.exit()


featureset = [(feature_extractor(row.text), labels.positive) for row in models.TrainDataRaw.objects(polarity=1)[0:args.size]]
featureset += [(feature_extractor(row.text), labels.negative) for row in models.TrainDataRaw.objects(polarity=-1)[0:args.size]]

# Train
# min_ll - Log Likelihood drop Training iterations if min_ll > -0.02
cls = nltk.MaxentClassifier.train(featureset, min_ll=args.cutoff)

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
