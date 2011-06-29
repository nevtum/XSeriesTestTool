from xml2dict import *

class subject:
    def __init__(self):
        self.observers = []
    def register(self, observer):
        self.observers.append(observer)
    def notifysubscribers(self):
        for each in self.observers:
            each.update()

class packetmdl:
    def packetinfo(self):
        pass
    
    def setdata(self, data):
        pass

class sdbMdl(packetmdl, subject):
    def readmetadata(self, filename):
        self.metadata = createmetadata(filename)
        self.statbyte = []
        self.statbyte.append(self.metadata.statusbyte1) 
        self.statbyte.append(self.metadata.statusbyte2)
        self.statbyte.append(self.metadata.statusbyte3) 
        self.statbyte.append(self.metadata.statusbyte4)
        
    def finditem(self, part):
        if self.metadata.__getitem__(part) is not None: # ugly ugly ugly
            return self.metadata.__getitem__(part)
        for statusbyte in self.statbyte:
            if statusbyte.__getitem__(part) is not None:
                return statusbyte.__getitem__(part)
        
    def getitem(self, part):
        item = self.finditem(part)
        if item['type'] == 'integer':
            print "part is an integer"
            lbound = int(item['startbyte'])
            hbound = int(item['endbyte'])
            return self.getByteString(lbound, hbound)
        elif item['type'] == 'bool':
            byte = 9 # magicnumber yaaaaaaaaay!!
            bit = int(item['bit'])
            return self.getBit(int(self.data[byte], 16), bit)
        elif item['type'] == 'currency':
            print "part is expressed in dollars"
        elif item['type'] == 'currency':
            print "part is expressed in dollars"
        else:
            raise IndexError

    def setdata(self, data):
        assert(data[1] == '00')
        assert(len(data) == 128)
        self.data = data
        self.notifysubscribers() # notify observers
    def packetinfo(self):
        return 'SDB'
    def getBit(self, byte, n):
        if ((byte >> n) & 0x1):
            return True
        else:
            return False
    def getByteVector(self, lbound, hbound):
        return self.data[hbound-1:lbound-2:-1]
    def getByteString(self, lbound, hbound):
        return ''.join(self.getByteVector(lbound, hbound))
    def versionNr(self):
        string = '%s.%s' % tuple(self.getByteVector(3, 4))
        return string.lstrip('0')
    def GMID(self):
        return self.getByteString(6, 8)
    def idle(self):
        return self.getBit(int(self.data[8], 16), 0)
    def gameCycle(self):
        return self.getBit(int(self.data[8], 16), 1)
    def powerUp(self):
        return self.getBit(int(self.data[8], 16), 2)
    def reset(self):
        return self.getBit(int(self.data[8], 16), 3)
    def ccceTxComplete(self):
        return self.getBit(int(self.data[8], 16), 4)
    def largeWin(self):
        return self.getBit(int(self.data[9], 16), 0)
    def collectCash(self):
        return self.getBit(int(self.data[9], 16), 1)
    def cancelCredit(self):
        return self.getBit(int(self.data[9], 16), 2)
    def progressiveWin(self):
        return self.getBit(int(self.data[9], 16), 3)
    def manufacturerWin0(self):
        return self.getBit(int(self.data[9], 16), 4)
    def manufacturerWin1(self):
        return self.getBit(int(self.data[9], 16), 5)
    def manufacturerWin2(self):
        return self.getBit(int(self.data[9], 16), 6)
    def doorOpen(self):
        return self.getBit(int(self.data[10], 16), 0)
    def logicCageOpen(self):
        return self.getBit(int(self.data[10], 16), 1)
    def displayError(self):
        return self.getBit(int(self.data[10], 16), 2)
    def selfAuditError(self):
        return self.getBit(int(self.data[10], 16), 3)
    def memoryError(self):
        return self.getBit(int(self.data[10], 16), 4)
    def cashInputError(self):
        return self.getBit(int(self.data[10], 16), 5)
    def cashOutputError(self):
        return self.getBit(int(self.data[10], 16), 6)
    def auditMode(self):
        return self.getBit(int(self.data[11], 16), 0)
    def testMode(self):
        return self.getBit(int(self.data[11], 16), 1)
    def powerSaveMode(self):
        return self.getBit(int(self.data[11], 16), 2)
    def subsEquipPaySuspended(self):
        return self.getBit(int(self.data[11], 16), 3)
    def mechMeterDisconnected(self):
        return self.getBit(int(self.data[11], 16), 4)
    def manufacturerError0(self):
        return self.getBit(int(self.data[11], 16), 5)
    def manufacturerError1(self):
        return self.getBit(int(self.data[11], 16), 6)
    def cancelCreditError(self):
        return self.getBit(int(self.data[12], 16), 0)
    def turnover(self):
        x = int(self.getByteString(17, 21))/100.00
        return '$%.2f' % x
    def totalWins(self):
        x = int(self.getByteString(22, 26))/100.00
        return '$%.2f' % x
    def cashBox(self):
        x = int(self.getByteString(27, 31))/100.00
        return '$%.2f' % x
    def cancelledCredits(self):
        x = int(self.getByteString(32, 36))/100.00
        return '$%.2f' % x
    def gamesPlayed(self):
        return self.getByteString(37, 40)
    def moneyIn(self):
        x = int(self.getByteString(42, 46))/100.00
        return '$%.2f' % x
    def moneyOut(self):
        x = int(self.getByteString(47, 51))/100.00
        return '$%.2f' % x
    def cashIn(self):
        x = int(self.getByteString(52, 56))/100.00
        return '$%.2f' % x
    def cashOut(self):
        x = int(self.getByteString(57, 61))/100.00
        return '$%.2f' % x
    def credits(self):
        return self.getByteString(62, 66).lstrip('0')
    def miscAccrual(self):
        return '????'
    def nrpowerUps(self):
        return self.getByteString(72, 75).lstrip('0')
    def gamesSinceReboot(self):
        return self.getByteString(76, 79).lstrip('0')
    def gamesSinceDoorOpen(self):
        return self.getByteString(80, 83).lstrip('0')
    def port1Status(self):
        return self.getBit(int(self.data[83], 16), 0)
    def port2Status(self):
        return self.getBit(int(self.data[83], 16), 1)
    def port3Status(self):
        return self.getBit(int(self.data[83], 16), 2)
    def port4Status(self):
        return self.getBit(int(self.data[83], 16), 3)
    def port5Status(self):
        return self.getBit(int(self.data[83], 16), 4)
    def port6Status(self):
        return self.getBit(int(self.data[83], 16), 5)
    def baseCreditValue(self):
        x = int(self.getByteString(85, 86))/100.00
        return '$%.2f' % x
    def programID1(self):
        x = [chr(int(val, 16)) for val in self.getByteVector(88, 95)]
        return ''.join(x).strip()
    def programID2(self):
        x = [chr(int(val, 16)) for val in self.getByteVector(96, 103)]
        return ''.join(x).strip()
    def programID3(self):
        x = [chr(int(val, 16)) for val in self.getByteVector(104, 111)]
        return ''.join(x).strip()
    def programID4(self):
        x = [chr(int(val, 16)) for val in self.getByteVector(112, 119)]
        return ''.join(x).strip()
    def prtp(self):
        x = int(self.getByteString(120, 121))/100.00
        return '%.2f%%' % x
    def linkedProgSupported(self):
        return self.getBit(int(self.data[121], 16), 0)

