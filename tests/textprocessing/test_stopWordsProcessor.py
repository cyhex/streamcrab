from unittest import TestCase
from smm.classifier.textprocessing import StopWordsProcessor
__author__ = 'gx'


class TestStopWordsProcessor(TestCase):

    def setUp(self):
        self.text = "hello my name is Timor "

    def test_getSearchTokens(self):
        result = StopWordsProcessor.getSearchTokens(self.text)
        expect = set("hello name timor".split())
        self.assertEqual(expect, result)

    def test_getClassifierTokens(self):
        result = StopWordsProcessor.getClassifierTokens(self.text)
        expect = set("hello name timor".split())
        self.assertEqual(expect, result)