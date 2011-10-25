# -*- coding: utf-8 -*-
import tweetstream 
import time
import Queue
import threading
import cPickle
import os
import sys
from datetime import datetime



class streamCollector(threading.Thread):
    """ List of keywords to track"""
    trackingK = [':)']
    
    """ Limit (how many tweets should be received before quitting ) """
    limit = 1000000
    
    """ Twitter user/pass"""
    twitterUser = 'your_twitter_username'
    twitterPass = 'your_twitter_pass'
    
    def __init__(self,tweetsQ,stop_event):
        threading.Thread.__init__(self)
        self.q = tweetsQ
        self.stop_event = stop_event
        self.start_t = time.time()
        self.c = 0
        
    def collect(self):
        stream = tweetstream.TrackStream(self.twitterUser, self.twitterPass ,keywords=self.trackingK, url='https://stream.twitter.com/1/statuses/filter.json')  
        for tweet in stream:
            
            if self.c and self.c % 1000 == 0:
                print "done with %d tweets in %s" % (self.c,datetime.now())
                
                
            if self.c >= self.limit:
                raise Exception('done');
            
            try:
                self.q.put(tweet)
            except Exception, e:
                print e
            
            self.c += 1
     
    def run(self):
        while True:
            try:
                self.collect()
            except Exception, e:
                print e
                if self.c >= self.limit:
                    self.stop_event.set()
                    break
            
          


class streamWriter(threading.Thread):
    
    fileName = os.path.abspath(os.path.join( os.curdir,os.path.normpath('../../data/tweets_positive_raw.dat')))
    data = []
    
    def __init__(self,tweetsQ,stop_event):
        threading.Thread.__init__(self)
        self.stop_event = stop_event
        self.q = tweetsQ
        self.file = open(self.fileName,'ab')
        
    def run(self):
        c = 0
        while True:
            if self.stop_event.is_set():
                break;
            
            c += 1
            if self.q.qsize() == 0:
                time.sleep(1)
            
            tweet = self.q.get()
            self.q.task_done()
            cPickle.dump(tweet, self.file,protocol=2)
            
            

try:
    tweetsQ = Queue.Queue()   
    stop_event = threading.Event()
    
    c = streamCollector(tweetsQ,stop_event)
    c.daemon = True
    c.start()
    
    
    w = streamWriter(tweetsQ,stop_event)
    w.daemon = True
    w.start()
    
    while True:
        time.sleep(100)
    
except KeyboardInterrupt:
     print "Ctrl-c pressed ..."
     sys.exit(1)


                        
    
    
                
                
                            

    
    