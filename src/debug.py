from datetime import datetime

def DBGLOG(message):
    log = open('DebugLog.txt', 'a')
    print message
    log.write("%s %s\n" % (str(datetime.now()), message))
    log.close()