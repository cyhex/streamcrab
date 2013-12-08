__author__ = 'gx'
import threading
from smm.datastream.plugins.twitterworker import TwitterWorker

class WorkerPool(object):

    def __init__(self):
        self.kill = threading.Event()
        self.pool = []

    def start(self):
        twitter_worker = TwitterWorker(self.kill)
        twitter_worker.setDaemon(True)
        twitter_worker.start()
        self.pool.append(twitter_worker)

    def join(self, timeout=None):
        for w in self.pool:
            w.join(timeout)

    def terminate(self):
        self.kill.set()
