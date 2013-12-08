__author__ = 'gx'
import threading

class DataStreamAbstract(threading.Thread):

    def __init__(self, terminate):
        event_class = getattr(threading, '_Event', threading.Event)
        assert isinstance(terminate, event_class)
        self.terminate = terminate
        threading.Thread.__init__(self)