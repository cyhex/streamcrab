from abstract import TestCaseDB
from smm import models
import nltk


__author__ = 'gx'



class TestTrainedClassifiers(TestCaseDB):

    def setUp(self):
        TestCaseDB.setUp(self)
        self.cls = nltk.NaiveBayesClassifier.train([({'a':'a', 'b':'b'}, 'positive')])


    def test_set_get_classifier(self):
        row = models.TrainedClassifiers()
        row.name = 'test'
        row.set_classifier(self.cls)
        row.save()
        self.assertIsInstance(row.get_classifier(), nltk.NaiveBayesClassifier)

    def tearDown(self):
        models.TrainedClassifiers.drop_collection()