__author__ = 'gx'
import twitter
import argparse
import sys
import time
from smm import models
from smm.classifier import emoticons
from smm import config
from smm.classifier.textprocessing import TwitterMixin

import logging

logger = logging.getLogger('collect-tweets')

parser = argparse.ArgumentParser(description='Collect tweets', usage='python collect-tweets.py happy 1000')
parser.add_argument('what', help='What to collect ( happy | sad )')
parser.add_argument('count', type=int, help='How much tweets to collect')
args = parser.parse_args()


#connect to db
models.connect()


class TwitterCollectorException(Exception):
    pass


class TwitterCollectorTimeoutException(Exception):
    pass


class TwitterCollector(object):
    def __init__(self, kw_track, polarity, total_target):
        self.kw_track = kw_track
        self.count = 0
        self.total_target = total_target
        self.polarity = polarity
        self.auth = twitter.OAuth(config.twitter_oauth_token, config.twitter_oauth_secret,
                                  config.twitter_oauth_custkey, config.twitter_oauth_custsecret)

    def run(self):
        while True:
            try:
                self.get_tweets()
            except twitter.TwitterHTTPError, e:
                logger.warn("%s - sleeping for %d sec", e.message, config.twitter_http_error_sleep)
                time.sleep(config.twitter_http_error_sleep)

            except TwitterCollectorException, e:
                logger.info(e.message)
                logger.info('Exit')
                sys.exit(0)

            except TwitterCollectorTimeoutException, e:
                logger.warn("%s - sleeping for %d sec", e.message, config.twitter_http_error_sleep)
                time.sleep(config.twitter_http_error_sleep)


    def get_tweets(self):
        logger.info('Connecting to twitter api')
        stream = twitter.TwitterStream(auth=self.auth, timeout=5)
        logger.info('Tracking: %s' % ",".join(self.kw_track))
        iterator = stream.statuses.filter(track=",".join(self.kw_track))

        for tweet in iterator:

            if tweet.get('timeout', False):
                raise TwitterCollectorTimeoutException('Timeout')

            if not self.is_tweet_valid(tweet):
                continue

            self.save(tweet)

            if self.count >= self.total_target:
                raise TwitterCollectorException('Done')

            if not self.count % 100:
                logger.info('Done with %d tweets out of %d' % (self.count, self.total_target))

    def save(self, tweet):

        row = models.TrainDataRaw()
        row.text = tweet['text']
        row.original = tweet
        row.polarity = self.polarity
        row.save()
        logger.debug('Tweet %s saved', row.id)
        self.count += 1


    def is_tweet_valid(self, tweet):

        if not tweet or 'delete' in tweet:
            logger.debug('Empty tweet - skipping')
            return False

        if not 'lang' in tweet or tweet['lang'] != 'en':
            logger.debug('Non EN - skipping')
            return False

        if not 'text' in tweet or tweet['text'].startswith('RT'):
            logger.debug('RE-Tweet found - skipping')
            return False

        folded_text = TwitterMixin.word_map(tweet['text']).split()
        if '__h__' in folded_text and '__s__' in folded_text:
            logger.debug('Tweet with double emoicons found - skipping')
            return False

        return True


polarity = {'sad': -1, 'happy': 1}.get(args.what)

try:
    c = TwitterCollector(getattr(emoticons, args.what), polarity, args.count)
    c.run()

except (KeyboardInterrupt, SystemExit):
    pass