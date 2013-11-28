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
        self.kw_int = config.twitter_kw_interval_check
        self.kw_last_check = time.time()

    def run(self):
        while True:
            try:
                self.get_tweets()
            except twitter.TwitterHTTPError:
                time.sleep(config.twitter_http_error_sleep)


    def get_tweets(self):

        if not self.kw_track:
            raise twitter.TwitterHTTPError('kw empty')

        stream = twitter.TwitterStream(auth=self.auth)
        iterator = stream.statuses.filter(track=",".join(self.kw_track))

        for tweet in iterator:
            if not self.is_tweet_valid(tweet):
                continue

            self.check_keywords()
            self.save(tweet)




    def check_keywords(self):
        """
        check if twitter keywords are changed
        """


        if (time.time() - self.kw_last_check) > self.kw_int:
            kw_hash = SocketSession.get_keywords_hash()

            if self.kw_hash != kw_hash:
                self.kw_hash = kw_hash
                self.kw_track = SocketSession.get_keywords()
                raise twitter.TwitterHTTPError('kw change')



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
