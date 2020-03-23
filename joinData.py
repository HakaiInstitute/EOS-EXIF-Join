import joinData_gui
from PyQt5 import QtCore, QtWidgets
import sys
from OrthoRenamer import OrthoRenamer
from contextlib import redirect_stdout
import io


class joinData_Form(QtWidgets.QWidget, joinData_gui.Ui_Form):

    def __init__(self, parent=None):

        super(joinData_Form, self).__init__(parent)

        self.setupUi(self)

        self.loadEOS.clicked.connect(self.get_eos_filepath)
        self.loadEXIF.clicked.connect(self.get_exif_filepath)
        self.join.clicked.connect(self.joinData)

        self.EOS_FILE = None
        self.EXIF_FILE = None

        self.separator = "\t"

    def get_eos_filepath(self):

        f = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select file to open...', '', ".txt(*.txt)")

        self.EOS_FILE = str(f[0])

        self.eospath.setText(self.EOS_FILE)

        print(self.EOS_FILE)

    def get_exif_filepath(self):

        f = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select file to open...', '', ".csv(*.csv)")

        self.EXIF_FILE = str(f[0])

        self.exifpath.setText(self.EXIF_FILE)

        print(self.EXIF_FILE)

    def showMessage(self, text, title):
        msg_box = QtWidgets.QErrorMessage()
        msg_box.showMessage(title + ": <br>" + text.replace("\n", "<br>"))
        msg_box.exec_()

    def joinData(self):

        outFile = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save As...', '', "*.txt")

        f = io.StringIO()
        try:
            with redirect_stdout(f):
                ortho_renamer = OrthoRenamer()
                ortho_renamer.join_eos_exif_and_write_output(
                    self.EOS_FILE, self.EXIF_FILE, outFile[0], self.separator)

            out = f.getvalue()
            self.showMessage(out, 'Join output')
        except Exception as e:
            self.showMessage(str(e), "Error")


app = QtWidgets.QApplication(sys.argv)

form = joinData_Form()

form.show()

app.exec_()
