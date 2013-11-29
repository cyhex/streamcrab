from unittest import TestCase
from smm.classifier.textprocessing import StopPosTwitterProcessor
__author__ = 'gx'


class TestStopPosTwitterProcessor(TestCase):

    def setUp(self):
        self.text = "hi :) whats up ? my name is not Timor #hastag @somename http://cyhex.com"

    def test_getClassifierTokens(self):
        result = StopPosTwitterProcessor.getClassifierTokens(self.text)
        expect = set([('__not__', 'NNP'), ('__h__', 'NNP'), ('?', '.'), ('hi', 'NN'), ('name', 'NN'),
                      ('@somename', 'NN'), ('whats', 'NNS'), ('__', 'NNP'), ('#hastag', 'NNP'), ('timor', 'NN')])
        self.assertEqual(expect, result)