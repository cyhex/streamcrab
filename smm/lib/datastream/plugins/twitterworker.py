__author__ = 'gx'

import threading
import twitter
import time
from smm.models import RawStreamQueue, StreamSource, SocketSession
from smm import config


class TwitterWorker(threading.Thread):



    def __init__(self):
        threading.Thread.__init__(self)
        self.auth = twitter.OAuth(config.twitter_oauth_token, config.twitter_oauth_secret,
                                  config.twitter_oauth_custkey, config.twitter_oauth_custsecret)

        self.kw_track = SocketSession.get_keywords()
        self.kw_hash = SocketSession.get_keywords_hash()
        self.kw_int = 60 # seconds
        self.kw_last_check = time.time()


    def run(self):
        while True:
            self.get_tweets()


    def get_tweets(self):

        stream = twitter.TwitterStream(auth=self.auth)
        iter = stream.statuses.filter(track='google')
        for tweet in iter:

            if not self.is_tweet_valid(tweet):
                continue

            self.save(tweet)

            if self.check_keywords():
                return None



    def check_keywords(self):
        """
        check if twitter keywords are changed
        """
        if (time.time() - self.kw_last_check) > self.kw_int:
            kw_hash = SocketSession.get_keywords_hash()

            if self.kw_hash != kw_hash:
                self.kw_hash = kw_hash
                self.kw_track = SocketSession.get_keywords()
                return True

        return False


    def save(self, tweet):

        o = RawStreamQueue()
        o.original = tweet
        o.source = StreamSource.TWITTER
        o.text = tweet['text']
        o.save()


    def is_tweet_valid(self, tweet):
        if not tweet and tweet.has_key('delete') and tweet['lang'] != 'en' and not tweet.has_key('text'):
            return False
        else:
            return True
