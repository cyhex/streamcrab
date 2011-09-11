# -*- coding: utf-8 -*-


import ngrams
from tokenizer import CharGramTokenizer
from nltk.probability import FreqDist
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader.api import CorpusReader
from nltk.corpus.reader.util import StreamBackedCorpusView, concat

class LangIdCorpusReader(CorpusReader):
    '''
    LangID corpus reader
    '''
    
    CorpusView = StreamBackedCorpusView

    def _get_trigram_weight(self, line):
        '''
        Split a line in a trigram and its frequency count
        '''
        data = line.strip().split(' ')
        if len(data) == 2:
            return (unicode(data[1],'utf-8'), int(data[0]))
        
            

    def _read_trigram_block(self, stream):
        '''
        Read a block of trigram frequencies
        '''
        freqs = []
        for i in range(20): # Read 20 lines at a time.
            freqs.append(self._get_trigram_weight(stream.readline()))
        return filter(lambda x: x != None, freqs)

    def freqs(self, fileids=None):
        '''
        Return trigram frequencies for a language from the corpus        
        '''
        return concat([self.CorpusView(path, self._read_trigram_block) 
                       for path in self.abspaths(fileids=fileids)])
        
        
    
class LangDetect(object):
    language_trigrams = {}
    langid            = LazyCorpusLoader('langid', LangIdCorpusReader, r'(?!\.).*\.txt',encoding='utf-8')
    tk = CharGramTokenizer()
    
    def __init__(self, languages):
        for lang in languages:
            self.language_trigrams[lang] = FreqDist()
            for f in self.langid.freqs(fileids=lang+"-3grams.txt"):
                self.language_trigrams[lang].inc(f[0], f[1])

    def detect(self, text):
        '''
        Detect the text's language
        '''
        if not isinstance(text,unicode):
            raise Exception('not unicode')
        
        trigrams = self.tk.tokenize(text)

        scores   = dict([(lang, 0) for lang in self.language_trigrams.keys()])
        total = sum(trigrams.values())
        
        for trigram, count in trigrams.items():
            for lang, frequencies in self.language_trigrams.items():
                # normalize and add to the total score
                scores[lang] += (float(frequencies[trigram]) / float(frequencies.N())) * (float(count) / float(total))
        best_match = sorted(scores.items(), key=lambda x: x[1], reverse=True)[0]
        if best_match[1] == 0:
            return ('other',0)
        else:
            return best_match




