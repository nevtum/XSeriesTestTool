'''
Created on 17/06/2011

@author: nEVSTER
'''

class insertToDBCommand(object):
    '''
    classdocs
    '''


    def __init__(self, data):
        self.data = data
        self.array = self.fillarray()
        
    def getByteVector(self, lbound, hbound):
        return self.data[lbound-1:hbound]
        
    def fillarray(self):
        hexdata = []
        hexdata.append(self.convert(self.getByteVector(1, 1)))
        hexdata.append(self.convert(self.getByteVector(2, 2)))
        hexdata.append(self.convert(self.getByteVector(3, 4)))
        hexdata.append(self.convert(self.getByteVector(6, 8)))
        hexdata.append(self.convert(self.getByteVector(9, 9)))
        hexdata.append(self.convert(self.getByteVector(10, 10)))
        hexdata.append(self.convert(self.getByteVector(11, 11)))
        hexdata.append(self.convert(self.getByteVector(12, 12)))
        hexdata.append(self.convert(self.getByteVector(13, 13)))
        hexdata.append(self.convert(self.getByteVector(15, 15)))
        hexdata.append(self.convert(self.getByteVector(16, 16)))
        hexdata.append(self.convert(self.getByteVector(17, 21)))
        hexdata.append(self.convert(self.getByteVector(22, 26)))
        hexdata.append(self.convert(self.getByteVector(27, 31)))
        hexdata.append(self.convert(self.getByteVector(32, 36)))
        hexdata.append(self.convert(self.getByteVector(37, 40)))
        hexdata.append(self.convert(self.getByteVector(42, 46)))
        hexdata.append(self.convert(self.getByteVector(47, 51)))
        hexdata.append(self.convert(self.getByteVector(52, 56)))
        hexdata.append(self.convert(self.getByteVector(57, 61)))
        hexdata.append(self.convert(self.getByteVector(62, 66)))
        hexdata.append(self.convert(self.getByteVector(67, 71)))
        hexdata.append(self.convert(self.getByteVector(72, 75)))
        hexdata.append(self.convert(self.getByteVector(76, 79)))
        hexdata.append(self.convert(self.getByteVector(80, 83)))
        hexdata.append(self.convert(self.getByteVector(84, 84)))
        hexdata.append(self.convert(self.getByteVector(85, 86)))
        hexdata.append(self.convert(self.getByteVector(88, 95)))
        hexdata.append(self.convert(self.getByteVector(96, 103)))
        hexdata.append(self.convert(self.getByteVector(104, 111)))
        hexdata.append(self.convert(self.getByteVector(112, 119)))
        hexdata.append(self.convert(self.getByteVector(120, 121)))
        hexdata.append(self.convert(self.getByteVector(122, 122)))
        return hexdata
    
    def convert(self, data):
        return int(''.join(data), 16)
    
    def item(self, n):
        return self.array[n]

        