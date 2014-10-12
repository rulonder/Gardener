from twisted.enterprise import adbapi
from twisted.internet import reactor
import os
import random


class GardenerDB(object):
    def __init__(self,dbfile='test.sqlite', tableName= "garden"):
        self.addPool=[]
        self.initiated = False        
        self.db = adbapi.ConnectionPool("sqlite3", dbfile, check_same_thread=False)
        self.db.runOperation("CREATE TABLE IF NOT EXISTS {tableName}(time INTEGER PRIMARY KEY, value REAL, stdDev REAL) ".format(tableName=tableName)).addCallback(self._addPending)
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
            self.add(addValues)
    def add(self,*args):
        if self.initiated:
            self._add(args)
        else:
            self.addPool.append([args])
#        ret_render = lambda self,args: GardenerDB._add(self,args)
#        self.deferred.addCallback(ret_render)
    def _add(self,time, value=0.0, stdDev=0.0):
        return self.db.runOperation("INSERT INTO garden(time, value,stdDev) VALUES(?,?,?)",(time, value,stdDev))
    def getLastValue(self, number=10):
        return self.db.runQuery("SELECT time,value FROM garden ORDER BY time DESC LIMIT {0}".format(number)) 


def printResult(data):
    if data:
        print(data)
    else:
        print 'Nothing'

if __name__ == '__main__' :
    g = GardenerDB('test.sqlite')
    g._add(random.randint(1,1200),323.32,323.3)
    g._add(random.randint(1,1200),212.2,1.2)
    g.getLastValue().addCallback(printResult)
    reactor.run()