from abstract import TestCaseDB
from smm.models import ClassifiedStream
import json
__author__ = 'gx'


class TestClassifiedStream(TestCaseDB):

    def test_find_tokens(self):
        s1 = ClassifiedStream()
        s1.tokens = ['a', 'b', 'c']
        s1.text = 'ab'
        s1.source = 't'
        s1.save()

        s2 = ClassifiedStream()
        s2.tokens = ['b', 'c']
        s2.text = 'bs'
        s2.source = 't'
        s2.save()

        s3 = ClassifiedStream()
        s3.tokens = ['b', 'c']
        s3.text = 'bs'
        s3.source = 't'
        s3.save()

        self.assertEquals(1, len(ClassifiedStream.find_tokens(['a', 'b'])))
        self.assertEquals(1, len(ClassifiedStream.find_tokens(['a'])))
        self.assertEquals(1, len(ClassifiedStream.find_tokens(['c', 'b'], s2.id)))
        self.assertEquals(3, len(ClassifiedStream.find_tokens(['c', 'b'])))

    def tearDown(self):
        ClassifiedStream.drop_collection()
