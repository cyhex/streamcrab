__author__ = 'gx'
import mongoengine
import datetime
import hashlib

class StreamSource(object):
    TWITTER = "twitter"


class RawStreamQueue(mongoengine.Document):

    text = mongoengine.StringField(required=True, max_length=1024)
    source = mongoengine.StringField(required=True)
    original = mongoengine.DictField()



class ClassifiedStream(mongoengine.Document):
    meta = {
        'indexes': ['tokens'],
    }

    text = mongoengine.StringField(required=True, max_length=1024)
    polarity = mongoengine.FloatField()
    tokens = mongoengine.ListField(mongoengine.StringField(max_length=64))
    source = mongoengine.StringField(required=True)
    original = mongoengine.DictField()


class SocketSession(mongoengine.Document):

    TTL = 30
    ip = mongoengine.StringField(required=True, max_length=45)
    keywords = mongoengine.ListField(mongoengine.StringField(max_length=64))
    ttl = mongoengine.DateTimeField(default=datetime.datetime.now)

    meta = {
        'indexes': ['ip', 'ttl'],
    }

    def ping(self):
        self.ttl = datetime.datetime.now()
        self.save()

    @classmethod
    def remove_expired(cls):
        d = datetime.datetime.now() - datetime.timedelta(seconds=cls.TTL)
        cls.objects(ttl__lte=d).delete()

    @classmethod
    def get_keywords(cls):
        cls.remove_expired()
        k = set()
        for s in cls.objects:
            k.update(set(s.keywords))

        return k
    @classmethod
    def get_keywords_hash(cls):
        k = str(cls.get_keywords())
        return hashlib.sha1(k).hexdigest()