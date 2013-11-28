__author__ = 'gx'
import threading
import Queue


class WorkerPool(object):

    def __init__(self):
        self.terminate = threading.Event()
        self.keyword_hash = None
        self.pool = []
        self.workers = []
        self.fifo = Queue.Queue()
        self.keywords = []

    def start(self):
        self.start_pool()

        while True:
            self.process_queue()

            if self.keyword_change():
                self.restart_pool()

    def process_queue(self):
        task = self.fifo.get()
        task.task_done()

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