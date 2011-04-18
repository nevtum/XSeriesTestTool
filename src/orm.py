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
        #try:
        self.createnewtables()
        #except sqlite3.OperationalError:
        #    print "tables exists"
            
    def createnewtables(self):
        try:
            self.cursor.execute("PRAGMA foreign_keys = ON") 
            query = """CREATE TABLE Packets(
            eventID INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            GMID INTEGER,
            version TEXT)"""
            self.cursor.execute(query)
            
            query = """CREATE TABLE statusbytes(
            eventID INTEGER PRIMARY KEY AUTOINCREMENT,
            idle INTEGER,
            gamecycle INTEGER)"""
            self.cursor.execute(query)
        except:
            pass
    
    def __del__(self):
        #assumes connection is open, you have been warned!
        self.connection.close()
        
    def update(self, packet):
        string = "'%s'" % datetime.now()
        string += ',%s' % packet.GMID()
        string += ',%s' % packet.versionNr()
        sql = '''INSERT INTO Packets(date, GMID, version)
        VALUES(%s)''' % string
        self.cursor.execute(sql)
        
        string2 = '%s' % packet.idle()
        string2 += ',%s' % packet.gameCycle()
        sql = '''INSERT INTO statusbytes(idle, gamecycle)
        VALUES(%s)''' % string2
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