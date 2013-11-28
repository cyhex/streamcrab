
__author__ = 'gx'
from smm.lib.datastream.workerPool import WorkerPool
from smm import models
import time




#connect to db
models.connect()

# init pool
pool = WorkerPool()

try:
    pool.start()
    while True:
        # dont exit untill killed
        time.sleep(1)

except (KeyboardInterrupt, SystemExit):
    pool.terminate()