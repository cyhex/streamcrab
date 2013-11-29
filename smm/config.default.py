__author__ = 'gx'
import logging

############## MONGODB #############
# live db
mongo_db = dict(db='smm', host='localhost', port=27017, is_slave=False, read_preference=False,
                slaves=None, username=None, password=None)


#test db
test_mongo_db = dict(db='smm_test', host='localhost', port=27017, is_slave=False, read_preference=False,
                     slaves=None, username=None, password=None)


############ TWITTER DataStream Plugin ############
# collector, twitter auth
twitter_oauth_token = ""
twitter_oauth_secret = ""
twitter_oauth_custkey = ""
twitter_oauth_custsecret = ""

#sleep for x seconds if twitter raises httpError exception
twitter_http_error_sleep = 10

#how offten should we check of changed keywords
twitter_kw_interval_check = 60


### Logging ###

# default logging to console
logging.basicConfig(level=logging.DEBUG, format='%(name)s: %(levelname)s %(message)s')

# log INFO to file as well
file = logging.FileHandler('smm.log', 'w')
file.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
file.setFormatter(formatter)
logging.getLogger('').addHandler(file)
