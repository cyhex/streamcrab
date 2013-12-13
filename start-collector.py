__author__ = 'gx'
import time
import logging

from smm.datastream.workerPool import WorkerPool
from smm import models


logger = logging.getLogger('start-collector')


#connect to db
models.connect()

# init pool
pool = WorkerPool()

try:

    pool.start()
    logger.info("started WorkerPool with size %s", len(pool.pool))
    while True:
        time.sleep(60)
        logging.info('RawStreamQueue size: %s', models.RawStreamQueue.objects.count())

except (KeyboardInterrupt, SystemExit):
    pool.terminate()