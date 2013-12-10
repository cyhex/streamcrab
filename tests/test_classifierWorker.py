from multiprocessing import Queue, Event
import time
from abstract import TestCaseDB
from smm.models import RawStreamQueue, ClassifiedStream
from smm.classifier.worker import ClassifierWorker
import nltk

class TestClassifierWorker(TestCaseDB):


    def setUp(self):
        super(TestClassifierWorker, self).setUp()
        self.cls = nltk.NaiveBayesClassifier.train([({'a':'a', 'b':'b'}, 'positive')])
        self.data = []
        for i in range(5):
            d = RawStreamQueue()
            d.source = 'test'
            d.original = {}
            d.text = "this is a test"
            self.data.append(d)
        ClassifiedStream.drop_collection()



    def test_worker(self):
        queue = Queue(100)
        stop = Event()
        stop.clear()
        w = ClassifierWorker(self.cls, queue, stop)
        w.start()

        for d in self.data:
            queue.put(d)

        while not queue.empty():
            time.sleep(0.1)

        time.sleep(0.5)
        stop.set()
        w.join()

        self.assertEqual(ClassifiedStream.objects.count(), 5)



    def tearDown(self):
        ClassifiedStream.drop_collection()
        RawStreamQueue.drop_collection()