'''
Created on 17/06/2011

@author: nEVSTER
'''
import sqlite3
from time import strftime
from xml.dom import minidom

class createSDBTableCommand:
    def __init__(self, database):
        self.database = database
        self.meta_elems = self.getmetaitems('packets.xml')

    def getmetaitems(self, filename):
        xml = minidom.parse(filename)
        meta_elems = []
        for ch in xml.firstChild.childNodes:
            if ch.nodeType == 1:
                #t = ch.firstChild.nextSibling
                #t.firstChild.data
                meta_elems.append(ch.localName)
        return meta_elems

    def execute(self):
        try:
            self.createtable()
            createEventTableCommand(self.database).execute()
        except sqlite3.OperationalError:
            print "error creating tables"

    def createtable(self):
        meta  = [('EventID', 'INTEGER PRIMARY KEY')]
        for item in self.meta_elems:
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
        self.meta_elems = self.getmetaitems('packets.xml')
        
    def getmetaitems(self, filename):
        xml = minidom.parse(filename)
        meta_elems = []
        for ch in xml.firstChild.childNodes:
            if ch.nodeType == 1:
                #t = ch.firstChild.nextSibling
                #t.firstChild.data
                meta_elems.append(ch.localName)
        return meta_elems
        
    def execute(self):
        cursor = self.database.cursor()
        columns = ','.join(self.meta_elems)
        sql = '''INSERT INTO Packets(%s) VALUES(%s)''' % (columns, str(self.array).strip('[]'))
        cursor.execute(sql)
        vec = (strftime('"%Y-%m-%d %H:%M:%S"'), '"EGM"')
        sql = '''INSERT INTO Event(DateTime, Source) Values(%s,%s)''' % vec
        cursor.execute(sql)
        
    def getByteVector(self, lbound, hbound):
        return self.data[lbound-1:hbound]
        
    def fillarray(self):
        ranges = [(2,2), (3,4), (6,8), (9,9), (10,10), (11,11), # utilise metadata instead
                       (12,12), (13,13), (15,15), (16,16), (17,21),
                       (22,26), (27,31), (32,36), (37,40), (42,46),
                       (47,51), (52,56), (57,61), (62,66), (67,71),
                       (72,75), (76,79), (80,83), (84,84), (85,86),
                       (88,95), (96,103), (104,111), (112,119),
                       (120,121), (122,122)]
        
        hexdata = []
        for lbound, hbound in ranges:
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
database = sqlite3.connect('z.sqlite')
command1 = createSDBTableCommand(database)
command2 = insertToDBCommand(data, database)
command3 = viewDBCommand(database)
command1.execute()
command2.execute()
command3.execute()
database.commit()
database.close()

        
