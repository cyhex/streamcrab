 # coding=utf-8

__author__ = 'gx'

from abstract import TestCaseDB
from smm import models

class TestUnicode(TestCaseDB):

    def test_UnicodeMongo(self):
        r = models.ClassifiedStream()
        r.text = 'hällo'
        r.source = 't'
        r.save()
        print r.text

        r = models.ClassifiedStream()
        r.text = unicode.encode(u'really be on google box \ud83d\ude02\ud83d\ude02\ud83d\ude02','utf-8')
        r.source = 't'
        r.save()

        print r.to_dict()

