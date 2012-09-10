'''
Created on 11/06/2012

@author: neville
'''
import sys
from factory import TransmissionFactory
from views import Publisher
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
        self.decoder = parent.getFactory().getProtocolDecoder()

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
            proxy = self.sqlwrapper.getProxyModel()
            origmdl = self.sqlwrapper.getSourceModel()
            srcMdlIndex = proxy.mapToSource(newMdlIndex)
            
            record = origmdl.record(srcMdlIndex.row())
            timestamp = record.value("timestamp").toString()
            raw = str(record.value("hex").toString())
            seq = [x for x in bytearray.fromhex(raw)]
            
            decoded = self.decoder.createXMLPacket(seq)
            
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
            self.textEdit.setText(decoded)
            self.uiRawData.setText(string)

            #DBGLOG("ProxyIndex: %i, ModelIndex: %i" % (newMdlIndex.row(), srcMdlIndex.row()))




class MyApp(appbase, appform):
    def __init__(self, parent = None):
        super(appbase, self).__init__(parent)
        self.setupUi(self)
        self.db = None
        self.factory = TransmissionFactory()
        #self.queue = self.factory.getMessageQueue()
        #self.datalogger = DataLogger("test.db", self)
        #self.publisher = Publisher()
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
        self.tableView.setModel(self.db.getProxyModel())
        self.connect(self.tableView.selectionModel(), SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.decDialog.Update)

        proxy = self.db.getProxyModel()
        self.connect(self.lineEdit, SIGNAL("textChanged(QString)"), proxy.setFilterRegExp)
        self.updateViewContents()

    def setupConnections(self):
        self.btnRefresh.clicked.connect(self.updateViewContents)
        self.btnAnalyze.clicked.connect(self.decDialog.show)
        self.btnClear.clicked.connect(self.on_btnClear_clicked)
        self.pushButton.clicked.connect(self.on_btnReplay_clicked)
        self.replaying = False
        self.btnRecordPause.clicked.connect(self.on_btnRecordPause_clicked)
        self.recording = False
        self.checkBox.toggled.connect(self.on_autoRefreshCheckBoxToggled)
        self.cbFilterDupes.toggled.connect(self.on_IgnoreDupesCheckBoxToggled)
        #self.setupViews()

    #def setupViews(self):
    #    self.publisher.Attach(self.datalogger)

    def getCurrentModelIndex(self):
        index = self.tableView.selectionModel().currentIndex()
        return index

    def on_Queued_message(self):
        while not self.queue.isEmpty():
            self.publisher.Record(self.queue.dequeue())

    def on_autoRefreshCheckBoxToggled(self):
        if self.checkBox.isChecked():
            self.connect(self.db, SIGNAL("newentry"), self.updateViewContents)
        else:
            self.disconnect(self.db, SIGNAL("newentry"), self.updateViewContents)

    def on_IgnoreDupesCheckBoxToggled(self):
        ddfilter = self.db.getDuplicateDatablockFilter()
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

    def updateViewContents(self):
        self.db.getSourceModel().setQuery("SELECT * FROM packetlog ORDER BY timestamp DESC LIMIT 200")
        self.tableView.setColumnWidth(0, 150)
        self.tableView.setColumnWidth(1, 60)
        self.tableView.setColumnWidth(2, 100)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setSortingEnabled(True)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())
