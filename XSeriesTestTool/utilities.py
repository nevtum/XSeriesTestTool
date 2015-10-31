
def convert_to_hex_string(byte_array):
	hexstring = ''.join(["%02X" % byte for byte in byte_array])
	return hexstring

def convert_to_byte_array(hexstring):
	byte_array = []
	length = len(hexstring)-1
	for i in range(length):
		nibble = "%s%s" % (hexstring[i], hexstring[i+1])
		byte_array.append(int(nibble, 16))
	return byte_array