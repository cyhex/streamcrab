# -*- coding: utf-8 -*-
import nltk
from collections import defaultdict
import re
from tracker.lib import ngrams

class tokenizer(object):
    
    emos = {'##s##': [':)',':-)',';-)',': )',':d','=)',':p',';)','<3'],
             '##b##': [':(',':-(',': (']
            }
    
    re_username =  re.compile('@[a-z_]*',re.UNICODE)
    re_url = re.compile("https?://[a-z0-9/.#?=&+,@-_~]*")
    re_plain = re.compile('[^\w\s#]',re.UNICODE)
    re_hash = re.compile('#[\S]*',re.UNICODE)
    re_numbers = re.compile('[0-9]*',re.UNICODE)
    stemmer = {}
    synonym = {}
    stopwords = {}
    
    def __init__(self):
        self.stemmer['en'] = nltk.PorterStemmer()
        self.synonym['en'] = nltk.corpus.wordnet
        self.stopwords['en'] = set(nltk.corpus.stopwords.words('english'))
    
    def charFold(self,text):
        # filter out chars that repeat longer then 3 times in a row
        char_list = list(text)
        clean_list = []
        
        for i in range(len(char_list)):
            _c = char_list[i]
            if i > 0 and i < len(char_list)-1:
                if _c != char_list[i-1] or  _c != char_list[i+1]:
                    clean_list.append(_c)
            else:
                clean_list.append(_c)
        return "".join(clean_list)    

    
    def foldEmo(self,text):
        # convert :) to ### and :( to ***
        for label, items in self.emos.items():
            for item in items:
                text = text.replace(item," %s " % label)
         
        return text
    
    def removeUsernames(self,text):
        return self.re_username.sub('',text)
    
    def removeHash(self,text):
        return self.re_hash.sub('', text)
    
    def removeUrls(self,text):
        return self.re_url.sub(' ',text)
    
    def makePlain(self,text):
        return self.re_plain.sub(' ',text)
    
    def removeNumbers(self,text):
        return self.re_numbers.sub('',text)
    
    def cleanText(self,text):
        text = text.lower()
        text = self.removeUsernames(text)
        text = self.removeHash(text)
        text = self.charFold(text)
        text = self.foldEmo(text)
        text = self.removeUrls(text)
        text = self.removeNumbers(text)
        text = self.makePlain(text)
        return text.strip()
    
    
    def _specialProcessing(self,tokens,lang):
        
        tokens = set(tokens) - self.stopwords[lang] 
        p_tokens = []
        for t in tokens:
            try:
                t1 = self.synonym[lang].synsets(t)[0].lemma_names[0].lower()
            except:
                t1 = t
                
            p_tokens.append(self.stemmer[lang].stem(t1))
        
        return p_tokens
    
    def specialProcessing(self,tokens,lang):
        
        if lang == 'en':
            return self._specialProcessing(tokens,lang)
        else:
            return tokens
        
        
    
    
    def _tokenize(self,text):
        tokens = text.split()
        #for t in tokens[:]:
        #    if len(t) < 3:
        #        tokens.remove(t)
         
        return tokens
        
    
    def tokenize(self,text,lang=False,reduce=True,):

        if not isinstance(text,unicode):
            raise Exception('not unicode')
        
        text = unicode(text)
        if reduce:
            text = self.cleanText(text)
            
        tokens = self._tokenize(text)
        tokens = self.specialProcessing(tokens, lang)
        return tokens
       
  
  
class WordGramTokenizer(object):
    """
        makes binary grams out of words ('not bad','not good'...)
    """
    
    def __init__(self,n=2):
        self.tokenizer = tokenizer()
        self.n = n
        
    
    def tokenize(self,text,lang):
        grams = {}
        for gram in  ngrams.ngram(self.tokenizer.tokenize(text,lang,True), self.n):
            grams[gram] = 1 
        
        return grams
    
        
                    
                
  

class CharGramTokenizer(object):
    """
        makes grams out of word's chars
    """
    
    def __init__(self,n=3):
        self.tokenizer = tokenizer()
        self.n = n
    
    def tokenize(self,text):
        grams = defaultdict(int)
        for t in self.tokenizer.tokenize(text):
            if t:
                for gram in  ngrams.ngram(list(t), self.n):
                    grams[gram] += 1 
    
        
        return grams


#print WordGramTokenizer().tokenize(u'toyota kind-of +x is a bad car :) ******','en')


