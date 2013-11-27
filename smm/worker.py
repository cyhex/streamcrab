__author__ = 'gx'
import threading
import time


class WorkerPool(object):

    pool = []
    workers = []
    terminate = None

    def __init__(self):
        self.terminate = threading.Event()
        self.keyword_hash = None

    def start(self):
        self.start_pool()

        while True:
            if self.keyword_change():
                self.restart_pool()
            else:
                time.sleep(1)


    def restart_pool(self):

        self.terminate.set()
        self.join_pool()
        self.keyword_hash = 'newHash'
        self.terminate.clear()
        self.start_pool()

    def join_pool(self):

        for w in self.pool:
            w.join()

    def start_pool(self):

        for w in self.workers:
            i = w(self.terminate)
            i.setDaemon(True)
            i.start()

    def keyword_change(self):
        return True