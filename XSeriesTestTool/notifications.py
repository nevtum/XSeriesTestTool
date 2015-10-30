from PyQt4.QtCore import QObject, SIGNAL

def notify_unexpected_length(packet_info, data):
	QObject.emit(SIGNAL("UNEXPECTED_PACKET_LENGTH"), packet_info, data)
        
def notify_packet_received(packet_type, data):
	QObject.emit(SIGNAL("VALID_PACKET_RECEIVED"), packet_type, data)

def notify_unknown_packet_received(data):
	QObject.emit(SIGNAL("UNEXPECTED_PACKET_RECEIVED"), data)