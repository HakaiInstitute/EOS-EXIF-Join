# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'joinData.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(700, 157)
        self.eospath = QtWidgets.QTextEdit(Form)
        self.eospath.setGeometry(QtCore.QRect(40, 40, 391, 31))
        self.eospath.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.eospath.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.eospath.setObjectName("eospath")
        self.exifpath = QtWidgets.QTextEdit(Form)
        self.exifpath.setGeometry(QtCore.QRect(40, 100, 391, 31))
        self.exifpath.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.exifpath.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.exifpath.setObjectName("exifpath")
        self.loadEOS = QtWidgets.QPushButton(Form)
        self.loadEOS.setGeometry(QtCore.QRect(440, 40, 93, 28))
        self.loadEOS.setObjectName("loadEOS")
        self.loadEXIF = QtWidgets.QPushButton(Form)
        self.loadEXIF.setGeometry(QtCore.QRect(440, 100, 93, 28))
        self.loadEXIF.setObjectName("loadEXIF")
        self.join = QtWidgets.QPushButton(Form)
        self.join.setGeometry(QtCore.QRect(570, 70, 93, 28))
        self.join.setObjectName("join")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Data Join"))
        self.loadEOS.setText(_translate("Form", "Load EOS"))
        self.loadEXIF.setText(_translate("Form", "Load EXIF"))
        self.join.setText(_translate("Form", "Join"))
