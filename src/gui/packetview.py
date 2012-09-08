# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'packetview.ui'
#
# Created: Sat Sep 08 12:54:24 2012
#      by: PyQt4 UI code generator 4.9.4
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
        packetViewer.setEnabled(True)
        packetViewer.resize(603, 700)
        packetViewer.setWindowTitle(_fromUtf8("Packet View"))
        packetViewer.setModal(False)
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
        self.lineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnPrev = QtGui.QPushButton(packetViewer)
        self.btnPrev.setObjectName(_fromUtf8("btnPrev"))
        self.horizontalLayout.addWidget(self.btnPrev)
        self.btnNext = QtGui.QPushButton(packetViewer)
        self.btnNext.setObjectName(_fromUtf8("btnNext"))
        self.horizontalLayout.addWidget(self.btnNext)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEdit = QtGui.QTextEdit(packetViewer)
        self.textEdit.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setAcceptDrops(False)
        self.textEdit.setFrameShape(QtGui.QFrame.StyledPanel)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout.addWidget(self.textEdit)
        self.uiRawData = QtGui.QTextEdit(packetViewer)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiRawData.sizePolicy().hasHeightForWidth())
        self.uiRawData.setSizePolicy(sizePolicy)
        self.uiRawData.setMaximumSize(QtCore.QSize(16777215, 80))
        self.uiRawData.setReadOnly(True)
        self.uiRawData.setObjectName(_fromUtf8("uiRawData"))
        self.verticalLayout.addWidget(self.uiRawData)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.checkBox = QtGui.QCheckBox(packetViewer)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.horizontalLayout_2.addWidget(self.checkBox)
        spacerItem1 = QtGui.QSpacerItem(98, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.btnCopy = QtGui.QPushButton(packetViewer)
        self.btnCopy.setEnabled(True)
        self.btnCopy.setObjectName(_fromUtf8("btnCopy"))
        self.horizontalLayout_2.addWidget(self.btnCopy)
        self.btnClose = QtGui.QPushButton(packetViewer)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout_2.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(packetViewer)
        QtCore.QObject.connect(self.btnClose, QtCore.SIGNAL(_fromUtf8("clicked()")), packetViewer.close)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), self.uiRawData.setHidden)
        QtCore.QMetaObject.connectSlotsByName(packetViewer)
        packetViewer.setTabOrder(self.lineEdit, self.checkBox)
        packetViewer.setTabOrder(self.checkBox, self.btnPrev)
        packetViewer.setTabOrder(self.btnPrev, self.btnNext)
        packetViewer.setTabOrder(self.btnNext, self.btnCopy)
        packetViewer.setTabOrder(self.btnCopy, self.btnClose)
        packetViewer.setTabOrder(self.btnClose, self.textEdit)
        packetViewer.setTabOrder(self.textEdit, self.uiRawData)

    def retranslateUi(self, packetViewer):
        self.btnPrev.setText(QtGui.QApplication.translate("packetViewer", "Previous", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNext.setText(QtGui.QApplication.translate("packetViewer", "Next", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("packetViewer", "Hide Raw", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCopy.setText(QtGui.QApplication.translate("packetViewer", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setText(QtGui.QApplication.translate("packetViewer", "Close", None, QtGui.QApplication.UnicodeUTF8))

