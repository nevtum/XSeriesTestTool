'''
Created on 11/06/2012

@author: neville
'''
import sys
from factory import TransmissionFactory
from views import DataLogger, Publisher
from comms_threads import *
from PyQt4 import QtGui, QtCore
from gui.analyzer import Ui_MainWindow
from gui.maxrowsdialog import Ui_Dialog
from gui.packetview import Ui_packetViewer

class MaxRowsDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setupConnections()

    def setupConnections(self):
        pass






class DecoderDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_packetViewer()
        self.ui.setupUi(self)
        self.setupConnections()
        self.sqlwrapper = parent.factory.getQtSQLWrapper()

    def setupConnections(self):
        self.ui.btnCopy.clicked.connect(self.on_btnCopy_clicked)
        self.ui.btnNext.clicked.connect(self.on_btnNext_clicked)
        self.ui.btnPrev.clicked.connect(self.on_btnPrev_clicked)

    def on_btnCopy_clicked(self):
        self.ui.textEdit.selectAll()
        self.ui.textEdit.copy()

    def on_btnNext_clicked(self):
        mdlindex = self.parent().getCurrentModelIndex()
        if mdlindex.isValid():
            nextrow = mdlindex.row()+1
            self.parent().ui.tableView.selectRow(nextrow)

    def on_btnPrev_clicked(self):
        mdlindex = self.parent().getCurrentModelIndex()
        if mdlindex.isValid():
            prevrow = mdlindex.row()-1
            self.parent().ui.tableView.selectRow(prevrow)

    def Update(self, newMdlIndex, oldMdlIndex):
        if newMdlIndex.isValid():
            srcMdlIndex = self.sqlwrapper.getModel().mapToSource(newMdlIndex)
            
            timestamp = self.sqlwrapper.getTimestamp(srcMdlIndex.row())
            contents = self.sqlwrapper.getDecodedData(srcMdlIndex.row())
            raw = self.sqlwrapper.getRawData(srcMdlIndex.row())
            
            self.ui.lineEdit.setText(timestamp)
            self.ui.textEdit.setText(contents)
            self.ui.uiRawData.setText(raw)
            
            #DBGLOG("ProxyIndex: %i, ModelIndex: %i" % (newMdlIndex.row(), srcMdlIndex.row()))
 
 
 
 
class MyApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
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
        self.ui.lineEditPort.setText("com17")

    def setupChildDialogs(self):
        self.decDialog = DecoderDialog(self)
        self.maxRowsDialog = MaxRowsDialog(self)

    def setupDB(self):
        self.db = self.factory.getQtSQLWrapper()
        self.ui.tableView.setModel(self.db.getModel())
        QObject.connect(self.ui.tableView.selectionModel(), SIGNAL("currentChanged(QModelIndex, QModelIndex)"), self.decDialog.Update)

        proxy = self.db.getModel()
        QObject.connect(self.ui.lineEdit, SIGNAL("textChanged(QString)"), proxy.setFilterRegExp)
        self.updateViewContents()

    def setupConnections(self):
        # set up connection to selection of record
        # some bugs here regarding current row is not selected
        self.ui.btnRefresh.clicked.connect(self.on_btnRefresh_clicked)
        self.ui.btnAnalyze.clicked.connect(self.on_btnAnalyze_clicked)
        self.ui.btnClear.clicked.connect(self.on_btnClear_clicked)
        self.ui.pushButton.clicked.connect(self.on_btnReplay_clicked)
        self.replaying = False
        self.ui.btnRecordPause.clicked.connect(self.on_btnRecordPause_clicked)
        self.recording = False
        self.ui.actionSet_Maximum_Rows.triggered.connect(self.on_MaxRowsAction_triggered)
        self.ui.checkBox.toggled.connect(self.on_autoRefreshCheckBoxToggled)
        self.ui.cbFilterDupes.toggled.connect(self.on_IgnoreDupesCheckBoxToggled)
        self.connect(self.queue, SIGNAL("receivedpacket"), self.on_Queued_message)
        self.setupViews()

    def setupViews(self):
        self.publisher.Attach(self.datalogger)

    def getCurrentModelIndex(self):
        index = self.ui.tableView.selectionModel().currentIndex()
        return index

    def on_Queued_message(self):
        self.publisher.Record(self.queue)

    def on_autoRefreshCheckBoxToggled(self):
        if self.ui.checkBox.isChecked():
            self.connect(self.datalogger, SIGNAL("newentry"), self.on_btnRefresh_clicked)
        else:
            self.disconnect(self.datalogger, SIGNAL("newentry"), self.on_btnRefresh_clicked)

    def on_IgnoreDupesCheckBoxToggled(self):
        filter = self.datalogger.getDuplicateDatablockFilter()
        if self.ui.cbFilterDupes.isChecked():
            filter.filterduplicates(True)
        else:
            filter.filterduplicates(False)

    def on_btnRecordPause_clicked(self):
        if not self.recording:
            self.ui.btnRecordPause.setText("Pause")
            self.ui.pushButton.setDisabled(True)
            self.ui.lineEditPort.setDisabled(True)
            self.recording = True
            portname = str(self.ui.lineEditPort.text())
            self.listenThread.setcommport(portname)
            self.listenThread.setbaud(9600)
            self.listenThread.start()
        else:
            self.ui.btnRecordPause.setText("Record")
            self.ui.pushButton.setDisabled(False)
            self.ui.lineEditPort.setDisabled(False)
            self.recording = False
            self.listenThread.quit()

    def on_btnReplay_clicked(self):
        if not self.replaying:
            self.ui.pushButton.setText("Stop Replay")
            self.ui.btnRecordPause.setDisabled(True)
            self.ui.lineEditPort.setDisabled(True)
            self.replaying = True
            portname = str(self.ui.lineEditPort.text())
            self.replayThread.setcommport(portname)
            self.replayThread.setbaud(9600)
            self.replayThread.start()
        else:
            # what about when thread finishes on its own?
            self.ui.pushButton.setText("Replay")
            self.ui.btnRecordPause.setDisabled(False)
            self.ui.lineEditPort.setDisabled(False)
            self.replaying = False
            self.replayThread.quit()

    def on_MaxRowsAction_triggered(self):
        self.maxRowsDialog.exec_()

    def on_btnClear_clicked(self):
        self.db.clearDatabase()
        self.updateViewContents()

    def on_btnAnalyze_clicked(self):
        self.decDialog.show()

    def on_btnRefresh_clicked(self):
        self.updateViewContents()

    def updateViewContents(self):
        """commented out (experimental"""
        #self.db.getModel().setQuery(self.query)

        self.db.refresh()
        self.ui.tableView.setColumnWidth(0, 150)
        self.ui.tableView.setColumnWidth(1, 60)
        self.ui.tableView.setColumnWidth(2, 100)
        self.ui.tableView.setColumnWidth(3, 250)
        self.ui.tableView.setSortingEnabled(True)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())
