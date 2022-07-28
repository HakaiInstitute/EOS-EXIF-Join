import io
import os
import sys
from contextlib import redirect_stdout

from PyQt5 import QtGui, QtWidgets, uic

from join_eos_exif.OrthoRenamer import GeographicEllipsRenamer, GeographicOrthoRenamer, \
    UTMEllipsRenamer, UTMOrthoRenamer


def resource_path(relative_path):
    """
    Define function to import external files when using PyInstaller.
    Get absolute path to resource, works for dev and for PyInstaller
    """
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath("./resources")

    return os.path.join(base_path, relative_path)


class JoinDataForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi(resource_path('gui.ui'), self)
        self.show()

        self.btn_load_eos.clicked.connect(self.get_eos_filepath)
        self.btn_load_exif.clicked.connect(self.get_exif_filepath)
        self.btn_save_as.clicked.connect(self.get_save_filepath)
        self.btn_join.clicked.connect(self.join_data)

        self.separator = "\t"

    @property
    def eos_path(self):
        return self.lne_eospath.text()

    @eos_path.setter
    def eos_path(self, value):
        self.lne_eospath.setText(value)

    @property
    def exif_path(self):
        return self.lne_exifpath.text()

    @exif_path.setter
    def exif_path(self, value):
        self.lne_exifpath.setText(value)

    @property
    def save_path(self):
        return self.lne_savepath.text()

    @save_path.setter
    def save_path(self, value):
        self.lne_savepath.setText(value)

    @property
    def coord_type(self):
        return str(self.combo_coord_type.currentText())

    @property
    def orthometric_heights(self):
        return self.radio_orthometric.isChecked()

    @staticmethod
    def write_list(list_item):
        with open('log.txt', 'w') as list_export:
            list_export.writelines("%s\n" % x for x in list_item)

    def update_log(self, text):
        self.log_view.insertPlainText(">> " + text + "\n")
        self.log_view.moveCursor(QtGui.QTextCursor.End)

    def get_eos_filepath(self):
        self.eos_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select file to open...', '', ".txt(*.txt)")

        os.chdir(os.path.dirname(os.path.abspath(self.eos_path)))
        self.update_log("EOS file loaded: %s" % self.eos_path)

    def get_exif_filepath(self):
        self.exif_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select file to open...', '', ".csv(*.csv)")

        self.update_log("EXIF file loaded: %s" % self.exif_path)

    def get_save_filepath(self):
        self.save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save As...', '', "*.txt")

    @staticmethod
    def show_message(text, title):
        msg_box = QtWidgets.QErrorMessage()
        msg_box.showMessage(title + ": <br>" + text.replace("\n", "<br>"))
        msg_box.exec_()

    @property
    def joiner(self):
        if self.coord_type == "UTM" and self.orthometric_heights:
            return UTMOrthoRenamer()
        elif self.coord_type == "UTM":
            return UTMEllipsRenamer()
        elif self.coord_type == "Geographic" and self.orthometric_heights:
            return GeographicOrthoRenamer()
        elif self.coord_type == "Geographic":
            return GeographicEllipsRenamer()
        else:
            raise RuntimeError("coord_type error")

    def join_data(self):
        print(self.eos_path, self.exif_path, self.save_path, self.separator)

        try:
            with redirect_stdout(out_stream := io.StringIO()):
                # Create the joined file
                self.joiner(self.eos_path, self.exif_path, self.save_path, self.separator)
                self.write_list([f"No match found for file \t{fn}" for fn in self.joiner.errors])

            out = out_stream.getvalue()
            self.update_log(out)
            self.update_log(f"File saved to {self.save_path}")

        except Exception as e:
            self.update_log(str(e))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = JoinDataForm()
    app.exec_()
