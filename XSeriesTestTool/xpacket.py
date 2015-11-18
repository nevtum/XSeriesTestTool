
class XPacket:
	def __init__(self, time_generated, packet_type, data):
		self._time = time_generated
		self._packet_type = packet_type
		self._data = data
	
	def get_time(self):
		return self._time
	
	def get_type(self):
		return self._packet_type
	
	def get_data(self):
		return [x for x in bytearray.fromhex(self._data)]
	
	def pretty_print(self, decoder):
		packetname, array = decoder.getDecodedData(self.get_data())
		mystring = "Packet: %s\n" % packetname
		for key, value in array:
			mystring += "    {0:50s}\t{1}\n".format(key, value)
		return mystring
	
	def format_raw_data(self):
		string = ""
		for i in range(len(self._data)):
			string += self._data[i]
			if i > 0:
				if (i+1)%60 == 0:
					string += "\n"
				elif (i+1)%20 == 0:
					string += "\t"
				elif (i+1)%2 == 0:
					string += " "
		return string
	
	def get_differences(self, old_packet, decoder):
		newseq = self.get_data()
		oldseq = old_packet.get_data()
		packetname, array = decoder.getDiffPackets(newseq, oldseq)
		mystring = "Packet: %s\n" % packetname
		for key, newval, oldval in array:
			mystring += "  {0}\n".format(key)
			mystring += "    {0:10s}\t{1}\n".format('after:', newval)
			mystring += "    {0:10s}\t{1}\n\n".format('before:', oldval)
		return mystring