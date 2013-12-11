import time

from abstract import TestCaseDB
from smm.datastream.workerPool import WorkerPool
from smm.models import RawStreamQueue, SocketSession


class TestWorkerPool(TestCaseDB):

    def test_start(self):
        """
        test datastream worker pool
        """
        s = SocketSession(ip='x')
        s.keywords = ['google', 'bieber']
        s.save()

        w = WorkerPool()
        w.start()
        while not RawStreamQueue.objects.count():
            time.sleep(0.1)

        w.terminate()

        self.assertGreater(RawStreamQueue.objects.count(), 0)

    def tearDown(self):
        RawStreamQueue.drop_collection()
        SocketSession.drop_collection()