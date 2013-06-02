# -*- coding: utf-8 -*-
import sys
sys.path.append('../../')
from tracker.lib.moodClassifierClient import MoodClassifierTCPClient


MCC = MoodClassifierTCPClient('127.0.0.1',6666)

test_data  = [
    {'text':u'this is a test text 1'},
    {'text':u'this is a test text 2'},
]

print MCC.classify(test_data, 'search')
