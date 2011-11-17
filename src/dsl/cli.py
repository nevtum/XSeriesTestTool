'''
Created on Nov 17, 2011

@author: nEVSTER
'''
from threading import Thread

class MyDSL(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.recording = False
    
    def run(self):
        while True:
            x = raw_input('> ')
            self.process(x)
    
    def process(self, commandstring):
        if commandstring == "record start":
            if self.recording == True:
                print "already recording script"
            else:
                self.recording = True
                print "recording script session..."
        elif commandstring == "record stop":
            if self.recording == False:
                print "no recording session started"
            else:
                self.recording = False
                print "recording session stopped"
                
        elif commandstring == "set dooropen on":
            print "setting dooropen bit to ON"
        
        elif commandstring == "set dooropen off":
            print "setting dooropen bit to OFF"
        
        else:
            print "unrecognized command"

g = MyDSL()
g.start()