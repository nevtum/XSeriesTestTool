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

from config.configmanager import metaRepository
from decoder import *
from views import QtSQLWrapper
from comms_threads import ListenThread
from notifications import Publisher

class TransmissionFactory:
    def __init__(self, parent):
        self.publisher = Publisher()
        self.xdec = self._build_protocol_decoder()
        self.sqlwrapper = QtSQLWrapper("test.db", self.publisher, parent)
        self.serial_thread = ListenThread(self.xdec, self.publisher, parent)
    
    def _build_protocol_decoder(self):
        xmetadata = metaRepository('settings/')
        decoder = XProtocolDecoder(xmetadata)
        decoder.registerTypeDecoder('integer-reverse', reverseIntegerDecoder)
        decoder.registerTypeDecoder('currency-reverse', reverseCurrencyDecoder)
        decoder.registerTypeDecoder('boolean', booleanDecoder)
        decoder.registerTypeDecoder('ascii-reverse', reverseAsciiDecoder)
        return decoder

    def getProtocolDecoder(self):
        return self.xdec
    
    def getQtSQLWrapper(self):
        return self.sqlwrapper
    
    def get_serial_thread(self):
        return self.serial_thread