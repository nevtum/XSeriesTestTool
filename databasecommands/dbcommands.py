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
        
    def fillarray(self):
        hexdata = []
        hexdata.append(self.convert(self.data[2:3]))
        return hexdata
    
    def convert(self, data):
        x = ''.join(data)
        return int(x, 16)
    
    def item(self, n):
        return self.array[n]

        