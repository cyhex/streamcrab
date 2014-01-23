from nltk.tree import _child_names

__author__ = 'gx'

from multiprocessing import Process
import time

from smm.models import RawStreamQueue, ClassifiedStream
from smm import config
from smm.classifier import labels
import logging

class ClassifierWorker(Process):

    def __init__(self, classifier, queue, stop):
        self.classifier = classifier
        self.queue = queue
        self.stop = stop
        super(ClassifierWorker, self).__init__()
        self.logger = logging.getLogger(self.name)
        self.tokenizer = config.classifier_tokenizer

    def run(self):
        try:
            self._run()
        except (KeyboardInterrupt, SystemExit):
            self.logger.info('quiting')


    def _run(self):
        self.logger.info('Starting')

        while not self.stop.is_set():
            if not self.queue.empty():
                raw_data = self.queue.get()
                self.save(raw_data)
            else:
                time.sleep(0.2)

    def save(self, raw_data):
        assert isinstance(raw_data, RawStreamQueue)
        row = ClassifiedStream()
        row.source = raw_data.source
        row.original = raw_data.original
        row.text = raw_data.text
        row.tokens = list(self.tokenizer.getSearchTokens(row.text))
        row.polarity = self.get_classifications(row.text)
        row.save()
        self.logger.debug('ClassifiedStream saved %s', row.id)

    def get_classifications(self, text):
        features = config.classifier_tokenizer.getFeatures(text)

        prob = self.classifier.prob_classify(features)

        classified_label = self.classifier.classify(features)
        polarity = prob.prob(classified_label)

        if labels.negative == classified_label:
            polarity *= -1


        return polarity
