from twisted.enterprise import adbapi
from twisted.internet import reactor
import os
import random


class GardenerDB(object):
    def __init__(self,dbfile='test.sqlite'):
        self.addPool=[]
        self.db = adbapi.ConnectionPool("sqlite3", dbfile, check_same_thread=False)
        self.deferred = self.db.runOperation("CREATE TABLE IF NOT EXISTS garden(time INTEGER PRIMARY KEY, value REAL, stdDev REAL) ")
    def shutdown(self):
        """
            Shutdown function
            It's a required task to shutdown the database connection pool:
                garbage collector doesn't shutdown associated thread
        """
        self.db.close()        
    def _addPending(self,*args):
        self.initiated = True
        for addValues in self.addPool:
            seld.add(addValues)
    def add(self,*args):
        if self.initiated:
            self._add(args)
        else:
            self.addPool.append([args])
    def _add(self,time, value=0.0, stdDev=0.0):
        return self.db.runOperation("INSERT INTO garden(time, value,stdDev) VALUES(?,?,?)",(time, value,stdDev))
    def getLastValue(self):
        if self.initiated:
            return self.db.runQuery("SELECT time,value FROM garden ORDER BY time DESC LIMIT 10")
        else:




def printResult(data):
    if data:
        print(data)
    else:
        print 'Nothing'

if __name__ == '__main__' :
    g = GardenerDB('test.sqlite')
    g.add(random.randint(1,1200),323.32,323.3).addErrback(printResult)
    g.add(random.randint(1,1200),212.2,1.2).addErrback(printResult)
    g.getLastValue().addCallback(printResult)
    g.shutdown()
    reactor.run()