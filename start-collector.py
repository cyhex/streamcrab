__author__ = 'gx'
from smm.lib.datastream.workerPool import WorkerPool
from smm import models
import time

import logging

logger = logging.getLogger('start-collector')


#connect to db
models.connect()

s = models.SocketSession()
s.ip='x'
s.keywords = ['google']
s.save()

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