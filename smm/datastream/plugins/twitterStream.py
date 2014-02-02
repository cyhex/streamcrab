__author__ = 'gx'
from smm import config
import requests
from requests_oauthlib import OAuth1


class TwitterStreamHttpException(Exception):
    def __init__(self, msg, status_code):
        self.status_code = status_code
        Exception.__init__(self, msg)


class TwitterStreamHandler(object):
    streamUri = 'https://stream.twitter.com/1.1/statuses/filter.json'

    def __init__(self, ):
        self.auth = None
        self.request = None

    def connect(self, keywords):
        if not len(keywords):
            raise TwitterStreamHttpException('HTTP code 406', status_code=406)

        self.auth = OAuth1(config.twitter_oauth_custkey, config.twitter_oauth_custsecret,
                           config.twitter_oauth_token, config.twitter_oauth_secret)

        self.request = requests.post(self.streamUri, data={'track': ",".join(keywords)}, stream=True, auth=self.auth)

        if self.request.status_code != 200:
            raise TwitterStreamHttpException('HTTP code %s' % self.request.status_code,
                                             status_code=self.request.status_code)

    def get_iter(self):
        return self.request.iter_lines()
