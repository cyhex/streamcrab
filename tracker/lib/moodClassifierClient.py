# -*- coding: utf-8 -*-
import cPickle
import socket
import math


class MoodClassifierTCPClient(object):
    """
        This is a tcp client for the classifier daemon, 
    """
    
    timeout = 120
    BUFSIZE = 1440
    recvData = []
    
    def __init__(self,host='127.0.0.1',port=6666):
        self.host = host
        self.port = port
        
    
    def _connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
    
    def _readResults(self):
        raw_data = ""
        dataLen = self.sock.recv(32)
        dataLen = int(dataLen)
        
        while True:
            raw_data += self.sock.recv(self.BUFSIZE)
            if len(raw_data) >= dataLen:
                break
        
        if raw_data:
            self.recvData = cPickle.loads(str(raw_data))

    def _send(self,data):
        data_to_send = cPickle.dumps(data, protocol=2)
        
        dataLen = "%032d" % len(data_to_send)
        self.sock.send(dataLen)
        self.sock.sendall(data_to_send)
    
    def _close(self):
        self.sock.close()
    
    def classify(self,data,search):
        """
            data = list of dicts - as it comes from twitter
            search = user search phrase
            Returns same list of dicts with x_mood and x_lang property added 
        """
        
        self._connect()
        self._send([search,data])
        self._readResults()
        self._close()
        return self.recvData
    




