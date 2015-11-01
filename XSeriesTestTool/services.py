import utilities
import scripts
from datetime import datetime
from PyQt4.QtCore import QObject
from PyQt4 import QtSql

class QueryEngine(QObject):
    def __init__(self, filename, parent = None):
        QObject.__init__(self, parent)
        self.context = self._create_context(filename)
        self._create_sql_tables()

    def insert(self, direction, packet_type, byte_array):
        loggedtime = str(datetime.now())
        self._insert_changed_packet(direction, packet_type, byte_array, loggedtime)
        self._insert_received_packet(packet_type, byte_array, loggedtime)

    def clear_database(self):
        query = QtSql.QSqlQuery(self.context)
        query.exec_(scripts.drop_session_table())
        query.exec_(scripts.drop_distinct_table())
        query.finish()

    def _create_context(self, filename):
        context = QtSql.QSqlDatabase.addDatabase(scripts.database_type())
        context.setDatabaseName(filename)
        context.open()
        return context

    def _get_latest_packet(self, packet_type):
        query = QtSql.QSqlQuery(self.context)
        query.prepare(scripts.get_latest(packet_type))
        query.exec_()
        if query.next():
            row_id = query.value(0)
            timestamp = query.value(1)
            data = query.value(4)
            return row_id, timestamp, data
        return None, None, None

    def _create_sql_tables(self):
        query = QtSql.QSqlQuery(self.context)
        query.prepare(scripts.create_session_table())
        query.exec_()
        query.prepare(scripts.create_distinct_table())
        query.exec_()
        query.finish()

    def _has_changed(self, packet_type, byte_array):
        row_id, timestamp, data = self._get_latest_packet(packet_type)
        if row_id is None:
            return True
        
        sequence = utilities.convert_to_hex_string(byte_array)
        return sequence != data

    def _insert_changed_packet(self, direction, packet_type, byte_array, logged_time):
        if not self._has_changed(packet_type, byte_array):
            return

        query = QtSql.QSqlQuery(self.context)
        hexstring = utilities.convert_to_hex_string(byte_array)
        query.prepare(scripts.insert_distinct())
        query.bindValue(":date", logged_time)
        query.bindValue(":direction", str(direction))
        query.bindValue(":type", packet_type)
        query.bindValue(":contents", str(hexstring))
        query.exec_()
        query.finish()

    def _insert_received_packet(self, packet_type, byte_array, logged_time):
        row_id, timestamp, data = self._get_latest_packet(packet_type)
        query = QtSql.QSqlQuery(self.context)
        query.prepare(scripts.insert_session())
        query.bindValue(":date", logged_time)
        query.bindValue(":packetid", row_id)
        query.exec_()
        query.finish()

    def __del__(self):
        self.context.close()
