# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'packetview.ui'
#
# Created: Mon Jun 11 00:35:31 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_packetViewer(object):
    def setupUi(self, packetViewer):
        packetViewer.setObjectName(_fromUtf8("packetViewer"))
        packetViewer.setWindowModality(QtCore.Qt.NonModal)
        packetViewer.resize(800, 700)
        packetViewer.setWindowTitle(_fromUtf8("Packet View"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(packetViewer)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(98, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(packetViewer)
        self.pushButton.setText(QtGui.QApplication.translate("packetViewer", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout_2.addWidget(self.pushButton, 2, 1, 1, 1)
        self.textEdit = QtGui.QTextEdit(packetViewer)
        self.textEdit.setAcceptDrops(False)
        self.textEdit.setFrameShape(QtGui.QFrame.StyledPanel)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout_2.addWidget(self.textEdit, 0, 0, 2, 2)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.retranslateUi(packetViewer)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), packetViewer.close)
        QtCore.QMetaObject.connectSlotsByName(packetViewer)

    def retranslateUi(self, packetViewer):
        pass

