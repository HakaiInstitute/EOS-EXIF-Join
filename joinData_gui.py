# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'joinData.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(602, 462)
        self.loadEOS = QtWidgets.QPushButton(Form)
        self.loadEOS.setGeometry(QtCore.QRect(440, 40, 121, 28))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.loadEOS.setFont(font)
        self.loadEOS.setObjectName("loadEOS")
        self.loadEXIF = QtWidgets.QPushButton(Form)
        self.loadEXIF.setGeometry(QtCore.QRect(440, 100, 121, 28))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.loadEXIF.setFont(font)
        self.loadEXIF.setObjectName("loadEXIF")
        self.join = QtWidgets.QPushButton(Form)
        self.join.setGeometry(QtCore.QRect(40, 420, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.join.setFont(font)
        self.join.setObjectName("join")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 150, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.headerOffset = QtWidgets.QLineEdit(Form)
        self.headerOffset.setGeometry(QtCore.QRect(230, 149, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.headerOffset.setFont(font)
        self.headerOffset.setObjectName("headerOffset")
        self.eospath = QtWidgets.QLineEdit(Form)
        self.eospath.setGeometry(QtCore.QRect(40, 39, 391, 31))
        self.eospath.setObjectName("eospath")
        self.exifpath = QtWidgets.QLineEdit(Form)
        self.exifpath.setGeometry(QtCore.QRect(40, 100, 391, 31))
        self.exifpath.setObjectName("exifpath")
        self.logView = QtWidgets.QTextBrowser(Form)
        self.logView.setGeometry(QtCore.QRect(40, 251, 521, 151))
        self.logView.setObjectName("logView")
        self.coordType = QtWidgets.QComboBox(Form)
        self.coordType.setGeometry(QtCore.QRect(40, 201, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.coordType.setFont(font)
        self.coordType.setObjectName("coordType")
        self.coordType.addItem("")
        self.coordType.addItem("")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Data Join"))
        self.loadEOS.setText(_translate("Form", "Load EOS"))
        self.loadEXIF.setText(_translate("Form", "Load EXIF"))
        self.join.setText(_translate("Form", "Join"))
        self.label.setText(_translate("Form", "Header Offset"))
        self.headerOffset.setText(_translate("Form", "39"))
        self.coordType.setItemText(0, _translate("Form", "Geographic"))
        self.coordType.setItemText(1, _translate("Form", "UTM"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

