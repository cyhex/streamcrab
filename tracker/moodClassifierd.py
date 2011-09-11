#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import sys
sys.path.append('../')

from tracker.lib.mood_detection import MoodDetect, MoodDetectTrainer
from tracker.lib.lang_detection import LangDetect
from tracker.lib.supportedLangs import supportedLangs
from tracker.lib.daemon import Daemon

import socket
import threading
import SocketServer
import math
import os
import cPickle

HOST, PORT = "", 6666


class TCPRequestHandler(SocketServer.BaseRequestHandler):
    
    BUFSIZE = 1440
    
    def _send(self,data_to_send):
        
        data = cPickle.dumps(data_to_send, protocol=2)
        dataLen = "%032d" % len(data)
        self.request.send(dataLen)
        self.request.sendall(data)
        
    
    def handle(self):
        dataLen = int(self.request.recv(32))
        
        raw_data = ""
        
        while True:
            raw_data += self.request.recv(self.BUFSIZE)
            if len(raw_data) >= dataLen:
                break
            
        
        if raw_data:
            searchPhrase, recvData = cPickle.loads(str(raw_data))
        
        
        self.server.moodCls.setUpSearchPhraseCleaner(searchPhrase)
           
        try:
        
            data_to_send = []
            for r in recvData:
                text = r.get('text')
                r['x_lang'] = self.server.langCls.detect(text)[0]
                r['x_mood'] = self.server.moodCls.classify(text,r['x_lang'] )
                data_to_send.append(r)
        except Exception,e:
            raise e
            return False
            
        self._send(data_to_send)
            


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    allow_reuse_address = True
    max_children = 40
    timeout = 300
    
    @staticmethod
    def loadCls():
        ThreadedTCPServer.langCls = LangDetect(supportedLangs)
        ThreadedTCPServer.moodCls = MoodDetect(MoodDetectTrainer())


class serverDaemon(Daemon):
    def run(self):
        searchserver = ThreadedTCPServer((HOST, PORT), TCPRequestHandler)
        try:
            searchserver.serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)
        




if __name__ == "__main__":
    PID = os.path.join(os.getcwd(),'moodClassifierd.pid')
    stdout = os.path.join(os.getcwd(),'moodClassifierd.log')
    stderr = os.path.join(os.getcwd(),'moodClassifierd.log')
    
    daemon = serverDaemon(pidfile=PID,stderr=stderr,stdout=stdout)
    
    
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print 'starting...'
            ThreadedTCPServer.loadCls()
            print 'OK'
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.stop()
            time.sleep(2)
            daemon.start()
        elif 'debug' == sys.argv[1]:
            print 'starting debug mode...'
            ThreadedTCPServer.loadCls()
            print 'OK'
            
            
            searchserver = ThreadedTCPServer((HOST, PORT), TCPRequestHandler)
            try:
                searchserver.serve_forever()
            except KeyboardInterrupt:
                sys.exit(0)
            
        else:
            print "Unknown command"
            sys.exit(2)
            sys.exit(0)
            
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)


