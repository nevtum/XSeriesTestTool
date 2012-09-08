'''
Created on 11/06/2012

@author: neville
'''
import sys
from factory import TransmissionFactory
from views import DataLogger, Publisher
from comms_threads import ListenThread, ReplayThread
from PyQt4 import QtGui, uic
from PyQt4.QtCore import SIGNAL

decbase, decform = uic.loadUiType("gui/packetview.ui")
appbase, appform = uic.loadUiType("gui/analyzer.ui")



class DecoderDialog(decbase, decform):
    def __init__(self, parent = None):
        super(decbase, self).__init__(parent)
        self.setupUi(self)
        self.setupConnections()
        self.sqlwrapper = parent.getFactory().getQtSQLWrapper()

    def setupConnections(self):
        self.btnCopy.clicked.connect(self.on_btnCopy_clicked)
        self.btnNext.clicked.connect(self.on_btnNext_clicked)
        self.btnPrev.clicked.connect(self.on_btnPrev_clicked)

    def on_btnCopy_clicked(self):
        self.textEdit.selectAll()
        self.textEdit.copy()

    def on_btnNext_clicked(self):
        mdlindex = self.parent().getCurrentModelIndex()
        if mdlindex.isValid():
            nextrow = mdlindex.row()+1
            self.parent().tableView.selectRow(nextrow)

    def on_btnPrev_clicked(self):
        mdlindex = self.parent().getCurrentModelIndex()
        if mdlindex.isValid():
            prevrow = mdlindex.row()-1
            self.parent().tableView.selectRow(prevrow)

    def Update(self, newMdlIndex, oldMdlIndex):
        if newMdlIndex.isValid():
            srcMdlIndex = self.sqlwrapper.getModel().mapToSource(newMdlIndex)
            
            timestamp = self.sqlwrapper.getTimestamp(srcMdlIndex.row())
            contents = self.sqlwrapper.getDecodedData(srcMdlIndex.row())
            raw = self.sqlwrapper.getRawData(srcMdlIndex.row())
            
            string = ""
            for i in range(len(raw)):
                string += raw[i]
                if i > 0:
                    if (i+1)%60 == 0:
                        string += "\n"
                    elif (i+1)%20 == 0:
                        string += "\t"
                    elif (i+1)%2 == 0:
                        string += " "

            self.lineEdit.setText(timestamp)
            self.textEdit.setText(contents)
            self.uiRawData.setText(string)

            #DBGLOG("ProxyIndex: %i, ModelIndex: %i" % (newMdlIndex.row(), srcMdlIndex.row()))




class MyApp(appbase, appform):
    def __init__(self, parent = None):
        super(appbase, self).__init__(parent)
        self.setupUi(self)
        self.db = None
        self.factory = TransmissionFactory()
        self.queue = self.factory.getMessageQueue()
        self.datalogger = DataLogger("test.db", self)
        self.publisher = Publisher()
        self.setupChildDialogs()
        self.setupDB()
        self.setupConnections()
        self.listenThread = ListenThread(self)
        self.replayThread = ReplayThread(self)
        self.lineEditPort.setText("com17")

    def getFactory(self):
        return self.factory

    def setupChildDialogs(self):
        self.decDialog = DecoderDialog(self)

    def setupDB(self):
        self.db = self.factory.getQtSQLWrapper()
        self.tableView.setModel(self.db.getModel())
        self.connect(self.tableView.selectionModel(), SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.decDialog.Update)

        proxy = self.db.getModel()
        self.connect(self.lineEdit, SIGNAL("textChanged(QString)"), proxy.setFilterRegExp)
        self.updateViewContents()

    def setupConnections(self):
        self.btnRefresh.clicked.connect(self.on_btnRefresh_clicked)
        self.btnAnalyze.clicked.connect(self.on_btnAnalyze_clicked)
        self.btnClear.clicked.connect(self.on_btnClear_clicked)
        self.pushButton.clicked.connect(self.on_btnReplay_clicked)
        self.replaying = False
        self.btnRecordPause.clicked.connect(self.on_btnRecordPause_clicked)
        self.recording = False
        self.checkBox.toggled.connect(self.on_autoRefreshCheckBoxToggled)
        self.cbFilterDupes.toggled.connect(self.on_IgnoreDupesCheckBoxToggled)
        self.connect(self.queue, SIGNAL("receivedpacket"), self.on_Queued_message)
        self.setupViews()

    def setupViews(self):
        self.publisher.Attach(self.datalogger)

    def getCurrentModelIndex(self):
        index = self.tableView.selectionModel().currentIndex()
        return index

    def on_Queued_message(self):
        while not self.queue.isEmpty():
            self.publisher.Record(self.queue.dequeue())

    def on_autoRefreshCheckBoxToggled(self):
        if self.checkBox.isChecked():
            self.connect(self.datalogger, SIGNAL("newentry"), self.on_btnRefresh_clicked)
        else:
            self.disconnect(self.datalogger, SIGNAL("newentry"), self.on_btnRefresh_clicked)

    def on_IgnoreDupesCheckBoxToggled(self):
        ddfilter = self.datalogger.getDuplicateDatablockFilter()
        if self.cbFilterDupes.isChecked():
            ddfilter.filterduplicates(True)
        else:
            ddfilter.filterduplicates(False)

    def on_btnRecordPause_clicked(self):
        if not self.recording:
            self.btnRecordPause.setText("Pause")
            self.pushButton.setDisabled(True)
            self.lineEditPort.setDisabled(True)
            self.recording = True
            portname = str(self.lineEditPort.text())
            self.listenThread.setcommport(portname)
            self.listenThread.setbaud(9600)
            self.listenThread.start()
        else:
            self.btnRecordPause.setText("Record")
            self.pushButton.setDisabled(False)
            self.lineEditPort.setDisabled(False)
            self.recording = False
            self.listenThread.quit()

    def on_btnReplay_clicked(self):
        if not self.replaying:
            self.pushButton.setText("Stop Replay")
            self.btnRecordPause.setDisabled(True)
            self.lineEditPort.setDisabled(True)
            self.replaying = True
            portname = str(self.lineEditPort.text())
            self.replayThread.setcommport(portname)
            self.replayThread.setbaud(9600)
            self.replayThread.start()
        else:
            # what about when thread finishes on its own?
            self.pushButton.setText("Replay")
            self.btnRecordPause.setDisabled(False)
            self.lineEditPort.setDisabled(False)
            self.replaying = False
            self.replayThread.quit()

    def on_btnClear_clicked(self):
        self.db.clearDatabase()
        self.updateViewContents()

    def on_btnAnalyze_clicked(self):
        self.decDialog.show()

    def on_btnRefresh_clicked(self):
        self.updateViewContents()

    def updateViewContents(self):
        self.db.refresh()
        self.tableView.setColumnWidth(0, 150)
        self.tableView.setColumnWidth(1, 60)
        self.tableView.setColumnWidth(2, 100)
        self.tableView.setColumnWidth(3, 250)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setSortingEnabled(True)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())
