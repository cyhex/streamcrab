import time
import threading

from abstract import TestCaseDB
from smm.datastream.plugins.twitterworker import TwitterWorker
from smm.models import RawStreamQueue, SocketSession


class TestTwitterWorker(TestCaseDB):

    def test_worker(self):
        """
        test single twitter worker
        """
        s = SocketSession(ip='x')
        s.keywords = ['google','bieber']
        s.save()
        kill = threading.Event()

        w = TwitterWorker(kill)
        w.setDaemon(True)
        w.start()

        while not RawStreamQueue.objects.count():
            time.sleep(0.1)

        kill.set()
        self.assertGreater(RawStreamQueue.objects.count(), 0)

    def tearDown(self):
        RawStreamQueue.drop_collection()
        SocketSession.drop_collection()