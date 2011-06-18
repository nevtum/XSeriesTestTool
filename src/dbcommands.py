'''
Created on 17/06/2011

@author: nEVSTER
'''
import sqlite3

class createsdbtablecommand:
    def __init__(self, database):
        self.database = database
    def execute(self):
        try:
            self.__createtable()
        except sqlite3.OperationalError:
            print "error creating tables"
    def __createtable(self):
        metadata = {
        'ID': 'INTEGER',
        'VersionNr': 'INTEGER',
        'GMID': 'INTEGER',
        'Idle': 'INTEGER',
        'GameCycle': 'INTEGER',
        'PowerUP': 'INTEGER',
        'Reset': 'INTEGER',
        'CCCETxComplete': 'INTEGER', # metadata to be used for easier changes to columns
        'LargeWin': 'INTEGER',
        'CollectCash': 'INTEGER',
        'CancelCredit': 'INTEGER',
        'ProgressiveWin': 'INTEGER',
        'ManufacturerWin0': 'INTEGER',
        'ManufacturerWin1': 'INTEGER',
        'ManufacturerWin2': 'INTEGER'}
        string = ['%s %s' % kvpair for kvpair in metadata.iteritems()]
        table_info = ', '.join(string)
        cursor = self.database.cursor()
        sql = """CREATE TABLE Packets(%s)""" % table_info
        cursor.execute(sql)

class insertToDBCommand(object):
    def __init__(self, data, database):
        self.data = data
        self.array = self.fillarray()
        self.database = database
        
    def execute(self):
        cursor = self.database.cursor()
        values = ','.join([str(x) for x in self.array[1:16]]) # must deal with all values in array
        sql = '''INSERT INTO Packets VALUES(%s)''' % values
        cursor.execute(sql)
        
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
    
class selectallsdbcommand:
    def __init__(self, database):
        self.database = database
    def execute(self):
        cursor = self.database.cursor()
        query = 'SELECT * FROM Packets'
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # for debugging purposes
        for each in rows:
            values = ['0x%x' % item for item in each] 
            print values
            
        return rows
    
f = open('sdbmockdata.txt', 'r')
data = f.readline().split()
database = sqlite3.connect('new.sqlite')
command1 = createsdbtablecommand(database)
command2 = insertToDBCommand(data, database)
command3 = selectallsdbcommand(database)
command1.execute()
command2.execute()
command3.execute()
database.commit()
database.close()

        