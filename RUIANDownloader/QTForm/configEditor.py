# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configEditor.ui'
#
# Created: Sat May 03 11:07:11 2014
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 343)
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 9, 381, 141))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.dataDirectoryEdit = QtGui.QLineEdit(self.tab)
        self.dataDirectoryEdit.setGeometry(QtCore.QRect(20, 30, 311, 20))
        self.dataDirectoryEdit.setObjectName(_fromUtf8("dataDirectoryEdit"))
        self.downloadTypeComboBox = QtGui.QComboBox(self.tab)
        self.downloadTypeComboBox.setGeometry(QtCore.QRect(90, 60, 141, 22))
        self.downloadTypeComboBox.setObjectName(_fromUtf8("downloadTypeComboBox"))
        self.downloadButton = QtGui.QPushButton(self.tab)
        self.downloadButton.setGeometry(QtCore.QRect(260, 90, 101, 23))
        self.downloadButton.setObjectName(_fromUtf8("downloadButton"))
        self.uncompressDownloadedFilesCB = QtGui.QCheckBox(self.tab)
        self.uncompressDownloadedFilesCB.setGeometry(QtCore.QRect(90, 90, 151, 17))
        self.uncompressDownloadedFilesCB.setObjectName(_fromUtf8("uncompressDownloadedFilesCB"))
        self.openButton = QtGui.QPushButton(self.tab)
        self.openButton.setGeometry(QtCore.QRect(334, 30, 31, 23))
        self.openButton.setObjectName(_fromUtf8("openButton"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.timeEdit = QtGui.QTimeEdit(self.tab_2)
        self.timeEdit.setGeometry(QtCore.QRect(80, 30, 118, 22))
        self.timeEdit.setObjectName(_fromUtf8("timeEdit"))
        self.pushButton_2 = QtGui.QPushButton(self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 60, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton = QtGui.QPushButton(self.tab_2)
        self.pushButton.setGeometry(QtCore.QRect(120, 60, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.plainTextEdit = QtGui.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 150, 381, 191))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "RÚIANDownloader - [RUIANDownloader.cfg]", None))
        self.downloadButton.setText(_translate("Dialog", " Stáhnout data ", None))
        self.uncompressDownloadedFilesCB.setText(_translate("Dialog", "Rozbalit archivy GZ", None))
        self.openButton.setText(_translate("Dialog", "...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Nastavení stahování", None))
        self.pushButton_2.setText(_translate("Dialog", " Spustit službu ", None))
        self.pushButton.setText(_translate("Dialog", "Zastavit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Automatické stahování", None))

