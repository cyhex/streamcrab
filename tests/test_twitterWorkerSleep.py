import threading
import time

from abstract import TestCaseDB
from smm.datastream.plugins.twitterworker import TwitterWorker
from smm.models import RawStreamQueue, SocketSession

__author__ = 'gx'

class TestTwitterWorker(TestCaseDB):

    def test_workerSleep(self):
        """
        twitter collector should sleep if not keywords found
        """
        RawStreamQueue.drop_collection()
        SocketSession.drop_collection()
        kill = threading.Event()

        self.assertEqual(len(SocketSession.get_keywords()),0)
        w = TwitterWorker(kill)
        w.setDaemon(True)
        w.start()
        time.sleep(1)
        kill.set()
        self.assertEqual(RawStreamQueue.objects.count(), 0)


    def tearDown(self):
        RawStreamQueue.drop_collection()
        SocketSession.drop_collection()
