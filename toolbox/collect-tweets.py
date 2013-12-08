__author__ = 'gx'
from smm import models
from smm.classifier import emoticons
import twitter
import argparse


import logging
logger = logging.getLogger('collect-tweets')


parser = argparse.ArgumentParser(description='Collect tweets', usage='python collect-tweets.py happy 1000')
parser.add_argument('what', help='What to collect ( happy | sad )')
parser.add_argument('count', type=int, help='How much tweets to collect')
args = parser.parse_args()



#connect to db
models.connect()


class TwitterCollector(object):

    def __init__(self, kw_track, total_target):
        self.kw_track = kw_track
        self.count = 0
        self.total_target = total_target

    def run(self):
        while True:
            try:
                self.get_tweets()
            except twitter.TwitterHTTPError, e:
                logger.info(e.message)

    def get_tweets(self):
        logger.info('Connecting to twitter api')
        stream = twitter.TwitterStream(auth=self.auth)
        logger.info('Tracking: %s' % ",".join(self.kw_track))
        iterator = stream.statuses.filter(track=",".join(self.kw_track))

        for tweet in iterator:
            if not self.is_tweet_valid(tweet):
                continue

            row = models.TrainDataRaw()
            row.text = tweet['text']
            row.original = tweet
            row.save()
            self.count += 1

            if not self.count % 100:
                logger.info('Done with %d tweets out of %d' % (self.count, self.total_target))

    def is_tweet_valid(self, tweet):
        if tweet and not 'delete' in tweet and 'lang' in tweet and tweet['lang'] == 'en' \
            and 'text' in tweet and not tweet['text'].startswith('RE'):

            return True
        else:
            return False


try:

    c = TwitterCollector(getattr(emoticons, args.what), args.count)
    c.run()

except (KeyboardInterrupt, SystemExit):
    pass