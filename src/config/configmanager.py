'''
Created on Sep 17, 2011

@author: nEVSTER
'''

import os
from xml.etree import cElementTree
from config.metaclasses import *

# This repository is a dictionary of all meta objects.
# All knowledge of every type of packet can be found
# in the meta repository
class metaRepository:
    def __init__(self, filepath):
        self.filepath = filepath
        self.collection = {}
        self.__createRepository()
        
    def __createRepository(self):
        dupes = set()
        for cmo in self.__allMetaObjects():
            t = cmo.getPacketName(), cmo.getPacketLength(), cmo.getPacketPattern()
            if t in dupes:
                raise IndexError('Duplicate metadata!!')
            dupes.add(t)
            self.collection[cmo.getPacketPattern()] = cmo
        if (len(self.collection) == 0):
            raise ValueError('No metadata found!!')
            
    def __allMetaObjects(self):
        for root, dirs, files in os.walk(self.filepath):
            for file in files:
                pathname = os.path.join(root, file)
                if 'xml' in pathname:
                    tree = cElementTree.ElementTree()
                    tree.parse(pathname)
                    for each in tree.findall('.//packet'):
                        yield codecMetaObject(each)
                        
    def getMetaObject(self, key):
        obj = self.collection.get(key)
        if(obj is None):
            return NullMetaObject()
        return obj