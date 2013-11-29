from unittest import TestCase
from smm.classifier.textprocessing import StopTwitterProcessor
__author__ = 'gx'


class TestStopTwitterProcessor(TestCase):

    def setUp(self):
        self.text = "hello :) my name is not @Timor #hashtag http://cyhex.com"

    def test_clean(self):
        result = StopTwitterProcessor.clean(self.text).split()
        expect = 'hello  __h__  my name is  __not__  @timor #hashtag http://cyhex.com'.split()
        self.assertEqual(expect, result)

    def test_getSearchTokens(self):
        result = StopTwitterProcessor.getSearchTokens(self.text)
        expect = set("hello  __h__  name  __not__  @timor #hashtag http://cyhex.com".split())
        self.assertEqual(expect, result)

    def test_getClassifierTokens(self):
        result = StopTwitterProcessor.getClassifierTokens(self.text)
        expect = set("hello  __h__  name  __not__  @timor #hashtag".split())
        self.assertEqual(expect, result)