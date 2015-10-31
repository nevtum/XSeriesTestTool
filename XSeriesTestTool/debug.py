from datetime import datetime

_is_logging_enabled = False
_filename = "DebugLog.txt"

def Log(message):
    _log_to_console(message)
    if _is_logging_enabled:
        _log_to_file(message, _filename)

def enable_logging():
    _is_logging_enabled = True

def disable_logging():
    _is_logging_enabled = False

def _log_to_file(message, filename):
    log = open(filename, 'a')
    log.write("%s %s\n" % (str(datetime.now()), message))
    log.close()

def _log_to_console(message):
    print(message)
