__author__ = 'gx'
import mongoengine


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

