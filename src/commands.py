'''
Created on 29/04/2011

@author: ntummon
'''

class MDLCommand:
    def __init__(self, list, model):
        self.list = list # must ensure a deep copy
        self.mdl = model
    def execute(self):
        self.mdl.setdata(self.list)