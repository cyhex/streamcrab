# -*- coding: utf-8 -*-

import unittest
from tracker.lib.tokenizer import tokenizer
from collections import defaultdict


class TestToknizer(unittest.TestCase):

    def testTokenSimple(self):
        r1 = tokenizer().tokenize(u'This is a fox')
        r2 = [u'this', u'is', u'a', u'fox']
        assert r1 == r2
    
    def testTokenEmos(self):
        r1 = tokenizer().tokenize(u'This is a fox :) :(')
        r2 = [u'this', u'is', u'a', u'fox', u'##s##', u'##b##']
        assert r1 == r2
    
    
    def testTokenUsername(self):
        r1 = tokenizer().tokenize(u'This is a @fox')
        r2 = [u'this', u'is', u'a']
        assert r1 == r2
    
    def testTokenHash(self):
        r1 = tokenizer().tokenize(u'This is a #fox')
        r2 = [u'this', u'is', u'a']
        assert r1 == r2

    def testTokenCharFold(self):
        r1 = tokenizer().tokenize(u'This is a fooooooox')
        r2 = [u'this', u'is', u'a', u'foox']
        assert r1 == r2



    def testTokenUrl(self):
        r1 = tokenizer().tokenize(u'This is a http://fox.com fox news')
        r2 = [u'this', u'is', u'a',u'fox',u'news']
        assert r1 == r2
    
    
    def testTokenUnicode(self):
        r1 = tokenizer().tokenize(u'This is a föx')
        r2 = [u'this', u'is', u'a', u'föx']
        assert r1 == r2


    def testTokenInvalidInput(self):
        r1 = tokenizer().tokenize(u'This ### ##b ##s +++ *** \' !§$%x&/()=? " "')
        r2 = [u'this', u'x']
        assert r1 == r2

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()