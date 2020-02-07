# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'joinData.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(700, 157)
        self.eospath = QtGui.QTextEdit(Form)
        self.eospath.setGeometry(QtCore.QRect(40, 40, 391, 31))
        self.eospath.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.eospath.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.eospath.setObjectName(_fromUtf8("eospath"))
        self.exifpath = QtGui.QTextEdit(Form)
        self.exifpath.setGeometry(QtCore.QRect(40, 100, 391, 31))
        self.exifpath.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.exifpath.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.exifpath.setObjectName(_fromUtf8("exifpath"))
        self.loadEOS = QtGui.QPushButton(Form)
        self.loadEOS.setGeometry(QtCore.QRect(440, 40, 93, 28))
        self.loadEOS.setObjectName(_fromUtf8("loadEOS"))
        self.loadEXIF = QtGui.QPushButton(Form)
        self.loadEXIF.setGeometry(QtCore.QRect(440, 100, 93, 28))
        self.loadEXIF.setObjectName(_fromUtf8("loadEXIF"))
        self.join = QtGui.QPushButton(Form)
        self.join.setGeometry(QtCore.QRect(570, 70, 93, 28))
        self.join.setObjectName(_fromUtf8("join"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Data Join", None))
        self.loadEOS.setText(_translate("Form", "Load EOS", None))
        self.loadEXIF.setText(_translate("Form", "Load EXIF", None))
        self.join.setText(_translate("Form", "Join", None))

