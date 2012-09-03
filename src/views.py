import sqlite3
from datetime import datetime
from debug import *

class Publisher:
    def __init__(self):
        self.subscribers = []
        self.packet = None

    def Attach(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)

    def Detach(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(x)

    def Record(self, seq):
        self.packet = seq
        DBGLOG("publishing to views")
        self.Publish()
    
    def Publish(self):
        if len(self.subscribers) > 0:
            for subscriber in self.subscribers:
                subscriber.Update(self.packet)

class Subscriber:
    def __init__(self, publisher):
        assert(isinstance(publisher, Publisher))
        self.publisher = publisher
        self.publisher.Attach(self)

    def __del__(self):
        self.publisher.Detach(self)

    def Update(self, seq):
        raise RuntimeError('Abstract method, must be overloaded!')

class DuplicateDatablockFilter(Subscriber):
    def __init__(self, publisher):
        publisher.Attach(self) # hmmmmm... need to work on
        self.dupes = {}
        self.filterduplicates(False)

    def Update(self, seq):
        # add proper code later
        DBGLOG("Confirmed working: %s" % str(seq))

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

class DataLogger:
    def __init__(self, filename):
        self.con = sqlite3.connect(filename)
        cursor = self.con.cursor()
        sql = """CREATE TABLE IF NOT EXISTS packetlog(
        timestamp DATETIME,
        direction TEXT NOT NULL,
        packetid TEXT NOT NULL,
        hex TEXT NOT NULL)"""
        cursor.execute(sql)
        self.con.commit()
        self.duplicates = {}

    def logData(self, direction, packetid, seq):
        assert(isinstance(seq, list))
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