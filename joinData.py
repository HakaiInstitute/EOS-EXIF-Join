import joinData_gui
from PyQt5 import QtCore, QtWidgets, QtGui
import sys
from OrthoRenamer import OrthoRenamer
from contextlib import redirect_stdout
import io
import os

class joinData_Form(QtWidgets.QWidget, joinData_gui.Ui_Form):

    def __init__(self, parent=None):

        super().__init__()

        self.setupUi(self)

        self.loadEOS.clicked.connect(self.get_eos_filepath)
        self.loadEXIF.clicked.connect(self.get_exif_filepath)
        self.join.clicked.connect(self.joinData)

        self.EOS_FILE = None
        self.EXIF_FILE = None
        
        self.no_matches = []

        self.separator = "\t"
        
        self.coord = str(self.coordType.currentText())
        
    def writeList(self, listItem):
        
        with open('log.txt', 'w') as listExport:
            
            listExport.writelines("%s\n" % x for x in listItem)
        
    def updateLog(self, text):
        
        self.logView.insertPlainText(">> " + text + "\n")
        
        self.logView.moveCursor(QtGui.QTextCursor.End)

    def get_eos_filepath(self):

        f = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select file to open...', '', ".txt(*.txt)")

        self.EOS_FILE = str(f[0])

        self.eospath.setText(self.EOS_FILE)
        
        os.chdir(os.path.dirname(os.path.abspath(self.EOS_FILE)))
        
        self.updateLog("EOS file loaded: %s" % self.EOS_FILE)

    def get_exif_filepath(self):

        f = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select file to open...', '', ".csv(*.csv)")
        
        self.EXIF_FILE = str(f[0])

        self.exifpath.setText(self.EXIF_FILE)
        
        self.updateLog("EXIF file loaded: %s" % self.EXIF_FILE)

    def showMessage(self, text, title):
        msg_box = QtWidgets.QErrorMessage()
        msg_box.showMessage(title + ": <br>" + text.replace("\n", "<br>"))
        msg_box.exec_()

    def joinData(self):
        
        self.coord = str(self.coordType.currentText())

        outFile = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save As...', '', "*.txt")
        
        self.updateLog("File saved to %s" % str(outFile))
        
        f = io.StringIO()
        
        try:
            with redirect_stdout(f):
                ortho_renamer = OrthoRenamer()
                
                ortho_renamer.coordType = self.coord
                
                ortho_renamer.join_eos_exif_and_write_output(
                    self.EOS_FILE, self.EXIF_FILE, outFile[0], self.separator, int(self.headerOffset.text()))
            
                self.writeList(ortho_renamer.errors)

            out = f.getvalue()
            
            #self.showMessage(out, 'Join output')
            
            self.updateLog(out)
            
        except Exception as e:
            
            #self.showMessage(str(e), "Error")
            
            self.updateLog(str(e))


app = QtWidgets.QApplication(sys.argv)

form = joinData_Form()

form.show()

app.exec_()
