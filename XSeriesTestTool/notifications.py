from PyQt4.QtCore import QObject, SIGNAL

class Publisher(QObject):
	def __init__(self, parent = None):
		QObject.__init__(self, parent)

	def notify_unexpected_length(self, packet_info, data):
		self.emit(SIGNAL("UNEXPECTED_PACKET_LENGTH"), packet_info, data)
			
	def notify_packet_received(self, packet):
		self.emit(SIGNAL("VALID_PACKET_RECEIVED"), packet)
	
	def notify_unknown_packet_received(self, packet):
		self.emit(SIGNAL("INVALID_PACKET_RECEIVED"), packet)

class ViewActions(QObject):
	def __init__(self, parent = None):
		QObject.__init__(self, parent)
	
	def navigate_next_entry(self):
		self.emit(SIGNAL("NEXT_ENTRY_NAVIGATED"))
		
	def navigate_prev_entry(self):
		self.emit(SIGNAL("PREVIOUS_ENTRY_NAVIGATED"))

	def navigate_first_entry(self):
		self.emit(SIGNAL("FIRST_ENTRY_NAVIGATED"))
	
	def navigate_final_entry(self):
		self.emit(SIGNAL("FINAL_ENTRY_NAVIGATED"))
		
	def start_recording(self, port):
		self.emit(SIGNAL("RECORDING_STARTED"), port)
		
	def stop_recording(self):
		self.emit(SIGNAL("RECORDING_STOPPED"))