"""
XSeriesTestTool - A NSW gaming protocol decoder/analyzer
    Copyright (C) 2012  Neville Tummon

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
from datetime import datetime
from PyQt4 import QtGui, uic, QtSql
from PyQt4.QtCore import SIGNAL, QObject

base, form = uic.loadUiType("gui/testdata_editor.ui")

class TestDataEditor(base, form):
    def __init__(self, parent = None):
        super(base, self).__init__(parent)
        self.setupUi(self)

        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("test.db")
        self.db.open()

        self.mdl = QtSql.QSqlTableModel(self, self.db)
        self.mdl.setTable("distinctpackets")
        self.mdl.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.mdl.select()

        self.proxymdl = QtGui.QSortFilterProxyModel(self)
        self.proxymdl.setSourceModel(self.mdl)
        self.proxymdl.setFilterKeyColumn(3)
        self.proxymdl.setDynamicSortFilter(True)

        self.uiView.setModel(self.proxymdl)
        self.uiView.setColumnWidth(0, 50)
        self.uiView.resizeColumnToContents(1)
        self.uiView.resizeColumnToContents(2)
        #self.uiView.setColumnWidth(1, 70)
        #self.uiView.setColumnWidth(2, 60)
        self.uiView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.uiView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.uiView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.uiView.horizontalHeader().setStretchLastSection(True)
        self.uiView.setSortingEnabled(True)

        self.mapper = QtGui.QDataWidgetMapper(self)
        self.mapper.setModel(self.proxymdl)
        self.mapper.addMapping(self.uiDateTime, 1)
        self.mapper.addMapping(self.uiDirection, 2)
        self.mapper.addMapping(self.uiType, 3)
        self.mapper.addMapping(self.uiPacket, 4)
        self.mapper.toFirst()
        self.connect(self.uiView.selectionModel(), SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.mapper.setCurrentModelIndex)

        self.btnPrev.clicked.connect(self.toPrevious)
        self.btnNext.clicked.connect(self.toNext)
        self.btnInsert.clicked.connect(self.addItem)
        self.btnRemove.clicked.connect(self.removeRow)
        self.lineEdit.textChanged.connect(self.proxymdl.setFilterRegExp)

        self.query = QtSql.QSqlQuery(self.db)

    def toNext(self):
        row = self.uiView.selectionModel().currentIndex().row()
        self.uiView.selectRow(row+1)

    def toPrevious(self):
        row = self.uiView.selectionModel().currentIndex().row()
        self.uiView.selectRow(row-1)

    def addItem(self):
        self.query.prepare("INSERT INTO packetlog VALUES(:date,:direction,:type,:contents)")
        self.query.bindValue(":date", str(datetime.now()))
        self.query.bindValue(":direction", "incoming")
        self.query.bindValue(":type", "testpacket")
        self.query.bindValue(":contents", "")

        index = self.uiView.selectionModel().currentIndex()
        print self.query.exec_()
        self.mdl.select()
        self.uiView.selectRow(index.row())

    def removeRow(self):
        index = self.uiView.selectionModel().currentIndex()
        self.mdl.removeRow(index.row())
        self.uiView.selectRow(index.row())

if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)
    app.setStyle("cleanlooks")
    
    wnd = TestDataEditor()
    wnd.show()

    sys.exit(app.exec_())