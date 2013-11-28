__author__ = 'gx'




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



