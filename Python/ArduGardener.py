from twisted.internet import reactor
from twisted.internet.serialport import SerialPort
from twisted.protocols import basic
from twisted.internet import task
import json
import datetime
import sys
import cgi

from twisted.web import server, resource
from twisted.internet import reactor, endpoints
comPort = "COM3"


class ArduGardener(basic.LineReceiver):
    def __init__(self,storage):
        self.storage=storage
    def lineReceived(self, line):
        try:
            recievedData = json.loads(line)
            recievedData["date"] = datetime.datetime.utcnow()
            self.storage.add(recievedData)
        except Exception, e:
            raise e("invalid string")
    def sendCommand(self, cmd):
        self.transport.write(cmd)
    def requestMeasurement(self):
        self.sendCommand("r")
    def requestPumping(self):
        self.sendCommand("p")

class Storage():
    db=[]
    def __init__(self):
        pass
    def add(self,data):
        print data
        self.db.append(data)
    def getLastValue(self):
        if len(self.db) > 0:
            return str(self.db[-1]["value"])
        else:
            return "None"

class Counter(resource.Resource):
    isLeaf = True
    numberRequests = 0
    def __init__(self,handler):
        self.db = handler.storage
        self.gardener = handler
    def render_GET(self, request):
        request.setHeader("content-type", "text/html")
        self.gardener.requestMeasurement()
        return """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
        Plant humidity is""" + (self.db.getLastValue())        +"""
 <FORM action="/" method="post">
    <P>
    Pass:<input type="text" name="pass">
    <INPUT type="submit" value="Water"> 
    </P>
 </FORM>
</body>
</html>
        """
    def render_POST(self, request):
        passw = cgi.escape(request.args["pass"][0])
        request.setHeader("content-type", "text/html")
        print passw
        if passw == "raulana":
            self.gardener.requestPumping()
        return """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
        Plant humidity is""" + (self.db.getLastValue())        +"""
 <FORM action="/" method="post">
    <P>
    Pass:<input type="text" name="pass">
    <INPUT type="submit" value="Water"> 
    </P>
 </FORM>
</body>
</html>
        """

if __name__ == '__main__':
    try:
        db = Storage()
        serial =ArduGardener(db)

        SerialPort(serial, 'COM3', reactor, baudrate='19200')
        l = task.LoopingCall(ArduGardener.requestMeasurement,serial)
        l.start(60.0) # call every second        
        endpoints.serverFromString(reactor, "tcp:8080").listen(server.Site(Counter(serial)))
        serial.sendCommand("r")
        reactor.run()
    except Exception, e:
        print e
        sys.exit(0)
