from PyQt4.QtCore import QObject, SIGNAL

class Publisher(QObject):
	def __init__(self, parent = None):
		QObject.__init__(self, parent)

	def notify_unexpected_length(self, packet_info, data):
		self.emit(SIGNAL("UNEXPECTED_PACKET_LENGTH"), packet_info, data)
			
	def notify_packet_received(self, packet_type, data):
		self.emit(SIGNAL("VALID_PACKET_RECEIVED"), packet_type, data)
	
	def notify_unknown_packet_received(self, data):
		self.emit(SIGNAL("INVALID_PACKET_RECEIVED"), data)