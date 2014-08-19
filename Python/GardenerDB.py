from twisted.enterprise import adbapi
from twisted.internet import reactor
import os


class GardenerDB(object):
    def __init__(self,dbFile):
        if not os.path.exists(dbFile):
            # init new DB
            self.dbpool = adbapi.ConnectionPool("sqlite3", dbFile)
            self.dbpool.runOperation("CREATE TABLE garden(time INTEGER PRIMARY KEY, value REAL, stdDev REAL) IF NOT EXISTS", check_same_thread=False)
        else:
            self.dbpool = adbapi.ConnectionPool("sqlite3", dbFile)  
            self.dbpool.runOperation("CREATE TABLE garden(time INTEGER PRIMARY KEY, value REAL, stdDev REAL)", check_same_thread=False)                      
    def add(self,time, value=0.0, stdDev=0.0):
        return self.dbpool.runOperation("INSERT INTO garden(time, value,stdDev) VALUES(?,?,?)",(time, value,stdDev))
    def getLastValue(self):
        return self.dbpool.runQuery("SELECT value FROM garden ORDER BY time DESC LIMIT 1")

