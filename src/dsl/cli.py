'''
Created on Nov 17, 2011

@author: nEVSTER
'''
from threading import Thread

class ScriptRecorder:
    def __init__(self):
        self.recording = False
    def enable(self):
        self.recording = True
        print "Recording script to file..."
    def disable(self):
        self.recording = False
        print "Finished recording script"
    def RecordCommand(self, string):
        if self.recording:
            print "recorded: '%s'" % string

class SetCommand:
    def __init__(self, *args):
        self.args = args
    ''' deals with tickboxes, possible radio boxes'''
    def execute(self):
        if self.args[1] == "on":
            print self.args[0], "tickbox set to ON"
        elif self.args[1] == "off":
            print self.args[0], "tickbox set to OFF"
        else:
            raise ValueError

class CommandRepository:
    def __init__(self):
        self.repo = {}
    def Register(self, cmdString, commandObj):
        if self.repo.get(cmdString):
            print "command string exists"
            return
        self.repo[cmdString] = commandObj
    def Unregister(self, cmdString):
        self.repo.pop(cmdString)
    def GetCommandObj(self, key, *args):
        return self.repo.get(key)(*args)

class MyDSL(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.recorder = ScriptRecorder()
        self.cmdRepo = CommandRepository()
        self.cmdRepo.Register("set", SetCommand)
    
    def run(self):
        while True:
            x = raw_input('> ')
            try:
                self.process(x)
            except:
                print "unrecognized command"
    
    def changedRecording(self, list):
        if list[0] == "record":
            if list[1] == "start":
                self.recorder.enable()
            elif list[1] == "stop":
                self.recorder.disable()
            else:
                raise ValueError
            return True
        return False
         
    def process(self, commandstring):
        g = commandstring.lower().split()
        if self.changedRecording(g):
            return
        key = g[0]
        args = g[1:]
        cmd = self.cmdRepo.GetCommandObj(key, *args)
        cmd.execute()
        self.recorder.RecordCommand(commandstring)

g = MyDSL()
g.start()