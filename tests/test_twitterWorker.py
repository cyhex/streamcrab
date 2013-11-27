from unittest import TestCase
from smm.lib.datastream.plugins.twitterworker import TwitterWorker

__author__ = 'gx'



class TestTwitterWorker(TestCase):
    def test_run(self):
        w = TwitterWorker()
        w.setDaemon(True)
        w.start()
        w.join()
