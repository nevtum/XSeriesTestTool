from PyQt4 import uic
from PyQt4.QtCore import SIGNAL
from xpacket import XPacket

decbase, decform = uic.loadUiType("gui/packetview.ui")

class DecoderDialog(decbase, decform):
    def __init__(self, view_actions, parent = None):
        super(decbase, self).__init__(parent)
        self.setupUi(self)
        self.setupConnections(view_actions)
        self.dvm = parent.getFactory().get_data_view_manager()
        self.decoder = parent.getFactory().getProtocolDecoder()

    def setupConnections(self, view_actions):
        self.btnCopy.clicked.connect(self._on_btnCopy_clicked)
        self.btnNext.clicked.connect(view_actions.navigate_next_entry)
        self.btnPrev.clicked.connect(view_actions.navigate_prev_entry)
        self.btnFirst.clicked.connect(view_actions.navigate_first_entry)
        self.btnLast.clicked.connect(view_actions.navigate_final_entry)

    def _on_btnCopy_clicked(self):
        self.textEdit.selectAll()
        self.textEdit.copy()

    def Update(self, newMdlIndex, oldMdlIndex):
        self._update_current_packet_view(newMdlIndex)
        self._update_old_packet_view(oldMdlIndex)
        self._update_differences_view(newMdlIndex, oldMdlIndex)
    
    def _update_current_packet_view(self, newMdlIndex):
        if newMdlIndex.isValid():
            record = self._get_record(newMdlIndex)
            packet = self._to_packet(record)
            self.uiSelected.setText(packet.pretty_print(self.decoder))
            self.lineEdit.setText(packet.get_time())
            self.uiRawData.setText(packet.format_raw_data())
            
    def _update_old_packet_view(self, oldMdlIndex):
        if oldMdlIndex.isValid():
            record = self._get_record(oldMdlIndex)
            packet = self._to_packet(record)
            self.uiDeselected.setText(packet.pretty_print(self.decoder))
    
    def _update_differences_view(self, newMdlIndex, oldMdlIndex):
        if newMdlIndex.isValid() & oldMdlIndex.isValid():
            new_pkt = self._to_packet(self._get_record(newMdlIndex))
            old_pkt = self._to_packet(self._get_record(oldMdlIndex))
            differences = new_pkt.get_differences(old_pkt, self.decoder)
            self.uiChangeSet.setText(differences)
        
    def _get_record(self, model_index):
        proxy = self.dvm.getProxyModel()
        true_index = proxy.mapToSource(model_index)
        origmdl = proxy.sourceModel()
        return origmdl.record(true_index.row())
    
    def _to_packet(self, record):
        timestamp = record.value("LastChanged")
        packet_type = record.value("Class")
        data = record.value("Data")
        return XPacket(timestamp, packet_type, data)
