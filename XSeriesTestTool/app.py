import sys
from PyQt4 import QtGui
from gui.mainwindow import MyApp

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())
