# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'packetview.ui'
#
# Created: Wed Jun 13 20:51:46 2012
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
        packetViewer.resize(741, 700)
        packetViewer.setWindowTitle(_fromUtf8("Packet View"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(packetViewer)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.textEdit = QtGui.QTextEdit(packetViewer)
        self.textEdit.setAcceptDrops(False)
        self.textEdit.setFrameShape(QtGui.QFrame.StyledPanel)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout_4.addWidget(self.textEdit)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(98, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.btnClose = QtGui.QPushButton(packetViewer)
        self.btnClose.setText(QtGui.QApplication.translate("packetViewer", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout_2.addWidget(self.btnClose, 2, 2, 1, 1)
        self.btnCopy = QtGui.QPushButton(packetViewer)
        self.btnCopy.setText(QtGui.QApplication.translate("packetViewer", "Copy to clipboard", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCopy.setObjectName(_fromUtf8("btnCopy"))
        self.gridLayout_2.addWidget(self.btnCopy, 2, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.retranslateUi(packetViewer)
        QtCore.QObject.connect(self.btnClose, QtCore.SIGNAL(_fromUtf8("clicked()")), packetViewer.close)
        QtCore.QMetaObject.connectSlotsByName(packetViewer)

    def retranslateUi(self, packetViewer):
        pass

