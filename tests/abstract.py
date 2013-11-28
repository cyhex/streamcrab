from unittest import TestCase
import mongoengine
from smm.config import test_mongo_db


class TestCaseDB(TestCase):

    def setUp(self):
        mongoengine.connect(**test_mongo_db)
