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
        self.cursor.execute("PRAGMA foreign_keys = ON") 
        query = """CREATE TABLE Packets(
        date TEXT,
        assetnr INTEGER,
        packetversion INTEGER,
        idle INTEGER,
        gamecycle INTEGER,
        powerup INTEGER,
        reset INTEGER,
        cccetxcomplete INTEGER,
        largewin INTEGER,
        collectcash INTEGER,
        cancelcredit INTEGER,
        progressivewin INTEGER,
        manufacturerwin0 INTEGER,
        manufacturerwin1 INTEGER,
        manufacturerwin2 INTEGER,
        dooropen INTEGER,
        cageopen INTEGER,
        displayerror INTEGER)"""
        self.cursor.execute(query)
        query = """CREATE TABLE foo(
        displayerror INTEGER,
        FOREIGN KEY(hey) REFERENCES Packets(assetnr))"""
        self.cursor.execute(query)
    
    def __del__(self):
        self.connection.close()
        
    def update(self, packet):
        string = "'%s'" % datetime.now()
        string += ',%s' % packet.GMID()
        string += ',%s' % packet.versionNr()
        string += ',%s' % packet.idle()
        string += ',%s' % packet.gameCycle()
        string += ',%s' % packet.powerUp()
        string += ',%s' % packet.reset()
        string += ',%s' % packet.ccceTxComplete()
        string += ',%s' % packet.largeWin()
        string += ',%s' % packet.collectCash()
        string += ',%s' % packet.cancelCredit()
        string += ',%s' % packet.progressiveWin()
        string += ',%s' % packet.manufacturerWin0()
        string += ',%s' % packet.manufacturerWin1()
        string += ',%s' % packet.manufacturerWin2()
        string += ',%s' % packet.doorOpen()
        string += ',%s' % packet.logicCageOpen()
        string += ',%s' % packet.displayError()
        sql = '''INSERT INTO Packets
        VALUES(%s)''' % string
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