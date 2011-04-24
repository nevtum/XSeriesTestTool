'''
Created on 19/03/2011

@author: ntummon
'''
import os
from datetime import datetime
import sqlite3
from datablockmodels import *

class createsdbtablecommand:
    def __init__(self, database):
        self.database = database
    def execute(self):
        try:
            self.__createtable()
        except sqlite3.OperationalError:
            print "error creating tables"
    def __createtable(self):
        cursor = self.database.cursor()
        query = """CREATE TABLE Packets(
            eventID INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            GMID INTEGER,
            version TEXT)"""
        cursor.execute(query)
        query = """CREATE TABLE statusbytes(
            eventID INTEGER PRIMARY KEY AUTOINCREMENT,
            idle INTEGER,
            gamecycle INTEGER,
            powerup INTEGER,
            reset INTEGER)"""
        cursor.execute(query)
        
class insertsdbcommand:
    def __init__(self, sdbmdl, database):
        self.sdbmdl = sdbmdl
        self.database = database
    def execute(self):
        assert(self.sdbmdl) # assert sdbmdl still in scope
        cursor = self.database.cursor()
        string = "'%s'" % datetime.now()
        string += ',%s' % self.sdbmdl.GMID()
        string += ',%s' % self.sdbmdl.versionNr()
        sql = '''INSERT INTO Packets(date,
        GMID,
        version)
        VALUES(%s)''' % string
        cursor.execute(sql)
        string2 = '%s' % self.sdbmdl.idle()
        string2 += ',%s' % self.sdbmdl.gameCycle()
        string2 += ',%s' % self.sdbmdl.powerUp()
        string2 += ',%s' % self.sdbmdl.reset()
        sql = '''INSERT INTO statusbytes(idle
        , gamecycle
        , powerup
        , reset)
        VALUES(%s)''' % string2
        cursor.execute(sql)

class selectallsdbcommand:
    def __init__(self, database):
        self.database = database
    def execute(self):
        cursor = self.database.cursor()
        query = 'SELECT * FROM Packets'
        cursor.execute(query)
        rows = cursor.fetchall()
        for each in rows:
            print each
        
f = open('sdbmockdata.txt', 'r')
data = f.readline().split()
sdb = sdbMdl()
sdb.setdata(data)
database = sqlite3.connect('new.sqlite')
command1 = createsdbtablecommand(database)
command2 = insertsdbcommand(sdb, database)
command3 = selectallsdbcommand(database)
command1.execute()
command2.execute()
command3.execute()