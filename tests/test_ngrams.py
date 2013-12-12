from unittest import TestCase
from smm.classifier import ngrams
__author__ = 'gx'


class TestTrigrams(TestCase):

    def test_trigrams(self):
        self.assertEqual(['abc', 'bcd'], ngrams.trigrams(['a', 'b', 'c', 'd']))

    def test_bigrams(self):
        self.assertEqual(['ab', 'bc', 'cd'], ngrams.bigrams(['a', 'b', 'c', 'd']))

    def test_unigrams(self):
        self.assertEqual(['a', 'b', 'c', 'd'], ngrams.unigrams(['a', 'b', 'c', 'd']))

    def test_ngram(self):
        self.assertEqual(['abcd', 'bcde', 'cdef', 'defg', 'efgh'], ngrams.ngram(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'], 4))


