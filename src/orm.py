'''
Created on 19/03/2011

@author: ntummon
'''
import os
from datetime import datetime
import sqlite3
from datablockmodels import *

class SDBORM(object):

    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        try:
            self.createnewtables()
        except sqlite3.OperationalError:
            print "tables exists"
            
    def createnewtables(self):
        query = """CREATE TABLE Packets(
        id INTEGER PRIMARY KEY,
        date TEXT,
        assetnr INTEGER,
        packetversion INTEGER)"""
        self.cursor.execute(query)
    
    def __del__(self):
        self.connection.close()
        
    def update(self, packet):
        string = "'%s'" % datetime.now()
        string += ',%s' % packet.GMID()
        string += ',%s' % packet.versionNr()
        sql = '''INSERT INTO Packets(date, assetnr, packetversion)
        VALUES(%s)''' % string
        print sql
        self.cursor.execute(sql)
        self.connection.commit()
        
    def fetchall(self):
        self.cursor.execute("SELECT * FROM Packets")
        self.connection.commit()
        return self.cursor.fetchall()
    
f = open('sdbmockdata.txt', 'r')
data = f.readline().split()
sdb = sdbMdl()
sdb.setdata(data)
x = SDBORM('sdb.db')
x.update(sdb)
rows = x.fetchall()
for each in rows:
    print each