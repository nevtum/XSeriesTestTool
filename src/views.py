import sqlite3
from datetime import datetime
from debug import *
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4 import QtSql, QtGui

class QtSQLWrapper(QObject):
    def __init__(self, filename, parent = None):
        QObject.__init__(self, parent)
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(filename)
        self.db.open()

        self.model = QtSql.QSqlQueryModel(self)
        self.setupProxyModel()

    def setupProxyModel(self):
        self.proxy = QtGui.QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterKeyColumn(2)
        self.proxy.setDynamicSortFilter(True)
        
    def getProxyModel(self):
        return self.proxy
    
    def getSourceModel(self):
        return self.model
    
    def refresh(self):
        DBGLOG("Wrapper: Refreshing!!!")
        self.model.setQuery("SELECT * FROM packetlog ORDER BY timestamp DESC LIMIT 200")
    
    def clearDatabase(self):
        query = "DELETE FROM packetlog"
        q = QtSql.QSqlQuery(self.db)
        q.exec_(query)

    def __del__(self):
        self.db.close()

class Publisher:
    def __init__(self):
        self.subscribers = []
        self.packet = None

    def Attach(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)

    # this function is not currently in use.
    def Detach(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)

    def Record(self, packet):
            self.packet = packet
            DBGLOG("Publisher: publishing to views")
            self.Publish()

    def Publish(self):
        for subscriber in self.subscribers:
            subscriber.Update(self.packet)

class DuplicateDatablockFilter:
    def __init__(self):
        self.dupes = {}
        self.filterduplicates(False)

    def filterduplicates(self, toggle):
        assert(isinstance(toggle, bool))
        self.filtered = toggle
        DBGLOG("DDFilter: Filtering enabled = %s" % toggle)

    def differentToPrevious(self, blocktype, seq):
        if not self.filtered:
            return True

        key = blocktype
        data = self.dupes.get(key)
        if data is None:
            DBGLOG("DDFilter: NEW DATABLOCK!")
            self.dupes[key] = seq
            return True

        assert(len(seq) == len(data))
        for i in range(len(seq)):
            if seq[i] != data[i]:
                self.dupes[key] = seq
                assert(seq == self.dupes.get(key))
                DBGLOG("DDFilter: DIFFERENT DATABLOCK!")
                return True
        DBGLOG("DDFilter: REPEATED!")
        return False

class DataLogger(QObject):
    def __init__(self, filename, parent = None):
        QObject.__init__(self, parent)
        self.con = sqlite3.connect(filename)
        cursor = self.con.cursor()
        sql = """CREATE TABLE IF NOT EXISTS packetlog(
        timestamp DATETIME,
        direction TEXT NOT NULL,
        packetid TEXT NOT NULL,
        hex TEXT NOT NULL)"""
        self.dec = parent.getFactory().getProtocolDecoder()
        self.filter = DuplicateDatablockFilter()
        cursor.execute(sql)
        self.con.commit()
        self.duplicates = {}

    def Update(self, seq):
        # add proper code later
        meta = self.dec.getMetaData(seq)
        self.logData("incoming", meta.getPacketName(), seq)
        DBGLOG("Logger: emitting newentry signal")
        self.emit(SIGNAL("newentry"))

    def getDuplicateDatablockFilter(self):
        return self.filter

    def logData(self, direction, packetid, seq):
        assert(isinstance(seq, list))
        if not self.filter.differentToPrevious(packetid, seq):
            return
        data = ''.join(["%02X" % byte for byte in seq])
        if(direction not in ('incoming', 'outgoing')):
            raise ValueError()
        cursor = self.con.cursor()
        params = (str(datetime.now()), direction, packetid, data)
        sql = "INSERT INTO packetlog VALUES('%s','%s','%s','%s')" % params
        cursor.execute(sql)
        self.con.commit()

    def queryData(self, query):
        assert(isinstance(query, str))
        cursor = self.con.cursor()
        return cursor.execute(query)