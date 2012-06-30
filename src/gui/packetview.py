# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'packetview.ui'
#
# Created: Sun Jul  1 02:25:39 2012
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
        self.verticalLayout = QtGui.QVBoxLayout(packetViewer)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit = QtGui.QLineEdit(packetViewer)
        self.lineEdit.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.btnLineCopy = QtGui.QPushButton(packetViewer)
        self.btnLineCopy.setText(QtGui.QApplication.translate("packetViewer", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLineCopy.setObjectName(_fromUtf8("btnLineCopy"))
        self.horizontalLayout.addWidget(self.btnLineCopy)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEdit = QtGui.QTextEdit(packetViewer)
        self.textEdit.setEnabled(True)
        self.textEdit.setAcceptDrops(False)
        self.textEdit.setFrameShape(QtGui.QFrame.StyledPanel)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(98, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnCopy = QtGui.QPushButton(packetViewer)
        self.btnCopy.setText(QtGui.QApplication.translate("packetViewer", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCopy.setObjectName(_fromUtf8("btnCopy"))
        self.horizontalLayout_2.addWidget(self.btnCopy)
        self.btnClose = QtGui.QPushButton(packetViewer)
        self.btnClose.setText(QtGui.QApplication.translate("packetViewer", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout_2.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(packetViewer)
        QtCore.QObject.connect(self.btnClose, QtCore.SIGNAL(_fromUtf8("clicked()")), packetViewer.close)
        QtCore.QMetaObject.connectSlotsByName(packetViewer)

    def retranslateUi(self, packetViewer):
        pass

