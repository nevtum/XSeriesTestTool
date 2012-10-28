'''
Created on 11/06/2012

@author: neville
'''
import sys
from factory import TransmissionFactory
from comms_threads import ListenThread, ReplayThread
from PyQt4 import QtGui, uic, QtCore
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
        self.btnNext.clicked.connect(self.parent().toNext)
        self.btnPrev.clicked.connect(self.parent().toPrevious)
        self.btnFirst.clicked.connect(self.parent().toFirst)
        self.btnLast.clicked.connect(self.parent().toLast)

    def on_btnCopy_clicked(self):
        self.textEdit.selectAll()
        self.textEdit.copy()

    def GetPrettyPrint(self, seq):
        packetname, array = self.decoder.getDecodedData(seq)
        mystring = "Packet: %s\n" % packetname
        for key, value in array:
            mystring += "    {0:50s}\t{1}\n".format(key, value)
        return mystring

    def Update(self, newMdlIndex, oldMdlIndex):
        proxy = self.sqlwrapper.getProxyModel()
        origmdl = proxy.sourceModel()

        if newMdlIndex.isValid():
            newIndex = proxy.mapToSource(newMdlIndex)
            newrecord = origmdl.record(newIndex.row())
            newseq = [x for x in bytearray.fromhex(str(newrecord.value("Data").toString()))]

            self.uiSelected.setText(self.GetPrettyPrint(newseq))

            timestamp = newrecord.value("LastChanged").toString()
            raw = str(newrecord.value("Data").toString())
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
            self.uiRawData.setText(string)

        if oldMdlIndex.isValid():
            oldIndex = proxy.mapToSource(oldMdlIndex)
            oldrecord = origmdl.record(oldIndex.row())
            oldseq = [x for x in bytearray.fromhex(str(oldrecord.value("Data").toString()))]
            #self.uiDeselected.setText(self.decoder.createXMLPacket(oldseq))
            self.uiDeselected.setText(self.GetPrettyPrint(oldseq))

        if newMdlIndex.isValid() & oldMdlIndex.isValid():
            packetname, array = self.decoder.getDiffPackets(newseq, oldseq)
            mystring = "Packet: %s\n" % packetname

            for key, newval, oldval in array:
                mystring += "  {0}\n".format(key)
                mystring += "    {0:10s}\t{1}\n".format('after:', newval)
                mystring += "    {0:10s}\t{1}\n\n".format('before:', oldval)
            self.uiChangeSet.setText(mystring)

            #DBGLOG("ProxyIndex: %i, ModelIndex: %i" % (newMdlIndex.row(), srcMdlIndex.row()))




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

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())
