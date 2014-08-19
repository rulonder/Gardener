from ArduGardener import ArduGardener
from twisted.trial import unittest
from twisted.test import proto_helpers


class Storage():
    db=[]
    def __init__(self):
        pass
    def add(self,data):
        self.db.append(data)

class ArduGardenerTest(unittest.TestCase):
    def setUp(self):
        self.db = Storage()
        self.proto = ArduGardener(self.db)
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)
    def test_readValue(self):
        self.proto.requestMeasurement()
        self.assertEqual(self.tr.value(), "r")
        self.proto.lineReceived('{"value":%d,"error":null}' % (5))
        self.assertEqual(int(self.db.db[-1]["value"]), 5) 
        self.proto.lineReceived('{"value":%d,"error":null}' % (5))
        self.proto.lineReceived('{"value":%d,"error":null}' % (5))
        self.proto.lineReceived('{"value":%d,"error":null}' % (5)) 
        self.assertEqual(len(self.db.db), 4)        
    def test_requestPump(self):               
        self.proto.requestPumping()
        self.assertEqual(self.tr.value(), "p")               