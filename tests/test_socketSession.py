from abstract import TestCaseDB
from smm.models import *
import mongoengine
import time


class TestSocketSession(TestCaseDB):

    def testRemoveExpired(self):
        SocketSession.TTL = 1
        mongoengine.connect('test')
        SocketSession.drop_collection()
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
        SocketSession.drop_collection()


    def testKeywords(self):
        s = SocketSession()
        s.ip = "x3"
        s.keywords = ['a','b']
        s.save()

        s = SocketSession()
        s.ip = "x3"
        s.keywords = ['c','d']
        s.save()
        expected = set([u'a', u'c', u'b', u'd'])

        self.assertEqual(expected, SocketSession.get_keywords())
        self.assertEqual('61f728a510729c464bc80910333199ba7dabe92b', SocketSession.get_keywords_hash())

        s = SocketSession.objects.first()
        s.keywords = []
        s.save()

        self.assertNotEqual(expected, SocketSession.get_keywords())
        self.assertNotEqual('61f728a510729c464bc80910333199ba7dabe92b', SocketSession.get_keywords_hash())


    def tearDown(self):
        SocketSession.drop_collection()
