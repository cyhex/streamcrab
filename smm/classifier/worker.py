__author__ = 'gx'
from nltk.classify.naivebayes import NaiveBayesClassifier


class ClassifierWorker(object):

    def __init__(self, classifier=NaiveBayesClassifier, training_data=None):
        self.classifier = classifier
        self.training_data = training_data

    def classify(self):
        pass