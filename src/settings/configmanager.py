'''
Created on Sep 17, 2011

@author: nEVSTER
'''

import os
import hashlib
from xml.etree import cElementTree
from config.metaclasses import codecMetaObject

def allmetaobjects():
    for tuple in os.walk('.'):
        for file in tuple[2]:
            if 'xml' in file:
                tree = cElementTree.ElementTree()
                tree.parse(file)
                for eachmeta in tree.findall('.//packet'):
                    yield eachmeta

for obj in allmetaobjects():
    cmo = codecMetaObject(obj)
    print cmo.getPacketLength(), cmo.getPacketName()