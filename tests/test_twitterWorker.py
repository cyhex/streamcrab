from unittest import TestCase
from smm.lib.datastream.plugins.twitterworker import TwitterWorker
import Queue

__author__ = 'gx'



class TestTwitterWorker(TestCase):
    def test_run(self):
        q = Queue.Queue()
        w = TwitterWorker(q)
        w.setDaemon(True)
        w.start()
        w.join()
