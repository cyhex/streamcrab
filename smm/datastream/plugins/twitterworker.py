__author__ = 'gx'

import time
import logging

import twitter

from smm.datastream.plugins.abstract import DataStreamAbstract
from smm.models import RawStreamQueue, StreamSource, SocketSession
from smm import config

logger = logging.getLogger('TwitterWorker')


class TwitterWorkerKwChange(Exception):
    pass

class TwitterWorkerKwEmpty(Exception):
    pass

class TwitterWorkerTerminate(Exception):
    pass


class TwitterWorkerTimeout(Exception):
    pass

class TwitterWorker(DataStreamAbstract):
    def __init__(self, terminate):
        DataStreamAbstract.__init__(self, terminate)

        self.auth = twitter.OAuth(config.twitter_oauth_token, config.twitter_oauth_secret,
                                  config.twitter_oauth_custkey, config.twitter_oauth_custsecret)

        self.kw_track = SocketSession.get_keywords()
        self.kw_hash = SocketSession.get_keywords_hash()
        self.kw_int = config.twitter_kw_interval_check
        self.kw_last_check = time.time()

    def run(self):
        logger.info("started %s", self.getName())
        while True:
            if self.terminate.isSet():
                logger.info("Terminated")
                return None

            try:
                self.get_tweets()

            except TwitterWorkerKwChange, e:
                logger.info(e.message)

            except TwitterWorkerKwEmpty, e:
                sleep_int = config.twitter_kw_interval_check/2
                logger.warn("%s - sleeping for %d sec", e.message,sleep_int)
                time.sleep(sleep_int)

            except twitter.TwitterHTTPError, e:
                logger.warn("%s - sleeping for %d sec", e.message, config.twitter_http_error_sleep)
                time.sleep(config.twitter_http_error_sleep)

            except TwitterWorkerTimeout, e:
                logger.warn("%s - sleeping for %d sec", e.message, config.twitter_http_error_sleep)
                time.sleep(config.twitter_http_error_sleep)

            except TwitterWorkerTerminate:
                logger.info("Terminated")
                return None

    def get_tweets(self):

        if not self.kw_track:
            raise TwitterWorkerKwEmpty('keywords are empty')

        stream = twitter.TwitterStream(auth=self.auth, timeout=5)
        iterator = stream.statuses.filter(track=",".join(self.kw_track))

        for tweet in iterator:

            if self.terminate.isSet():
                raise TwitterWorkerTerminate()

            if tweet.get('timeout',False):
                raise TwitterWorkerTimeout('Timeout')

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
                raise TwitterWorkerKwChange('keywords change detected')


    def save(self, tweet):
        if self.is_tweet_valid(tweet):
            o = RawStreamQueue()
            o.original = tweet
            o.source = StreamSource.TWITTER
            o.text = tweet['text']
            o.save()
            logger.debug("RawStreamQueue saved with id %s", o.id)

    def is_tweet_valid(self, tweet):
        if tweet and not 'delete' in tweet and 'lang' in tweet and tweet['lang'] == 'en' and 'text' in tweet:
            return True
        else:
            return False
