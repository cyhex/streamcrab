__author__ = 'gx'
import logging
import os
import smm
from smm.classifier.textprocessing import StopTwitterProcessor, StopPosTwitterProcessor

basepath =  os.path.realpath(os.path.join(os.path.dirname(smm.__file__),'..'))

# MongoDB
# ========

# live db
mongo_db = dict(db='smm', host='localhost', port=27017, is_slave=False, read_preference=False,
                slaves=None, username=None, password=None)


#test db
test_mongo_db = dict(db='smm_test', host='localhost', port=27017, is_slave=False, read_preference=False,
                     slaves=None, username=None, password=None)


# Classifiers
# =============

# default tokenizer
classifier="maxEnt_100000"
classifier_tokenizer = StopTwitterProcessor
classifier_pool_size = 4



# TWITTER DataStream Plugin
# =========================

# collector, twitter auth
twitter_oauth_token = ""
twitter_oauth_secret = ""
twitter_oauth_custkey = ""
twitter_oauth_custsecret = ""

#sleep for x seconds if twitter raises httpError exception
twitter_http_error_sleep = 10

#how often should we check for changed keywords
twitter_kw_interval_check = 10

# Server Flask & socketio
# =======================
server_templates = os.path.join(basepath, 'resources', 'templates')
server_static = os.path.join(basepath, 'resources', 'static')
server_debug = True

server_socketio_handlers = ['websocket', 'xhr-polling', 'xhr-multipart', 'jsonp-polling']


# Logging
# =======

logfile_path = os.path.join(basepath, 'smm.log')
# default logging to console
logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(levelname)s %(message)s')

# log INFO to file as well
filelog = logging.FileHandler(logfile_path, 'w')
filelog.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
filelog.setFormatter(formatter)
logging.getLogger('').addHandler(filelog)