from abstract import TestCaseDB
from smm.models import ClassifiedStream
import json
__author__ = 'gx'


class TestClassifiedStream(TestCaseDB):

    def test_find_tokens(self):
        s1 = ClassifiedStream()
        s1.tokens = ['a','b']
        s1.text = 'ab'
        s1.source = 't'
        s1.save()

        s2 = ClassifiedStream()
        s2.tokens = ['b','c']
        s2.text = 'bs'
        s2.source = 't'
        s2.save()

        self.assertEquals(2, len(ClassifiedStream.find_tokens(['a', 'b'])))
        self.assertEquals(1, len(ClassifiedStream.find_tokens(['a'])))
        self.assertEquals(1, len(ClassifiedStream.find_tokens(['a', 'b'], s1.id)))

    def tearDown(self):
        ClassifiedStream.drop_collection()
