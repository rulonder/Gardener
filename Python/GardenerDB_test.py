from GardenerDB import GardenerDB
from twisted.trial import unittest
from twisted.internet.defer import Deferred
from twisted.test import proto_helpers
import os
from time import sleep
class ArduGardenerTest(unittest.TestCase):
    def setUp(self):
        db = "test.db"
        if os.path.exists(db):
            os.remove(db)
        self.db = GardenerDB(db)
    def tearDown(self):
        self.db.shutdown()       
    def test_addValue(self):
        self.db.add(1000,2.3) 
        self.db.add(1010,2.4,4.9)
    def test_requestPump(self): 
        def test_value(result):
            self.assertEqual(result[0][1], 2.4)
        d = self.db.getLastValue()
        d.addCallback(test_value) 
        return d                