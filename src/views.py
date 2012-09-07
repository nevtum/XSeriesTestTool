import sqlite3
from datetime import datetime
from debug import *
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4 import QtSql

class QtSQLWrapper(QObject):
    def __init__(self, filename, decoder, parent = None):
        QObject.__init__(self, parent)
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(filename)
        self.db.open()
        self.model = QtSql.QSqlQueryModel()
        self.dec = decoder

        # just a quick fix for now. used for pysqlite
        self.filename = filename
        self.sqlitedb = sqlite3.connect(self.filename)
        self.cur = self.sqlitedb.cursor()
    
    def getModel(self):
        return self.model
    
    def clearDatabase(self):
        query = "DELETE FROM packetlog"
        q = QtSql.QSqlQuery(self.db)
        q.exec_(query)
        self.db.clearDatabase()
    
    def getTimestamp(self, rowindex):
        record = self.model.record(rowindex)
        return record.value("timestamp").toString()

    def getDecodedData(self, rowindex):
        packet = self.getRawData2(rowindex)
        seq = [x for x in bytearray.fromhex(packet)]
        return self.dec.createXMLPacket(seq)
    
    def getRawData(self, rowindex):
        self.getRawData2(rowindex)
        assert(isinstance(rowindex, int))
        record = self.model.record(rowindex)
        return str(record.value("hex").toString())
    
    # just a quick fix for now
    def getRawData2(self, rowindex):
        time = self.getTimestamp(rowindex)
        sqlitedb = sqlite3.connect(self.filename)
        cur = sqlitedb.cursor()
        cur.execute("SELECT hex FROM packetlog WHERE timestamp = '%s'" % time)
        for next in cur:
            return next[0]
    
    def runQuery(self, querystring):
        self.cur.execute(querystring)
        return tuple(self.cur)

    def __del__(self):
        self.db.close()

class Publisher:
    def __init__(self):
        self.subscribers = []
        self.packet = None

    def Attach(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)

    # this function is not in use.
    def Detach(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)

    def Record(self, mq):
        while not mq.isEmpty():
            self.packet = mq.dequeue()
            DBGLOG("publishing to views")
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
        DBGLOG("Filtering enabled = %s" % toggle)

    def differentToPrevious(self, blocktype, seq):
        if not self.filtered:
            return True

        key = blocktype
        data = self.dupes.get(key)
        if data is None:
            DBGLOG("NEW DATABLOCK!")
            self.dupes[key] = seq
            return True

        assert(len(seq) == len(data))
        for i in range(len(seq)):
            if seq[i] != data[i]:
                self.dupes[key] = seq
                assert(seq == self.dupes.get(key))
                DBGLOG("DIFFERENT DATABLOCK!")
                return True
        DBGLOG("REPEATED!")
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
        self.dec = parent.factory.getProtocolDecoder()
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