from unittest import TestCase
from smm.classifier.textprocessing import StopPosTwitterProcessor
__author__ = 'gx'


class TestStopPosTwitterProcessor(TestCase):

    def setUp(self):
        self.text = "hi :) whats up ? my name is not Timor #hastag @somename http://cyhex.com"

    def test_getClassifierTokens(self):
        result = StopPosTwitterProcessor.getClassifierTokens(self.text)
        expect = [('hi', 'NN'), ('__h__', 'NNP'), ('whats', 'NNS'), ('?', '.'), ('name', 'NN'), ('__', 'NNP'),
                  ('__not__', 'NNP'), ('__', 'NNP'), ('timor', 'NN'), ('#hastag', '-NONE-')]

        self.assertEqual(expect, result)