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
        print "<********** SDB ***********>"
        self.printmachineinfo(self.sdbmdl)
        self.printstatusbytes(self.sdbmdl)
        self.printmeters(self.sdbmdl)
        self.printSEFPorts(self.sdbmdl)
        self.printprogramIDs(self.sdbmdl)
        self.printRTP(self.sdbmdl)
        self.printLinkProgSupport(self.sdbmdl)
        print ""
        
class mdbreporter:
    def __init__(self, mdbmodel):
        assert (isinstance(mdbmodel, mdbMdl))
        self.mdbmdl = mdbmodel
        self.mdbmdl.register(self)
        
    def update(self):
        print "<========== MDB ===========>"
        print "GMID:                     %s" % self.mdbmdl.GMID()
        print "Version nr:               %s" % self.mdbmdl.versionNr()
        print "Packet Type:              %s" % self.mdbmdl.mdbType()
        print "Stacker Door Open:        %s" % self.mdbmdl.stackerDoorOpen()
        print "Stacker Comms Error:      %s" % self.mdbmdl.stackerCommsError()
        print "Stacker Failure:          %s" % self.mdbmdl.stackerFailure()
        print "Stacker Full:             %s" % self.mdbmdl.stackerFull()
        print "Stacker Removed:          %s" % self.mdbmdl.stackerRemoved()
        print "Stacker Disabled:         %s" % self.mdbmdl.stackerOutOfService()
        print "Cashbox Door Open:        %s" % self.mdbmdl.cashBoxDropDoorOpen()
        print "Printer Paper Low:        %s" % self.mdbmdl.printerPaperLow()
        print "Valid Ticket Out:         %s" % self.mdbmdl.validTicketOut()
        print "Printer Fault:            %s" % self.mdbmdl.printerFault()
        print "Paper Empty:              %s" % self.mdbmdl.paperEmpty()
        print "Valid Ticket In:          %s" % self.mdbmdl.validTicketIn()
        print "Ticket In Comms Err:      %s" % self.mdbmdl.ticketInCommsError()
        print "Ticket Reject (Host):     %s" % self.mdbmdl.ticketInRejectedByHost()
        print "Ten Rejects:              %s" % self.mdbmdl.tenRejects()
        print "Misc. Ticket In Err:      %s" % self.mdbmdl.miscTicketInError()
        print "Ticket < BCV              %s" % self.mdbmdl.ticketLowerThanBCV()
        print "Ticket Stacking Done:     %s" % self.mdbmdl.ticketStackingDone()
        print "No. $5 Notes:             %s" % self.mdbmdl.nr5DollarNotes()
        print "No. $10 Notes:            %s" % self.mdbmdl.nr10DollarNotes()
        print "No. $20 Notes:            %s" % self.mdbmdl.nr20DollarNotes()
        print "No. $50 Notes:            %s" % self.mdbmdl.nr50DollarNotes()
        print "No. $100 Notes:           %s" % self.mdbmdl.nr100DollarNotes()
        print "Tickets Accepted:         %s" % self.mdbmdl.ticketsAccepted()
        print "Tickets Rejected:         %s" % self.mdbmdl.ticketsRejected()
        print "Tot. Spare Bills:         %s" % self.mdbmdl.totBillsAcceptedSpare()
        print "Value Bills Accepted:     %s" % self.mdbmdl.valBillsAccepted()
        print "Tot. Bills Accepted:      %s" % self.mdbmdl.totBillsAccepted()
        print "Date Ticket Print:        %s" % self.mdbmdl.dateTicketPrinted()
        print "Time Ticket Print:        %s" % self.mdbmdl.timeTicketPrinted()
        print "Printer ID:               %s" % self.mdbmdl.printerID()
        print "Ticket Amount:            %s" % self.mdbmdl.ticketAmount()
        print "Sequential #:             %s" % self.mdbmdl.sequentialNr()
        print "Hopper Configured:        %s" % self.mdbmdl.hopperConfigured()
        print "BNA Configured:           %s" % self.mdbmdl.BNAConfigured()
        print "Printer Configured:       %s" % self.mdbmdl.printerConfigured()
        print "Std Prog Done:            %s" % self.mdbmdl.stdProgPayDone()
        print "Myst Prog Done:           %s" % self.mdbmdl.mystProgPayDone()
        print "CCCE Tx Complete:         %s" % self.mdbmdl.ccceTxComplete()
        print "Myst Prog Win:            %s" % self.mdbmdl.mystProgWin()
        print "Std Prog Win Notified:    %s" % self.mdbmdl.stdProgWinNotification()
        print "Myst Prog Win Notified:   %s" % self.mdbmdl.mystProgWinNotification()
        print "CCCE Inc/Dec              %s" % self.mdbmdl.ccceIncDec()
        print "Std Prog Payment:         %s" % self.mdbmdl.stdProgPayment()
        print "Myst Prog Payment:        %s" % self.mdbmdl.mystProgPayment()
        print "Std Prog Pool Val:        %s" % self.mdbmdl.stdProgPoolVal()
        print "Myst Prog Pool Val:       %s" % self.mdbmdl.mystProgPoolVal()
        print "Ticket In Port1 Set:      %s" % self.mdbmdl.ticketInPort1Set()
        print "Time Broadcast Set:       %s" % self.mdbmdl.timeBroadcastSet()
        print "Amount Std Prog Win:      %s" % self.mdbmdl.amtStdProgWin()
        print "Amount Myst Prog Win:     %s" % self.mdbmdl.amtMystProgWin()
        print "Amount CCCE Tx In:        %s" % self.mdbmdl.amtCCCETxIn()
        print "Amount Ticket Out:        %s" % self.mdbmdl.amtTicketOut()
        print "Amount Ticket In:         %s" % self.mdbmdl.amtTicketIn()
        print ""