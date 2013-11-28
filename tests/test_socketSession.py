from abstract import TestCaseDB
from smm.models import *
import mongoengine
import time


class TestSocketSession(TestCaseDB):

    def testRemoveExpired(self):
        SocketSession.TTL = 1
        s = SocketSession()
        s.ip = "x1"
        s.keywords = []
        s.save()

        s = SocketSession()
        s.ip = "x2"
        s.keywords = []
        s.save()

        time.sleep(SocketSession.TTL/2.0)
        SocketSession.objects.first().ping()
        time.sleep(SocketSession.TTL/2.0)
        SocketSession.remove_expired()
        self.assertEquals(1, SocketSession.objects.count())


    def testKeywordsHash(self):
        s = SocketSession()
        s.ip = "x3"
        s.keywords = ['a','b']
        s.save()

        s = SocketSession()
        s.ip = "x3"
        s.keywords = ['c','d']
        s.save()

        self.assertEqual('61f728a510729c464bc80910333199ba7dabe92b', SocketSession.get_keywords_hash())


    def testKeywordsSet(self):
        s = SocketSession()
        s.ip = "x3"
        s.keywords = ['a','b']
        s.save()

        s = SocketSession()
        s.ip = "x3"
        s.keywords = ['a','c']
        s.save()
        expected = set([u'a', u'b', u'c'])

        self.assertEqual(expected, SocketSession.get_keywords())


    def tearDown(self):
        SocketSession.drop_collection()