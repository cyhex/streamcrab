from unittest import TestCase
import mongoengine
from smm.config import test_mongo_db
from smm import models

class TestCaseDB(TestCase):

    def setUp(self):
        models.connect(test_mongo_db)
