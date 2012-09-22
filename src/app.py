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


class XmlSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(XmlSyntaxHighlighter, self).__init__(parent)
        self.formattingRules = []

        # Inner xml format.
        rule = QtGui.QTextCharFormat()
        rule.setFontWeight(QtGui.QFont.Bold)
        regex = QtCore.QRegExp("[^\>]+(?=\<\/)")
        regex.setMinimal(True)
        self.formattingRules.append((regex, rule))


    def highlightBlock(self, text):
        for pattern, rule in self.formattingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule)
                index = expression.indexIn(text, index + length)


class DecoderDialog(decbase, decform):
    def __init__(self, parent = None):
        super(decbase, self).__init__(parent)
        self.setupUi(self)
        self.setupConnections()
        self.sqlwrapper = parent.getFactory().getQtSQLWrapper()
        self.decoder = parent.getFactory().getProtocolDecoder()
        self.hl1 = XmlSyntaxHighlighter(self.uiSelected)
        self.hl2 = XmlSyntaxHighlighter(self.uiDeselected)
        self.hl3 = XmlSyntaxHighlighter(self.uiChangeSet)

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
        proxy = self.sqlwrapper.getProxyModel()
        origmdl = self.sqlwrapper.getSourceModel()

        if newMdlIndex.isValid():
            newIndex = proxy.mapToSource(newMdlIndex)
            newrecord = origmdl.record(newIndex.row())
            newseq = [x for x in bytearray.fromhex(str(newrecord.value("hex").toString()))]
            self.uiSelected.setText(self.decoder.createXMLPacket(newseq))

            timestamp = newrecord.value("timestamp").toString()
            raw = str(newrecord.value("hex").toString())
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
            oldseq = [x for x in bytearray.fromhex(str(oldrecord.value("hex").toString()))]
            self.uiDeselected.setText(self.decoder.createXMLPacket(oldseq))

        if newMdlIndex.isValid() & oldMdlIndex.isValid():
            self.uiChangeSet.setText(self.decoder.diffXMLPacket(newseq, oldseq))

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
        self.tableView.setColumnWidth(0, 150)
        self.tableView.setColumnWidth(1, 60)
        self.tableView.setColumnWidth(2, 100)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setSortingEnabled(True)
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

    def setupChildDialogs(self):
        self.decDialog = DecoderDialog(self)

    def setupDB(self):
        self.db = self.factory.getQtSQLWrapper()
        self.tableView.setModel(self.db.getProxyModel())
        self.connect(self.tableView.selectionModel(), SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.decDialog.Update)

        proxy = self.db.getProxyModel()
        self.connect(self.lineEdit, SIGNAL("textChanged(QString)"), proxy.setFilterRegExp)
        self.refreshView()

    def setupConnections(self):
        self.btnRefresh.clicked.connect(self.refreshView)
        self.btnAnalyze.clicked.connect(self.decDialog.show)
        self.btnClear.clicked.connect(self.db.clearDatabase)
        self.btnReplay.clicked.connect(self.on_btnReplay_clicked)
        self.replaying = False
        self.btnRecordPause.clicked.connect(self.on_btnRecordPause_clicked)
        self.recording = False
        self.checkBox.toggled.connect(self.db.setAutoRefresh)
        self.cbFilterDupes.toggled.connect(self.db.filterduplicates)
        self.db.getSourceModel().rowsInserted.connect(self.tableView.setCurrentIndex)

    def refreshView(self):
        #index = self.tableView.selectionModel().currentIndex()
        self.db.refresh()
        #self.tableView.selectRow(index.row())
        #print index.row()
        # add code to refresh view as well

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
