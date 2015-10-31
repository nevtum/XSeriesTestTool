from datetime import datetime
from services import QueryEngine, DuplicateDatablockFilter
from PyQt4.QtCore import QObject, SIGNAL, Qt
from PyQt4 import QtSql, QtGui

class QtSQLWrapper(QObject):
    def __init__(self, filename, publisher, parent = None):
        QObject.__init__(self, parent)
        self.query_engine = self._create_query_engine(filename)
        self._build_view_tables()
        self.filter = DuplicateDatablockFilter()
        self.filter.filterduplicates(True)
        
        self.connect(publisher, SIGNAL("VALID_PACKET_RECEIVED"), self._on_valid_packet_received)
        self.connect(publisher, SIGNAL("INVALID_PACKET_RECEIVED"), self._on_invalid_packet_received)

    def _create_context(self, filename):
        context = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        context.setDatabaseName(filename)
        context.open()
        return context
        
    def _create_query_engine(self, filename):
        context = self._create_context(filename)
        query_engine = QueryEngine(context, self)
        query_engine.create_sql_tables()
        return query_engine

    def _build_view_tables(self):
        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable("distinctpackets")
        self.model.sort(0, Qt.DescendingOrder)
        self.proxy = QtGui.QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterKeyColumn(3)
        self.proxy.setDynamicSortFilter(True)

        self.sessionmodel = QtSql.QSqlRelationalTableModel(self)
        self.sessionmodel.setTable("session")
        self.sessionmodel.setRelation(1, QtSql.QSqlRelation("distinctpackets", "ID", "Class"))
        self.sessionmodel.sort(0, Qt.DescendingOrder)
        self.sessionproxy = QtGui.QSortFilterProxyModel()
        self.sessionproxy.setSourceModel(self.sessionmodel)
        self.sessionproxy.setFilterKeyColumn(1)
        self.sessionproxy.setDynamicSortFilter(True)

    def _add_record(self, direction, packet_type, byte_array):
        loggedtime = str(datetime.now())

        if self._has_changed_since_last_packet(packet_type, byte_array):
            self.query_engine.insert_changed_packet(direction, packet_type, byte_array, loggedtime)

        row_id = self.query_engine.get_row_id_of_latest_packet(packet_type)
        self.query_engine.insert_new_entry(row_id, loggedtime)
        self.emit(SIGNAL("newentry"))
        
    def _has_changed_since_last_packet(self, packet_type, byte_array):
        return self.filter.has_changed(packet_type, byte_array)
            
    def _on_invalid_packet_received(self, data):
        self._add_record("incoming", "unknown", data)
    
    def _on_valid_packet_received(self, packet_type, data):
        self._add_record("incoming", packet_type, data)

    def refresh(self):
        self.model.select()
        self.sessionmodel.select()

    def setAutoRefresh(self, toggle):
        if toggle == True:
            self.connect(self, SIGNAL("newentry"), self.refresh)
        else:
            self.disconnect(self, SIGNAL("newentry"), self.refresh)

    def getProxyModel(self):
        return self.proxy

    def getSessionProxy(self):
        return self.sessionproxy

    def clearDatabase(self):
        self.query_engine.clear_database()