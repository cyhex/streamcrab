__author__ = 'gx'
from smm import config

class ClassifierWorker(object):

    def __init__(self, classifier=config.classifier_default, training_data=None):
        self.classifier = classifier
        self.training_data = training_data

    def classify(self):
        pass