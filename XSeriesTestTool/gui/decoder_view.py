"""
XSeriesTestTool - A NSW gaming protocol decoder/analyzer
    Copyright (C) 2012  Neville Tummon

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from PyQt4 import uic
from PyQt4.QtCore import SIGNAL

decbase, decform = uic.loadUiType("gui/packetview.ui")

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
