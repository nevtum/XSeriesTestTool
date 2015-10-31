from services import QueryEngine, DuplicateDatablockFilter
from PyQt4.QtCore import QObject, SIGNAL, Qt
from PyQt4 import QtSql, QtGui

class DataViewManager(QObject):
    def __init__(self, filename, publisher, parent = None):
        QObject.__init__(self, parent)
        self.query_engine = QueryEngine(filename, self)
        self.distinct_table_view_model = ModifiedPacketTableModel(self)
        self.session_table_view_model = AnyPacketTableModel(self)
        self.is_autorefresh_enabled = False
        
        self.connect(publisher, SIGNAL("VALID_PACKET_RECEIVED"), self._on_valid_packet_received)
        self.connect(publisher, SIGNAL("INVALID_PACKET_RECEIVED"), self._on_invalid_packet_received)

    def _add_record(self, direction, packet_type, byte_array):
        self.query_engine.insert(direction, packet_type, byte_array)
        if self.is_autorefresh_enabled:
            self.refresh()
            
    def _on_invalid_packet_received(self, data):
        self._add_record("incoming", "unknown", data)
    
    def _on_valid_packet_received(self, packet_type, data):
        self._add_record("incoming", packet_type, data)

    def refresh(self):
        self.distinct_table_view_model.refresh_data()
        self.session_table_view_model.refresh_data()

    def setAutoRefresh(self, toggle):
        self.is_autorefresh_enabled = toggle

    def getProxyModel(self):
        return self.distinct_table_view_model.get_model()

    def getSessionProxy(self):
        return self.session_table_view_model.get_model()

    def clearDatabase(self):
        self.query_engine.clear_database()
        self.refresh()

class ModifiedPacketTableModel(QObject):
    def __init__(self, parent = None):
        QObject.__init__(self, parent)
        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable("distinctpackets")
        self.model.sort(0, Qt.DescendingOrder)
        self.proxy = QtGui.QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterKeyColumn(3)
        self.proxy.setDynamicSortFilter(True)
        
    def get_model(self):
        return self.proxy
    
    def refresh_data(self):
        self.model.select()

class AnyPacketTableModel(QObject):
    def __init__(self, parent = None):
        QObject.__init__(self, parent)
        self.model = QtSql.QSqlRelationalTableModel(self)
        self.model.setTable("session")
        self.model.setRelation(1, QtSql.QSqlRelation("distinctpackets", "ID", "Class"))
        self.model.sort(0, Qt.DescendingOrder)
        self.proxy = QtGui.QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterKeyColumn(1)
        self.proxy.setDynamicSortFilter(True)
        
    def get_model(self):
        return self.proxy
        
    def refresh_data(self):
        self.model.select()