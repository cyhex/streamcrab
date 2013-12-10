__author__ = 'gx'
import time
import logging

from smm.classifier.pool import ClassifierWorkerPool
from smm import models

logger = logging.getLogger('start-classifier')

#connect to db
models.connect()

# init pool
pool = ClassifierWorkerPool()

try:

    pool.start()
    logger.info("started with size %s", len(pool.workers))
    while True:
        time.sleep(1)

except (KeyboardInterrupt, SystemExit):
    pool.terminate()