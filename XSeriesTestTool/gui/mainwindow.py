import debug
from factory import TransmissionFactory
from gui.decoder_view import DecoderDialog
from PyQt4 import uic
from PyQt4.QtCore import SIGNAL

appbase, appform = uic.loadUiType("gui/analyzer.ui")

class MyApp(appbase, appform):
    def __init__(self, parent = None):
        super(appbase, self).__init__(parent)
        self.setupUi(self)
        self.factory = TransmissionFactory(self)
        self.setupChildDialogs()
        self.setupDB()
        self.setupConnections()
        self.setupWidgets()
        self.listenThread = self.factory.get_serial_thread()
        self.populateComPorts()
        
    def populateComPorts(self):
        import serial_app
        for port_nr in serial_app.list_serial_ports():
            self.comboBoxComPorts.addItem("COM%i" % port_nr)
    
    def getFactory(self):
        return self.factory

    def setupWidgets(self):
        self.tableView.setColumnWidth(0, 40)
        self.tableView.setColumnWidth(1, 150)
        self.tableView.setColumnWidth(2, 60)
        self.tableView.setColumnWidth(3, 60)

        self.tableView2.setColumnWidth(0, 150)

    def setupChildDialogs(self):
        self.decDialog = DecoderDialog(self.factory.get_publisher(), self)

    def setupDB(self):
        self.db = self.factory.getQtSQLWrapper()
        proxy = self.db.getProxyModel()
        sessionproxy = self.db.getSessionProxy()

        self.tableView.setModel(proxy)
        self.tableView2.setModel(sessionproxy)
        
        # connections to lineEdit
        self.lineEdit.textChanged.connect(proxy.setFilterRegExp)
        self.lineEdit.textChanged.connect(sessionproxy.setFilterRegExp)
        
        self.refreshView()

    def setupConnections(self):
        publisher = self.factory.get_publisher()
        self.connect(publisher, SIGNAL("NEXT_ENTRY_NAVIGATED"), self.toNext)
        self.connect(publisher, SIGNAL("PREVIOUS_ENTRY_NAVIGATED"), self.toPrevious)
        self.connect(publisher, SIGNAL("FIRST_ENTRY_NAVIGATED"), self.toFirst)
        self.connect(publisher, SIGNAL("FINAL_ENTRY_NAVIGATED"), self.toLast)        
        
        self.actionRefresh.triggered.connect(self.refreshView)
        self.actionOpenDecoder.triggered.connect(self.decDialog.show)
        self.tableView.doubleClicked.connect(self.decDialog.show)
        self.tableView.selectionModel().currentChanged.connect(self.decDialog.Update)
        self.actionClear_Session_data.triggered.connect(self.db.clearDatabase)
        self.btnRecordPause.clicked.connect(self.on_btnRecordPause_clicked)
        self.recording = False
        self.actionEnable_Autorefresh.toggled.connect(self.db.setAutoRefresh)
        self.actionEnable_DebugLog.toggled.connect(self._toggle_logging_settings)
        #self.db.getSourceModel().rowsInserted.connect(self.tableView.setCurrentIndex)

    def _toggle_logging_settings(self, enabled):
        if enabled:
            debug.enable_logging()
        else:
            debug.disable_logging()

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
            self.comboBoxComPorts.setDisabled(True)
            self.recording = True
            portname = str(self.comboBoxComPorts.currentText())
            self.listenThread.setcommport(portname)
            self.listenThread.setbaud(9600)
            self.listenThread.start()
        else:
            self.btnRecordPause.setText("Record")
            self.comboBoxComPorts.setDisabled(False)
            self.recording = False
            self.listenThread.quit()
