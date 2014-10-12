from twisted.internet import reactor
from twisted.internet.serialport import SerialPort
from twisted.protocols import basic
from twisted.internet import task
import json
import datetime
import time
import sys
import cgi
from GardenerDB import GardenerDB

from twisted.web import server, resource
from twisted.internet import reactor, endpoints
comPort = "/dev/ttyACM0"
                
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

f = open("Password.txt")
PASSWORD= f.read()
f.close()



class ArduGardener(basic.LineReceiver):
    def __init__(self,storage):
        self.storage=storage
    def lineReceived(self, line):
        try:
            if (len(line)>0):
                recievedData = json.loads(line)
                recievedData["time"] = int(time.time())
                recievedData["value"] = int(recievedData["value"])
                self.storage._add(time=recievedData["time"],value=recievedData["value"])
        except Exception, e:
            print 'error', line, e
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
    def ret(self, result, request):
        value=''
        for rec in result:
            value += '['+str(rec[0]*1000)+','+str(rec[1])+'],'
        template = env.get_template('index.html')
        request.write(template.render(ListValues=value).encode())
        request.finish()        
    def render_GET(self, request):
        request.setHeader("content-type", "text/html")
        self.db.getLastValue(288).addCallback(self.ret,request)
        return server.NOT_DONE_YET

    def render_POST(self, request):
        passw = cgi.escape(request.args["pass"][0])
        request.setHeader("content-type", "text/html")
        print passw
        if passw == PASSWORD:
            self.gardener.requestPumping()
        self.db.getLastValue(288).addCallback(self.ret,request)
        return server.NOT_DONE_YET

if __name__ == '__main__':
    try:
        db = GardenerDB('test.sqlite')
        serial =ArduGardener(db)
        SerialPort(serial, comPort, reactor, baudrate='9600')
        #call class method with object as argument
        l = task.LoopingCall(ArduGardener.requestMeasurement,serial)
        l.start(300.0) # call every 5 minutes     
        endpoints.serverFromString(reactor, "tcp:9080").listen(server.Site(Counter(serial)))
        reactor.run()
    except Exception, e:
        print e
        reactor.stop()
        sys.exit(0)
