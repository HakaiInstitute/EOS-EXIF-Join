import io
import os
import sys
from contextlib import redirect_stdout

from PyQt5 import QtGui, QtWidgets, uic

from core.OrthoRenamer import GeographicOrthoRenamer, UTMOrthoRenamer


def resource_path(relative_path):
    """
    Define function to import external files when using PyInstaller.
    Get absolute path to resource, works for dev and for PyInstaller
    """
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class JoinDataForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi(resource_path('gui.ui'), self)
        self.show()

        self.btn_load_eos.clicked.connect(self.get_eos_filepath)
        self.btn_load_exif.clicked.connect(self.get_exif_filepath)
        self.btn_join.clicked.connect(self.join_data)

        self.eos_path = None
        self.exif_path = None

        self.separator = "\t"

    @property
    def coord_type(self):
        return str(self.combo_coord_type.currentText())

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

        self.lne_eospath.setText(self.eos_path)

        os.chdir(os.path.dirname(os.path.abspath(self.eos_path)))
        self.update_log("EOS file loaded: %s" % self.eos_path)

    def get_exif_filepath(self):
        self.exif_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select file to open...', '', ".csv(*.csv)")

        self.lne_exifpath.setText(self.exif_path)
        self.update_log("EXIF file loaded: %s" % self.exif_path)

    @staticmethod
    def show_message(text, title):
        msg_box = QtWidgets.QErrorMessage()
        msg_box.showMessage(title + ": <br>" + text.replace("\n", "<br>"))
        msg_box.exec_()

    def join_data(self):
        out_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save As...', '', "*.txt")
        self.update_log(f"File saved to {out_path}")

        try:
            with redirect_stdout(out_stream := io.StringIO()):
                if self.coord_type == "Geographic":
                    ortho_renamer = GeographicOrthoRenamer()
                else:
                    ortho_renamer = UTMOrthoRenamer()

                # Create the joined file
                ortho_renamer(self.eos_path, self.exif_path, out_path, self.separator)
                self.write_list([f"No match found for file \t{fn}" for fn in ortho_renamer.errors])

            out = out_stream.getvalue()
            self.update_log(out)

        except Exception as e:
            self.update_log(str(e))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = JoinDataForm()
    app.exec_()
