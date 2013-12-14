from unittest import TestCase
from smm.classifier.textprocessing import StopBigramTwitterProcessor
from smm.classifier.ngrams import bigrams
__author__ = 'gx'


class TestStopTwitterProcessor(TestCase):

    def setUp(self):
        self.text = "hello :) my name is not @Timor #hashtag http://cyhex.com"

    def test_clean(self):
        result = StopBigramTwitterProcessor.clean(self.text).split()
        expect = 'hello  __h__  my name is  __not__  @timor #hashtag http://cyhex.com'.split()
        self.assertEqual(expect, result)

    def test_getSearchTokens(self):
        result = StopBigramTwitterProcessor.getSearchTokens(self.text)
        expect = "hello  __h__  name  __not__  @timor #hashtag http://cyhex.com".split()
        self.assertEqual(expect, result)

    def test_getClassifierTokens(self):
        result = StopBigramTwitterProcessor.getClassifierTokens(self.text)
        expect = bigrams("hello  __h__  name  __not__  #hashtag".split())
        self.assertEqual(expect, result)