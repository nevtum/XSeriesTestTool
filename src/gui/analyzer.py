# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'analyzer.ui'
#
# Created: Sun Jul 15 19:20:07 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(713, 379)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableView = QtGui.QTableView(self.centralwidget)
        self.tableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setGridStyle(QtCore.Qt.DashLine)
        self.tableView.setSortingEnabled(False)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 0, 2, 1, 1)
        self.btnRefresh = QtGui.QPushButton(self.centralwidget)
        self.btnRefresh.setObjectName(_fromUtf8("btnRefresh"))
        self.gridLayout.addWidget(self.btnRefresh, 0, 3, 1, 1)
        self.btnClear = QtGui.QPushButton(self.centralwidget)
        self.btnClear.setObjectName(_fromUtf8("btnClear"))
        self.gridLayout.addWidget(self.btnClear, 0, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(559, 24, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 3)
        self.btnRecordPause = QtGui.QPushButton(self.centralwidget)
        self.btnRecordPause.setObjectName(_fromUtf8("btnRecordPause"))
        self.gridLayout.addWidget(self.btnRecordPause, 1, 3, 1, 1)
        self.btnAnalyze = QtGui.QPushButton(self.centralwidget)
        self.btnAnalyze.setObjectName(_fromUtf8("btnAnalyze"))
        self.gridLayout.addWidget(self.btnAnalyze, 1, 4, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 713, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuSettings = QtGui.QMenu(self.menubar)
        self.menuSettings.setObjectName(_fromUtf8("menuSettings"))
        self.menuSerial = QtGui.QMenu(self.menubar)
        self.menuSerial.setObjectName(_fromUtf8("menuSerial"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        MainWindow.setMenuBar(self.menubar)
        self.actionSet_Maximum_Rows = QtGui.QAction(MainWindow)
        self.actionSet_Maximum_Rows.setObjectName(_fromUtf8("actionSet_Maximum_Rows"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionSerial = QtGui.QAction(MainWindow)
        self.actionSerial.setObjectName(_fromUtf8("actionSerial"))
        self.actionSet_database_file = QtGui.QAction(MainWindow)
        self.actionSet_database_file.setObjectName(_fromUtf8("actionSet_database_file"))
        self.menuSettings.addAction(self.actionSet_Maximum_Rows)
        self.menuSettings.addAction(self.actionSerial)
        self.menuSerial.addAction(self.actionSet_database_file)
        self.menuSerial.addSeparator()
        self.menuSerial.addAction(self.actionQuit)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuSerial.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.btnRefresh.setDisabled)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.lineEdit.setDisabled)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("MainWindow", "Auto Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "SQL:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRefresh.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClear.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRecordPause.setText(QtGui.QApplication.translate("MainWindow", "Record", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAnalyze.setText(QtGui.QApplication.translate("MainWindow", "Decode Message", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSettings.setTitle(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSerial.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSet_Maximum_Rows.setText(QtGui.QApplication.translate("MainWindow", "Set Maximum Rows", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSerial.setText(QtGui.QApplication.translate("MainWindow", "Serial...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSet_database_file.setText(QtGui.QApplication.translate("MainWindow", "Save database file as...", None, QtGui.QApplication.UnicodeUTF8))

