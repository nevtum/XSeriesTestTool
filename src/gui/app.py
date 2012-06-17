'''
Created on 11/06/2012

@author: neville
'''
import sys
from decoder import *
from PyQt4 import QtGui, QtSql
from analyzer import Ui_MainWindow
from maxrowsdialog import Ui_Dialog
from packetview import Ui_packetViewer
 
class XPacketDB:
    def __init__(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("test.sqlite")
        self.db.open()
        self.model = QtSql.QSqlQueryModel()
        self.setupDecoder()
        
    def setupDecoder(self):
        xmetadata = metaRepository('../settings/')
        self.xdec = XProtocolDecoder(xmetadata)
        self.xdec.registerTypeDecoder('integer-reverse', reverseIntegerDecoder)
        self.xdec.registerTypeDecoder('currency-reverse', reverseCurrencyDecoder)
        self.xdec.registerTypeDecoder('boolean', booleanDecoder)
        self.xdec.registerTypeDecoder('ascii-reverse', reverseAsciiDecoder)
        
    def getModel(self):
        return self.model
    
    def getData(self, rowindex):
        assert(isinstance(rowindex, int))
        record = self.model.record(rowindex)
        packet = str(record.value("hex").toString())
        return self.xdec.createXMLPacket(packet)
    
    def __del__(self):
        self.db.close()

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
        
    def setText(self, message):
        self.ui.textEdit.setText(message)
        
    def setupConnections(self):
        self.ui.btnCopy.clicked.connect(self.on_btnCopy_clicked)
        
    def on_btnCopy_clicked(self):
        self.ui.textEdit.selectAll()
        self.ui.textEdit.copy()
 
class MyApp(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupDB()
        self.setupChildDialogs()
        self.setupConnections()
        
    def setupChildDialogs(self):
        self.decDialog = DecoderDialog(self)
        self.maxRowsDialog = MaxRowsDialog(self)
    
    def setupDB(self):
        self.db = XPacketDB()
        self.ui.tableView.setModel(self.db.getModel())
        self.query = "SELECT * FROM packetlog ORDER BY timestamp DESC LIMIT 100"
        self.updateViewContents()
        self.ui.lineEdit.setText(self.db.getModel().query().executedQuery())
        self.ui.tableView.resizeColumnsToContents()
        
    def setupConnections(self):
        # set up connection to selection of record
        # some bugs here regarding current row is not selected
        self.ui.tableView.selectionModel().currentRowChanged.connect(self.decodeSelectedPacket)
        self.ui.btnRefresh.clicked.connect(self.on_btnRefresh_clicked)
        self.ui.btnAnalyze.clicked.connect(self.on_btnAnalyze_clicked)
        self.ui.actionSet_Maximum_Rows.triggered.connect(self.on_MaxRowsAction_triggered)
        
    def on_MaxRowsAction_triggered(self):
        self.maxRowsDialog.exec_()
    
    def on_btnAnalyze_clicked(self):
        self.decDialog.show()
        
    def on_btnRefresh_clicked(self):
        # updates query from user specified SQL statement
        self.query = self.ui.lineEdit.text()
        self.updateViewContents()
    
    def updateViewContents(self):
        self.db.getModel().setQuery(self.query)
        self.ui.tableView.selectRow(0)
        
    def decodeSelectedPacket(self):
        index = self.ui.tableView.currentIndex().row()
        self.decDialog.setText(self.db.getData(index))
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())