class mdbMdl(packetmdl, subject):
    def setdata(self, data):
        assert(data[1] == '22')
        assert(len(data) == 128)
        self.data = data
        self.notifysubscribers()
        
    def packetinfo(self):
        return 'MDB'
    def getBit(self, byte, n):
        if ((byte >> n) & 0x1):
            return True
        else:
            return False
    def getByteVector(self, lbound, hbound):
        return self.data[hbound-1:lbound-2:-1]
    def getByteString(self, lbound, hbound):
        return ''.join(self.getByteVector(lbound, hbound))    
    def GMID(self):
        return self.getByteString(5, 7)
    def versionNr(self):
        return self.getByteString(8, 9)
    def mdbType(self):
        string = '%s.%s' % tuple(self.getByteVector(10, 11))
        return string.lstrip('0')
    def stackerDoorOpen(self):
        return self.getBit(int(self.data[11], 16), 0)
    def stackerCommsError(self):
        return self.getBit(int(self.data[11], 16), 1)
    def stackerFailure(self):
        return self.getBit(int(self.data[11], 16), 2)
    def stackerFull(self):
        return self.getBit(int(self.data[11], 16), 3)
    def stackerRemoved(self):
        return self.getBit(int(self.data[11], 16), 4)
    def stackerOutOfService(self):
        return self.getBit(int(self.data[11], 16), 5)
    def cashBoxDropDoorOpen(self):
        return self.getBit(int(self.data[13], 16), 0)
    def printerPaperLow(self):
        return self.getBit(int(self.data[13], 16), 1)
    def validTicketOut(self):
        return self.getBit(int(self.data[13], 16), 2)
    def printerFault(self):
        return self.getBit(int(self.data[13], 16), 3)
    def paperEmpty(self):
        return self.getBit(int(self.data[13], 16), 4)
    def validTicketIn(self):
        return self.getBit(int(self.data[13], 16), 5)
    def ticketInCommsError(self):
        return self.getBit(int(self.data[14], 16), 0)
    def ticketInRejectedByHost(self):
        return self.getBit(int(self.data[14], 16), 1)
    def tenRejects(self):
        return self.getBit(int(self.data[14], 16), 2)
    def miscTicketInError(self):
        return self.getBit(int(self.data[14], 16), 3)
    def ticketLowerThanBCV(self):
        return self.getBit(int(self.data[14], 16), 4)
    def ticketStackingDone(self):
        return self.getBit(int(self.data[14], 16), 5)
    def nr5DollarNotes(self):
        return '%i' % int(self.getByteString(16, 20))
    def nr10DollarNotes(self):
        return '%i' % int(self.getByteString(21, 25))
    def nr20DollarNotes(self):
        return '%i' % int(self.getByteString(26, 30))
    def nr50DollarNotes(self):
        return '%i' % int(self.getByteString(31, 35))
    def nr100DollarNotes(self):
        return '%i' % int(self.getByteString(36, 40))
    def ticketsAccepted(self):
        return '%i' % int(self.getByteString(41, 45))
    def ticketsRejected(self):
        return '%i' % int(self.getByteString(46, 50))
    def totBillsAcceptedSpare(self):
        return '%i' % int(self.getByteString(51, 55))
    def valBillsAccepted(self):
        x = int(self.getByteString(56, 60))/100.00
        return '$%.2f' % x
    def totBillsAccepted(self):
        return '%i' % int(self.getByteString(61, 66))
    def dateTicketPrinted(self):
        return self.getByteString(67, 70)
    def timeTicketPrinted(self):
        return self.getByteString(71, 73)
    def printerID(self):
        return self.getByteString(74, 83)
    def ticketAmount(self):
        return self.getByteString(84, 88)
    def sequentialNr(self):
        return self.getByteString(89, 93)
    def hopperConfigured(self):
        return self.getBit(int(self.data[93], 16), 0)
    def BNAConfigured(self):
        return self.getBit(int(self.data[93], 16), 1)
    def printerConfigured(self):
        return self.getBit(int(self.data[93], 16), 2)
    def stdProgPayDone(self):
        return self.getBit(int(self.data[95], 16), 0)
    def mystProgPayDone(self):
        return self.getBit(int(self.data[95], 16), 1)
    def ccceTxComplete(self):
        return self.getBit(int(self.data[95], 16), 2)
    def mystProgWin(self):
        return self.getBit(int(self.data[95], 16), 3)
    def stdProgWinNotification(self):
        return self.getBit(int(self.data[97], 16), 0)
    def mystProgWinNotification(self):
        return self.getBit(int(self.data[97], 16), 1)
    def ccceIncDec(self):
        return self.getBit(int(self.data[97], 16), 2)
    def stdProgPayment(self):
        return self.getBit(int(self.data[97], 16), 3)
    def mystProgPayment(self):
        return self.getBit(int(self.data[97], 16), 4)
    def stdProgPoolVal(self):
        return self.getBit(int(self.data[97], 16), 5)
    def mystProgPoolVal(self):
        return self.getBit(int(self.data[97], 16), 6)
    def ticketInPort1Set(self):
        return self.getBit(int(self.data[98], 16), 0)
    def timeBroadcastSet(self):
        return self.getBit(int(self.data[98], 16), 1)
    def amtStdProgWin(self):
        x = int(self.getByteString(100, 104))/100.00
        return '$%.2f' % x
    def amtMystProgWin(self):
        x = int(self.getByteString(105, 109))/100.00
        return '$%.2f' % x
    def amtCCCETxIn(self):
        x = int(self.getByteString(110, 114))/100.00
        return '$%.2f' % x
    def amtTicketOut(self):
        x = int(self.getByteString(115, 119))/100.00
        return '$%.2f' % x
    def amtTicketIn(self):
        x = int(self.getByteString(120, 124))/100.00
        return '$%.2f' % x