'''
Created on 17/06/2011

@author: nEVSTER
'''
import sqlite3
from time import strftime
from xml.dom import minidom

def getmetaitems():
    xml = minidom.parse('packets.xml')
    meta_elems = []
    for ch in xml.firstChild.childNodes:
        if ch.nodeType == 1:
            #t = ch.firstChild.nextSibling
            #t.firstChild.data
            meta_elems.append(ch.localName)
    return meta_elems

def getmetaranges():
    xml = minidom.parse('packets.xml')
    meta_ranges = []
    for ch in xml.firstChild.childNodes:
        if ch.nodeType == 1:
            x = ch.attributes
            try:
                meta_ranges.append((int(x['startbyte'].value), int(x['endbyte'].value)))
            except KeyError:
                meta_ranges.append((int(x['byte'].value), int(x['byte'].value)))
    return meta_ranges

class createSDBTableCommand:
    def __init__(self, database):
        self.database = database

    def execute(self):
        try:
            self.createtable()
            createEventTableCommand(self.database).execute()
        except sqlite3.OperationalError:
            print "error creating tables"

    def createtable(self):
        meta = [('EventID', 'INTEGER PRIMARY KEY')]
        for item in getmetaitems():
            meta.append((item.encode(), 'TEXT'))
        string = ['%s %s' % kvpair for kvpair in meta]
        table_info = ', '.join(string)
        cursor = self.database.cursor()
        sql = """CREATE TABLE Packets(%s)""" % table_info
        cursor.execute(sql)
        
class createEventTableCommand:
    def __init__(self, database):
        self.database = database
        
    def execute(self):
        cursor = self.database.cursor()
        sql = """CREATE TABLE Event(ID INTEGER PRIMARY KEY, DateTime TEXT, Source TEXT)"""
        cursor.execute(sql)

class insertToDBCommand(object):
    def __init__(self, data, database):
        self.data = data
        self.fillarray()
        self.database = database
        
    def execute(self):
        cursor = self.database.cursor()
        columns = ','.join(getmetaitems())
        sql = '''INSERT INTO Packets(%s) VALUES(%s)''' % (columns, str(self.array).strip('[]'))
        cursor.execute(sql)
        vec = (strftime('"%Y-%m-%d %H:%M:%S"'), '"EGM"')
        sql = '''INSERT INTO Event(DateTime, Source) Values(%s,%s)''' % vec
        cursor.execute(sql)
        
    def getByteVector(self, lbound, hbound):
        return self.data[lbound - 1:hbound]
        
    def fillarray(self):
        hexdata = []
        for lbound, hbound in getmetaranges():
            hexdata.append(self.convert(self.getByteVector(lbound, hbound)))
            
        self.array = hexdata # needed for SQL Query
    
    def convert(self, data):
        return ''.join(data)
    
    def item(self, n):
        return self.array[n]
    
    def get(self, key):
        return self.dictionary[key]
    
class viewDBCommand:
    def __init__(self, database):
        self.database = database
    def execute(self):
        cursor = self.database.cursor()
        query = '''SELECT
        EV.*,
        P.*
        FROM Packets P
        JOIN Event EV
        ON EV.ID = P.EventID'''
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # for debugging purposes
        for each in rows:
            print each
            pass
            
        return rows
    
f = open('sdbmockdata.txt', 'r')
data = f.readline().split()
database = sqlite3.connect(':memory:')
command1 = createSDBTableCommand(database)
command2 = insertToDBCommand(data, database)
command3 = viewDBCommand(database)
command1.execute()
command2.execute()
command3.execute()
database.commit()
database.close()

        

