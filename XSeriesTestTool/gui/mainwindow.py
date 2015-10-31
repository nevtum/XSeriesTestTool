import debug
from factory import ApplicationFactory
from gui.decoder_view import DecoderDialog
from PyQt4 import uic
from PyQt4.QtCore import SIGNAL

appbase, appform = uic.loadUiType("gui/analyzer.ui")

class MyApp(appbase, appform):
    def __init__(self, parent = None):
        super(appbase, self).__init__(parent)
        self.setupUi(self)
        self.recording = False
        self.factory = ApplicationFactory(self)
        self.decDialog = DecoderDialog(self.factory.get_view_actions(), self)
        self._configure_data_view_manager()
        self._setup_connections()
        self.setupWidgets()
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

    def _configure_data_view_manager(self):
        self.dvm = self.factory.get_data_view_manager()
        self.dvm.connect_distinct_data(self.tableView)
        self.dvm.connect_session_data(self.tableView2)
        self.dvm.connect_text_inputs(self.lineEdit)
        
        self.refreshView()

    def _setup_connections(self):
        view_actions = self.factory.get_view_actions()
        self.connect(view_actions, SIGNAL("NEXT_ENTRY_NAVIGATED"), self.toNext)
        self.connect(view_actions, SIGNAL("PREVIOUS_ENTRY_NAVIGATED"), self.toPrevious)
        self.connect(view_actions, SIGNAL("FIRST_ENTRY_NAVIGATED"), self.toFirst)
        self.connect(view_actions, SIGNAL("FINAL_ENTRY_NAVIGATED"), self.toLast) 
        
        serial_thread = self.factory.get_serial_thread()
        self.connect(view_actions, SIGNAL("RECORDING_STARTED"), serial_thread.on_record_started)
        self.connect(view_actions, SIGNAL("RECORDING_STOPPED"), serial_thread.on_record_stopped)       
        
        self.actionClear_Session_data.triggered.connect(self.dvm.clearDatabase)
        self.actionEnable_Autorefresh.toggled.connect(self.dvm.setAutoRefresh)
        
        self.actionOpenDecoder.triggered.connect(self.decDialog.show)
        self.tableView.doubleClicked.connect(self.decDialog.show)
        self.tableView.selectionModel().currentChanged.connect(self.decDialog.Update)
        
        self.actionRefresh.triggered.connect(self.refreshView)
        self.btnRecordPause.clicked.connect(self.on_btnRecordPause_clicked)
        self.actionEnable_DebugLog.toggled.connect(self._toggle_logging_settings)

    def _toggle_logging_settings(self, enabled):
        if enabled:
            debug.enable_logging()
        else:
            debug.disable_logging()

    def refreshView(self):
        self.dvm.refresh()

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
        rowcount = self.dvm.getProxyModel().rowCount()
        self.tableView.selectRow(rowcount-1)

    def on_btnRecordPause_clicked(self):
        view_actions = self.factory.get_view_actions()
        if not self.recording:
            self.btnRecordPause.setText("Pause")
            self.comboBoxComPorts.setDisabled(True)
            self.recording = True
            portname = str(self.comboBoxComPorts.currentText())
            view_actions.start_recording(portname)
        else:
            self.btnRecordPause.setText("Record")
            self.comboBoxComPorts.setDisabled(False)
            self.recording = False
            view_actions.stop_recording()
