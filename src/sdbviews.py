'''
Created on 09/03/2011

@author: ntummon
'''
from datablockmodels import *

class sdbreporter:
    def __init__(self, sdbmodel):
        assert (isinstance(sdbmodel, sdbMdl))
        self.sdbmdl = sdbmodel
        self.sdbmdl.register(self)

    def printmachineinfo(self, packet):
        print "Version #:               %s" % packet.versionNr()
        print "Machine ID:              %s" % packet.GMID()
        print "Machine Idle:            %s" % packet.idle()

    def printmeters(self, packet):
        print "Turnover:                %s" % packet.turnover()
        print "Total Wins:              %s" % packet.totalWins()
        print "Cash Box:                %s" % packet.cashBox()
        print "Cancelled Credits:       %s" % packet.cancelledCredits()
        print "Games Played:            %s" % packet.gamesPlayed()
        print "Money In:                %s" % packet.moneyIn()
        print "Money Out:               %s" % packet.moneyOut()
        print "Cash In:                 %s" % packet.cashIn()
        print "Cash Out:                %s" % packet.cashOut()
        print "Current Credits:         %s" % packet.credits()
        print "Misc. Accrual:           %s" % packet.miscAccrual()
        print "Number Power Ups:        %s" % packet.nrpowerUps()
        print "Games Since Reboot:      %s" % packet.gamesSinceReboot()
        print "Games Since Door Open:   %s" % packet.gamesSinceDoorOpen()
        print "Base Credit Value:       %s" % packet.baseCreditValue()

    def printstatusbytes(self, packet):
        print "Game Cycle:              %s" % packet.gameCycle()
        print "Powered Up:              %s" % packet.powerUp()
        print "Reset:                   %s" % packet.reset()
        print "CCCE Tx Complete         %s" % packet.ccceTxComplete()
        print "Large Win:               %s" % packet.largeWin()
        print "Collect Cash:            %s" % packet.collectCash()
        print "Cancel Credit:           %s" % packet.cancelCredit()
        print "Progressive Win:         %s" % packet.progressiveWin()
        print "Manufacturer Win1:       %s" % packet.manufacturerWin0()
        print "Manufacturer Win2:       %s" % packet.manufacturerWin1()
        print "Manufacturer Win3:       %s" % packet.manufacturerWin2()
        print "Door Opened:             %s" % packet.doorOpen()
        print "Logic Cage Opened:       %s" % packet.logicCageOpen()
        print "Display Error:           %s" % packet.displayError()
        print "Self Audit Error:        %s" % packet.selfAuditError()
        print "Memory Error:            %s" % packet.memoryError()
        print "Cash Input Error:        %s" % packet.cashInputError()
        print "Audit Mode:              %s" % packet.auditMode()
        print "Test Mode:               %s" % packet.testMode()
        print "Power Save Mode:         %s" % packet.powerSaveMode()
        print "SubsEquip Pay Suspended  %s" % packet.subsEquipPaySuspended()
        print "Mech Meter Disconnected  %s" % packet.mechMeterDisconnected()
        print "Manufacturer Error1:     %s" % packet.manufacturerError0()
        print "Manufacturer Error2:     %s" % packet.manufacturerError1()
        print "Cancel Credit Error:     %s" % packet.cancelCreditError()

    def printSEFPorts(self, packet):
        print "SEF Port 1               %s" % packet.port1Status()
        print "SEF Port 2               %s" % packet.port2Status()
        print "SEF Port 3               %s" % packet.port3Status()
        print "SEF Port 4               %s" % packet.port4Status()
        print "SEF Port 5               %s" % packet.port5Status()
        print "SEF Port 6               %s" % packet.port6Status()

    def printprogramIDs(self, packet):
        print "Program ID 1:            %s" % packet.programID1()
        print "Program ID 2:            %s" % packet.programID2()
        print "Program ID 3:            %s" % packet.programID3()
        print "Program ID 4:            %s" % packet.programID4()

    def printRTP(self, packet):
        print "PRTP:                    %s" % packet.prtp()

    def printLinkProgSupport(self, packet):
        print "Link Progr. Supported:   %s" % packet.linkedProgSupported()

    def update(self):
        self.printmachineinfo(self.sdbmdl)
        self.printstatusbytes(self.sdbmdl)
        self.printmeters(self.sdbmdl)
        self.printSEFPorts(self.sdbmdl)
        self.printprogramIDs(self.sdbmdl)
        self.printRTP(self.sdbmdl)
        self.printLinkProgSupport(self.sdbmdl)
        print ""