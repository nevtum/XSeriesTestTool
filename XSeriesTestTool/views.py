import sqlite3
import debug
import utilities
from datetime import datetime
from PyQt4.QtCore import QObject, SIGNAL, Qt
from PyQt4 import QtSql, QtGui

class QtSQLWrapper(QObject):
    def __init__(self, filename, publisher, parent = None):
        QObject.__init__(self, parent)
        self._createSQLTables(filename)
        self._setupSourceModels()
        self._setupProxyModels()
        self.filter = DuplicateDatablockFilter()
        self.filter.filterduplicates(True)
        
        self.connect(publisher, SIGNAL("VALID_PACKET_RECEIVED"), self._on_valid_packet_received)
        self.connect(publisher, SIGNAL("INVALID_PACKET_RECEIVED"), self._on_invalid_packet_received)

    def _setupSourceModels(self):
        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable("distinctpackets")
        self.model.sort(0, Qt.DescendingOrder)

        self.sessionmodel = QtSql.QSqlRelationalTableModel(self)
        self.sessionmodel.setTable("session")
        self.sessionmodel.setRelation(1, QtSql.QSqlRelation("distinctpackets", "ID", "Class"))
        self.sessionmodel.sort(0, Qt.DescendingOrder)

    def _setupProxyModels(self):
        self.proxy = QtGui.QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterKeyColumn(3)
        self.proxy.setDynamicSortFilter(True)

        self.sessionproxy = QtGui.QSortFilterProxyModel()
        self.sessionproxy.setSourceModel(self.sessionmodel)
        self.sessionproxy.setFilterKeyColumn(1)
        self.sessionproxy.setDynamicSortFilter(True)

    def _createSQLTables(self, filename):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(filename)
        self.db.open()

        self.query = QtSql.QSqlQuery(self.db)
        sql = """CREATE TABLE IF NOT EXISTS session(
        Timestamp DATETIME,
        PacketID INTEGER NOT NULL)"""
        self.query.prepare(sql)
        self.query.exec_()
        sql = """CREATE TABLE IF NOT EXISTS distinctpackets(
        ID INTEGER PRIMARY KEY,
        LastChanged DATETIME,
        Direction TEXT NOT NULL,
        Class TEXT NOT NULL,
        Data TEXT NOT NULL)"""
        self.query.prepare(sql)
        self.query.exec_()
        self.query.finish()

    def _add_record(self, direction, packet_type, byte_array):
        loggedtime = str(datetime.now())

        if self._has_changed_since_last_packet(packet_type, byte_array):
            self._insert_changed_packet(direction, packet_type, byte_array, loggedtime)

        row_id = self._get_row_id_of_latest_packet(packet_type)
        self._insert_new_entry(row_id, loggedtime)
        self.emit(SIGNAL("newentry"))
        
    def _has_changed_since_last_packet(self, packet_type, byte_array):
        return self.filter.has_changed(packet_type, byte_array)
    
    def _insert_changed_packet(self, direction, packet_type, byte_array, logged_time):
        hexstring = utilities.convert_to_hex_string(byte_array)        
        
        self.query.prepare("INSERT INTO distinctpackets(LastChanged, Direction, Class, Data) VALUES(:date,:direction,:type,:contents)")
        self.query.bindValue(":date", logged_time)
        self.query.bindValue(":direction", str(direction))
        self.query.bindValue(":type", packet_type)
        self.query.bindValue(":contents", str(hexstring))
        self.query.exec_()
        self.query.finish()
        
    def _insert_new_entry(self, row_id, logged_time):
        self.query.prepare("INSERT INTO session(Timestamp, PacketID) VALUES(:date,:packetid)")
        self.query.bindValue(":date", logged_time)
        self.query.bindValue(":packetid", row_id)
        self.query.exec_()
        self.query.finish()
    
    def _get_row_id_of_latest_packet(self, packet_type):
        return self._get_last_packet(packet_type)[0]
    
    def _get_last_packet(self, packet_type):
        sql = """SELECT MAX(ID)
        FROM distinctpackets
        WHERE Class = '%s'
        AND Direction = 'incoming'""" % packet_type
        return self._runSelectQuery(sql)
    
    def _runSelectQuery(self, query):
        if self.query.isActive():
            debug.Log("Wrapper: previous query is still active")
            return []
        self.query.prepare(query)
        if self.query.exec_():
            list = []
            while self.query.next():
                list.append(str(self.query.value(0)))
            debug.Log("Wrapper: %i" % len(list))
            return list
        debug.Log("Wrapper: query did not execute successfully")
        return []
            
    def _on_invalid_packet_received(self, data):
        self._add_record("incoming", "unknown", data)
    
    def _on_valid_packet_received(self, packet_type, data):
        self._add_record("incoming", packet_type, data)

    def refresh(self):
        self.model.select()
        self.sessionmodel.select()
        #self.model.setQuery("SELECT * FROM packetlog ORDER BY timestamp DESC LIMIT 200")

    def setAutoRefresh(self, toggle):
        if toggle == True:
            self.connect(self, SIGNAL("newentry"), self.refresh)
        else:
            self.disconnect(self, SIGNAL("newentry"), self.refresh)

    #def filterduplicates(self, toggle):
    #    self.filter.filterduplicates(toggle)

    def getProxyModel(self):
        return self.proxy

    def getSessionProxy(self):
        return self.sessionproxy

    def clearDatabase(self):
        self.query.exec_("DELETE FROM session")
        self.query.exec_("DELETE FROM distinctpackets")
        self.query.finish()
        self.refresh()

    def __del__(self):
        self.db.close()

class DuplicateDatablockFilter:
    def __init__(self):
        self.dupes = {}
        self.filtered = False

    def filterduplicates(self, toggle):
        assert(isinstance(toggle, bool))
        self.filtered = toggle
        self.dupes.clear()
        debug.Log("DDFilter: Filtering enabled = %s" % toggle)

    def has_changed(self, blocktype, seq):
        if not self.filtered:
            return True

        key = blocktype
        data = self.dupes.get(key)
        if data is None:
            debug.Log("DDFilter: NEW DATABLOCK!")
            self.dupes[key] = seq
            return True

        assert(len(seq) == len(data))
        for i in range(len(seq)):
            if seq[i] != data[i]:
                self.dupes[key] = seq
                assert(seq == self.dupes.get(key))
                debug.Log("DDFilter: DIFFERENT DATABLOCK!")
                return True
        debug.Log("DDFilter: REPEATED!")
        return False
