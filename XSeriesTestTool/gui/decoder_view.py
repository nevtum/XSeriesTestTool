from PyQt4 import uic
from PyQt4.QtCore import SIGNAL

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

    def _to_pretty_print(self, seq):
        packetname, array = self.decoder.getDecodedData(seq)
        mystring = "Packet: %s\n" % packetname
        for key, value in array:
            mystring += "    {0:50s}\t{1}\n".format(key, value)
        return mystring

    def Update(self, newMdlIndex, oldMdlIndex):
        proxy = self.dvm.getProxyModel()
        origmdl = proxy.sourceModel()

        if newMdlIndex.isValid():
            newIndex = proxy.mapToSource(newMdlIndex)
            newrecord = origmdl.record(newIndex.row())
            newseq = self._to_sequence(newrecord)

            self.uiSelected.setText(self._to_pretty_print(newseq))

            timestamp = newrecord.value("LastChanged")
            raw_data = self._format_raw_data(newrecord)

            self.lineEdit.setText(timestamp)
            self.uiRawData.setText(raw_data)

        if oldMdlIndex.isValid():
            oldIndex = proxy.mapToSource(oldMdlIndex)
            oldrecord = origmdl.record(oldIndex.row())
            oldseq = self._to_sequence(oldrecord)
            self.uiDeselected.setText(self._to_pretty_print(oldseq))

        if newMdlIndex.isValid() & oldMdlIndex.isValid():
            self.uiChangeSet.setText(self._format_before_after(newseq, oldseq))
    
    def _to_sequence(self, record):
        return [x for x in bytearray.fromhex(str(record.value("Data")))]
    
    def _format_before_after(self, newseq, oldseq):
        packetname, array = self.decoder.getDiffPackets(newseq, oldseq)
        mystring = "Packet: %s\n" % packetname
        for key, newval, oldval in array:
            mystring += "  {0}\n".format(key)
            mystring += "    {0:10s}\t{1}\n".format('after:', newval)
            mystring += "    {0:10s}\t{1}\n\n".format('before:', oldval)
        return mystring
        
    def _format_raw_data(self, record):
        data = str(record.value("Data"))
        string = ""
        for i in range(len(data)):
            string += data[i]
            if i > 0:
                if (i+1)%60 == 0:
                    string += "\n"
                elif (i+1)%20 == 0:
                    string += "\t"
                elif (i+1)%2 == 0:
                    string += " "
        return string
