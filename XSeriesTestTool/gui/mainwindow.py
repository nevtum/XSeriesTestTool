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

from factory import TransmissionFactory
from gui.decoder_view import DecoderDialog
from comms_threads import ListenThread, ReplayThread
from PyQt4 import uic
from PyQt4.QtCore import SIGNAL

appbase, appform = uic.loadUiType("gui/analyzer.ui")

class MyApp(appbase, appform):
    def __init__(self, parent = None):
        super(appbase, self).__init__(parent)
        self.setupUi(self)
        self.factory = TransmissionFactory()
        self.setupChildDialogs()
        self.setupDB()
        self.setupConnections()
        self.setupWidgets()
        self.listenThread = ListenThread(self)
        self.replayThread = ReplayThread(self)
        self.lineEditPort.setText("com17")

    def getFactory(self):
        return self.factory

    def setupWidgets(self):
        self.tableView.setColumnWidth(0, 40)
        self.tableView.setColumnWidth(1, 150)
        self.tableView.setColumnWidth(2, 60)
        self.tableView.setColumnWidth(3, 60)

        self.tableView2.setColumnWidth(0, 150)

    def setupChildDialogs(self):
        self.decDialog = DecoderDialog(self)

    def setupDB(self):
        self.db = self.factory.getQtSQLWrapper()
        proxy = self.db.getProxyModel()
        sessionproxy = self.db.getSessionProxy()

        self.tableView.setModel(proxy)
        self.tableView2.setModel(sessionproxy)
        self.connect(self.tableView.selectionModel(), SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.decDialog.Update)

        self.connect(self.lineEdit, SIGNAL("textChanged(QString)"), proxy.setFilterRegExp)
        self.connect(self.lineEdit, SIGNAL("textChanged(QString)"), sessionproxy.setFilterRegExp)
        self.refreshView()

    def setupConnections(self):
        self.actionRefresh.triggered.connect(self.refreshView)
        self.actionOpenDecoder.triggered.connect(self.decDialog.show)
        self.actionClear_Session_data.triggered.connect(self.db.clearDatabase)
        self.btnReplay.clicked.connect(self.on_btnReplay_clicked)
        self.replaying = False
        self.btnRecordPause.clicked.connect(self.on_btnRecordPause_clicked)
        self.recording = False
        self.actionEnable_Autorefresh.toggled.connect(self.db.setAutoRefresh)
        #self.db.getSourceModel().rowsInserted.connect(self.tableView.setCurrentIndex)

    def refreshView(self):
        self.db.refresh()

    # to control tableView navigation
    def toFirst(self):
        self.tableView.selectRow(0)

    # to control tableView navigation
    def toNext(self):
        row = self.tableView.selectionModel().currentIndex().row()
        self.tableView.selectRow(row+1)

    # to control tableView navigation
    def toPrevious(self):
        row = self.tableView.selectionModel().currentIndex().row()
        self.tableView.selectRow(row-1)

    # to control tableView navigation
    def toLast(self):
        rowcount = self.db.getProxyModel().rowCount()
        self.tableView.selectRow(rowcount-1)

    def on_btnRecordPause_clicked(self):
        if not self.recording:
            self.btnRecordPause.setText("Pause")
            self.btnReplay.setDisabled(True)
            self.lineEditPort.setDisabled(True)
            self.recording = True
            portname = str(self.lineEditPort.text())
            self.listenThread.setcommport(portname)
            self.listenThread.setbaud(9600)
            self.listenThread.start()
        else:
            self.btnRecordPause.setText("Record")
            self.btnReplay.setDisabled(False)
            self.lineEditPort.setDisabled(False)
            self.recording = False
            self.listenThread.quit()

    def on_btnReplay_clicked(self):
        if not self.replaying:
            self.btnReplay.setText("Stop Replay")
            self.btnRecordPause.setDisabled(True)
            self.lineEditPort.setDisabled(True)
            self.replaying = True
            portname = str(self.lineEditPort.text())
            self.replayThread.setcommport(portname)
            self.replayThread.setbaud(9600)
            self.replayThread.start()
        else:
            # add slot to listen to signal
            # when thread finishes on its own
            self.btnReplay.setText("Replay")
            self.btnRecordPause.setDisabled(False)
            self.lineEditPort.setDisabled(False)
            self.replaying = False
            self.replayThread.quit()
