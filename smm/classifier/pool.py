__author__ = 'gx'

import time
from multiprocessing import Queue, Event, Process

from smm.classifier.worker import ClassifierWorker
from smm import config
from smm.models import RawStreamQueue, TrainedClassifiers

import logging


class QueueFeeder(Process):
    def __init__(self, queue, stop):
        self.queue = queue
        self.stop = stop
        super(QueueFeeder, self).__init__()
        self.logger = logging.getLogger(self.name)

    def run(self):
        try:
            self._run()
        except (KeyboardInterrupt, SystemExit):
            self.logger.info('quiting')

    def _run(self):
        self.logger.info('Starting')

        while not self.stop.is_set():

            if not RawStreamQueue.objects().count():
                time.sleep(0.5)
                continue

            raw_data = RawStreamQueue.objects().order_by('-id')[0:config.classifier_pool_size]
            for task in raw_data:
                self.queue.put(task)
                task.delete()


class ClassifierWorkerPool(object):
    def __init__(self):
        self.queue = Queue(100)
        self.workers = []
        self.stop = Event()
        self.stop.clear()
        self.queue_feeder = QueueFeeder(self.queue, self.stop)

        row = TrainedClassifiers.objects(name=config.classifier).first()

        if not row:
            raise Exception("Classifier %s does not exists" % config.classifier)

        self.trained_classifier = row.get_classifier()

    def start(self):
        self.queue_feeder.start()

        for i in range(0, config.classifier_pool_size):
            worker = ClassifierWorker(self.trained_classifier, self.queue, self.stop)
            worker.start()
            self.workers.append(worker)

    def terminate(self):
        self.stop.set()
        self.queue_feeder.join()
        for w in self.workers:
            w.join()