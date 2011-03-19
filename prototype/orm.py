'''
Created on 19/03/2011

@author: ntummon
'''
import os
import sqlite3

class SDBORM(object):

    def __init__(self, path):
        if not os.path.exists(path):
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
            query = """CREATE TABLE Packets (packetid INTEGER,
            gmid INTEGER,
            statusbyte INTEGER)"""
            self.cursor.execute(query)
        else:
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
    
    def __del__(self):
        self.connection.close()
        
    def insert(self, *packet):
        assert(len(packet) == 3)
        sql = "INSERT INTO Packets VALUES(%i, %i, %i)" % tuple(packet)
        print sql
        self.cursor.execute(sql)
        self.connection.commit()
        
    def fetchall(self):
        self.cursor.execute("SELECT * FROM Packets")
        self.connection.commit()
        return self.cursor.fetchall()