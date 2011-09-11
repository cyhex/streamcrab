# -*- coding: utf-8 -*-
import sys
sys.path.append('../../')
import socket
import os
from tracker.lib.moodClassifierClient import MoodClassifierTCPClient
from tracker.lib.lang_detection import LangDetect
from tracker.lib.supportedLangs import supportedLangs
import cPickle
import linecache


#MCC = MoodClassifierTCPClient('srv1.cyhex.com',6666)
MCC = MoodClassifierTCPClient('127.0.0.1',6666)

cls_data = {'nc':1,'pc':1,'n':1,'p':1,'n#':1,'p#':1}

langClassifier = LangDetect(supportedLangs)

tweetsPFile = "/home/gx/Sites/SMM/trunk/tracker/data/tweets_positive_test.dat"
tweetsNFile = "/home/gx/Sites/SMM/trunk/tracker/data/tweets_negative_test.dat"

def stripSmiles(text):
        emos = [':)',':-)',';-)',': )',':d','=)',':p',';)','<3',':(',':-(',': (']
        
        for item in emos:
            text = text.replace(item,"")
        return text 


def classify(file,m):
        #lines to sckip
        skip = 0
        line = 0
        c = 0
        while True:
            
            if c > 100000:
                break
            
            text = linecache.getline(file, skip + line)
            
            line +=1
            if not text:
                break
            
            
            if text:
                try:
                    tweets = [{'text':unicode(text)},
                              {'text':unicode(stripSmiles(text))}
                              ]
                except:
                    continue
                    
                tweet =  MCC.classify(tweets,'xxxxx')
                if tweet[0]['x_lang']=='en':
                    
                    c += 1
                    
                    if m =='p':
                        cls_data['pc'] +=1
                        if tweet[0]['x_mood'] > 0:
                            cls_data['p#'] +=1
                            
                        if tweet[1]['x_mood'] > 0:
                            cls_data['p'] +=1
                            
                    if m =='n':
                         cls_data['nc'] +=1
                         
                         if tweet[0]['x_mood'] < 0:
                            cls_data['n#'] +=1
                        
                         if tweet[1]['x_mood'] < 0:
                            cls_data['n'] +=1
            
            
            if c % 1000 == 0:
                printStats()
                
                    
                        


                  



def rewriteData(f,t):
        c = 0
        while True:
            try:
                tweet = cPickle.load(f)
            except EOFError:
                break
            except:
                pass
            
            if tweet and tweet.get('text'):
                tweet['text'] = unicode(tweet.get('text').strip('\r').strip('\n'))
             
                t.write(tweet['text'] + '\n')




def printStats(x=False):

    print "p w/o icons: %f%%" % ((cls_data['p']/float(cls_data['pc']))*100 )
    print "p with icons: %f%%" % ((cls_data['p#']/float(cls_data['pc']))*100 )
    print "n w/o icons: %f%%" % ((cls_data['n']/float(cls_data['nc']))*100 )
    print "n# with icons: %f%%" % ((cls_data['n#']/float(cls_data['nc']))*100 )
    print "avg w/o icons: %f%%" % ((((cls_data['n']/float(cls_data['nc'])) + (cls_data['p']/float(cls_data['pc'])) )/2)  *100 )
    print "avg# with icons: %f%%" % ((((cls_data['n#']/float(cls_data['nc'])) + (cls_data['p#']/float(cls_data['pc'])) )/2)  *100 )
    print cls_data



classify(tweetsPFile,'p')
classify(tweetsNFile,'n')



