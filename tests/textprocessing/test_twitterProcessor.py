from unittest import TestCase
from smm.classifier.textprocessing import TwitterProcessor
__author__ = 'gx'


class TestStopStemmTwitterProcessor(TestCase):
    def setUp(self):
        self.text = "The quick brown fox was jumping over the lazy dog #crazyfox @thedog http://fox.com :)"

    def test_getClean(self):
        self.assertEqual("the quick brown fox was jumping over the lazy dog #crazyfox @thedog http://fox.com  __h__",
                         TwitterProcessor.clean(self.text))

    def test_getSearchTokens(self):
        self.assertEqual(
            ['quick', 'brown', 'fox', 'jumping', 'lazy', 'dog', 'crazyfox', 'thedog', 'http', 'fox',
             'com', '__h__'],
            TwitterProcessor.getSearchTokens(self.text))

    def test_getClassifierTokens(self):
        self.assertEqual(['quick', 'brown', 'fox', 'jump', 'lazi', 'dog', '#crazyfox', '__h__'],
                         TwitterProcessor.getClassifierTokens(self.text))

    def test_getFeatures(self):
        result = TwitterProcessor.getFeatures(self.text)
        expect = {'quick': 1, 'brown': 1, 'fox': 1, 'jump': 1, 'lazi': 1, 'dog': 1, '#crazyfox': 1, '__h__': 1}
        self.assertEqual(expect, result)