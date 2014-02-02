from nltk import corpus
from nltk import PorterStemmer
from nltk import wordpunct_tokenize
from smm.classifier import emoticons
import re

stopwords = corpus.stopwords.words('english')


class SimpleProcessor():
    """
    Simple word tokenizer
    """

    @classmethod
    def clean(cls, text):
        text = text.replace(',', ' ')
        return text.strip().lower()

    @classmethod
    def getSearchTokens(cls, text):
        return text.split()

    @classmethod
    def getClassifierTokens(cls, text):
        return text.split()

    @classmethod
    def getFeatures(cls, text):
        return dict.fromkeys(cls.getClassifierTokens(text), 1)


class StopWordsMixin():
    @classmethod
    def remove_stop_words(self, tokens):
        for t in tokens[:]:
            if t in stopwords:
                tokens.remove(t)

        return tokens


class TwitterMixin(object):
    """
        Special case of Twitter cleanup
        Fold smilies to groups
        Fold not so it will not be removed by stop words
        Different Cleaners
    """
    _mapping = {
        '__h__': emoticons.happy,
        '__s__': emoticons.sad,
        '__not__': ['not']
    }

    re_username = re.compile('@[a-z_]*', re.UNICODE)
    re_url = re.compile("https?://[a-z0-9/.#?=&+,@-_~]*")
    re_plain = re.compile('[^\w\s#]', re.UNICODE)
    re_hash = re.compile('#[\S]*', re.UNICODE)
    re_numbers = re.compile('[0-9]*', re.UNICODE)


    @classmethod
    def remove_usernames(cls, text):
        return cls.re_username.sub('', text)

    @classmethod
    def remove_hashtags(cls, text):
        return cls.re_hash.sub('', text)

    @classmethod
    def remove_urls(cls, text):
        return cls.re_url.sub(' ', text)

    @classmethod
    def make_plain(cls, text):
        return cls.re_plain.sub(' ', text)

    @classmethod
    def remove_numbers(cls, text):
        return cls.re_numbers.sub('', text)

    @classmethod
    def char_fold(cls, text):
        """
        fold repeating chars more the n3 times chars looooool -> lool
        """
        char_list = list(text)
        clean_list = []

        for i in range(len(char_list)):
            _c = char_list[i]
            if i > 0 and i < len(char_list) - 1:
                if _c != char_list[i - 1] or _c != char_list[i + 1]:
                    clean_list.append(_c)
            else:
                clean_list.append(_c)
        return "".join(clean_list)

    @classmethod
    def word_map(cls, text):
        """
        map words in _mapping
        """
        for label, items in cls._mapping.items():
            for item in items:
                text = text.replace(item, " %s " % label)

        return text


class TwitterProcessor(SimpleProcessor, TwitterMixin, StopWordsMixin):
    """
    stop words, TwitterMixin
    """

    @classmethod
    def clean(cls, text):
        text = SimpleProcessor.clean(text)
        text = cls.char_fold(text)
        text = cls.word_map(text)
        return text.strip()

    @classmethod
    def getClassifierTokens(cls, text):
        text = cls.clean(text)
        text = cls.remove_urls(text)
        text = cls.remove_usernames(text)
        tokes = SimpleProcessor.getClassifierTokens(text)
        tokes = cls.remove_stop_words(tokes)
        tokes = cls.stemm(tokes)
        return tokes

    @classmethod
    def getSearchTokens(cls, text):
        text = cls.clean(text)
        tokes = wordpunct_tokenize(text)
        tokes = filter(lambda t: t.isalnum() or t in cls._mapping.keys(), tokes);
        tokes = cls.remove_stop_words(tokes)
        return tokes

    @classmethod
    def getFeatures(cls, text):
        return dict.fromkeys(cls.getClassifierTokens(text), 1)


    @classmethod
    def stemm(cls, tokens):
        stemmer = PorterStemmer()

        for i, t in enumerate(tokens):
            tokens[i] = stemmer.stem(t)

        return tokens
