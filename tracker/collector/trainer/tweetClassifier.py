import sys
sys.path.append('../../../')

import cPickle
import os
from dateutil import parser
import calendar
from tracker.lib.lang_detection import LangDetect
from tracker.lib.supportedLangs import supportedLangs
from tracker.lib.mood_detection import MoodDetectTrainData, MoodDetectTrainer, MoodDetect
import time
import re
import gzip
import sys
import multiprocessing



class RawClassifier(object):
    statsData = {}
    dataDir = "/home/gx/Sites/SMM/trunk/tracker/data"
    limit = {}
    skip = 0
    p2_f_limit = 0.75
    
    def __init__(self,traing_data_fileP1='mood_traing_p1.dat',traing_data_fileP2='mood_traing.dat',data_p_file='tweets_positive_raw.dat',data_n_file='tweets_negative_raw.dat'):
        
        self.clsP1 = MoodDetectTrainer(data_file = traing_data_fileP1)
        self.clsP2 = MoodDetectTrainer(data_file = traing_data_fileP2)
        
        self.langClassifier = LangDetect(supportedLangs)
        
        self.training_data_p1 = MoodDetectTrainData()
        self.training_data_p2 = MoodDetectTrainData()
        
        self.tweetsPFile = open(os.path.join( self.dataDir,data_p_file),'rb')
        self.tweetsNFile = open(os.path.join( self.dataDir,data_n_file),'rb')
        
        self.limit['en'] = 150000
        self.limit['default'] = 1000
        
    
    def classifyP1(self,stripSmiles=False):
        self.classifiyRaw(self.tweetsNFile,'n',stripSmiles)
        self.classifiyRaw(self.tweetsPFile,'p',stripSmiles)
        self.clsP1.train(self.training_data_p1)
        print "done training P1"
        
        print self.statsData
        
    def classifyP2(self):
        """
            remove noisy n-grams 
        """
        _st={'tf':0,'df':0}
        
        for feutures,label in self.training_data_p1:
            
            lang = feutures.pop('x_lang')
            feuturesP2 = feutures.copy()
            
            for f,v in feutures.items():
               prob = self.clsP1.classifier.prob_classify({f:v,'x_lang':lang}) 
               
               
               _st['tf']+=1
               
               if max(prob.prob('n'),prob.prob('p')) <= self.p2_f_limit:
                   del feuturesP2[f]
                   _st['df']+=1
            
            if len(feuturesP2) >= 3:
                feuturesP2['x_lang']=lang
                self.training_data_p2.append((feuturesP2,label))
            else:
                pass
            
        print len(self.training_data_p2), len(self.training_data_p1)  
        print _st
        
        print "deleting p1 set"
        del self.training_data_p1
        del self.clsP1
        print "Done deleting p1 set"
        self.clsP2.train(self.training_data_p2)
        
    
    def stripSmiles(self,text):
        emos = [':)',':-)',';-)',': )',':d','=)',':p',';)','<3',':(',':-(',': (']
        
        for item in emos:
            text = text.replace(item,"")
        return text         
    
    def stats(self,lang,mood):
        if not self.statsData.has_key(lang):
            self.statsData[lang] = {'n':0,'p':0}
        
        if self.limit.has_key(lang):
            limit = self.limit[lang]
        else:
            limit = self.limit['default']
            
              
        if self.statsData[lang][mood] >= limit:
                return 0
        else:
            self.statsData[lang][mood]+=1
            return 1
    
      
    def checkDoubleEmo(self,mood,text):
        if mood == 'n':
            if text.find(':)') != -1:
                return True
            else:
                return False
        
        if mood == 'p':
            if text.find(':(') != -1:
                return True
            else:
                return False
       
    
    
    
    def classifiyRaw(self,file,mood,stripSmiles):
        while True:
            try:
                tweet = cPickle.load(file)
            except EOFError:
                print "done for %s" % mood
                break
            except:
                pass
            
            if self.skip > 0:
                self.skip -= 1
                continue
            
            if tweet:
                text = unicode(tweet.get('text'))
                
                if text.lower().find('rt ') != -1:
                    continue
                
                if self.checkDoubleEmo(mood,text):
                    continue
                
                
                lang  = self.langClassifier.detect(text)
               
                if stripSmiles:
                    text = self.stripSmiles(text)
                
                sres = self.stats(lang[0], mood)
                if sres == 0:
                    continue
                
                if sres == -1:
                    print "done for %s" % mood
                    break
                
                self.training_data_p1.addRow(text, mood, lang[0])
            
    
    def countRows(self,file):
        rows = 0
        breakes = 0
        while True:
            try:
                tweet = cPickle.load(file)
                rows +=1
            except EOFError:
                break
            except:
                breakes +=1
            
        print file
        print rows,breakes
        
    
if __name__ == "__main__":
    
    cls = RawClassifier(traing_data_fileP1='mood_traing_p1.dat',
                        traing_data_fileP2='mood_traing_150k_1k_0.6.dat',
                        data_p_file='tweets_positive_raw.dat',
                        data_n_file='tweets_negative_raw.dat')
    # limit the number of tweets for en 
    cls.limit['en'] = 150000
    # default lang limit
    cls.limit['default'] = 1000
    # second filter threshold
    cls.p2_f_limit = 0.6
    # do not strip icons from trainging data
    cls.classifyP1(stripSmiles=False)
    cls.classifyP2()
    cls.clsP2.save()
    
    # train test data
    
    #cls = RawClassifier(traing_data_fileP1='mood_traing_test_50000.dat',traing_data_fileP2='mood_traing.dat',data_p_file='tweets_positive_raw.dat',data_n_file='tweets_negative_raw.dat')
    #cls.skip = 300000
    #cls.limit['en'] = 50000
    #cls.limit['deafult'] = 1000
    #cls.classifyP1(stripSmiles=True)
    #cls.clsP1.save()
    



