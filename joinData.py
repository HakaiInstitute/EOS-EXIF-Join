import joinData_gui
from PyQt4 import QtCore, QtGui
import sys

class joinData_Form(QtGui.QWidget, joinData_gui.Ui_Form):

    def __init__(self, parent=None):

        super(joinData_Form, self).__init__(parent)

        self.setupUi(self)

        self.loadEOS.clicked.connect(self.get_eos_filepath)
        self.loadEXIF.clicked.connect(self.get_exif_filepath)
        self.join.clicked.connect(self.joinData)

        self.EOS_FILE = None
        self.EXIF_FILE = None

        self.EOS_FIRST_LINE = 39
        self.MAX_DECIMALS = 3
        self.separator = "\t"

    def get_eos_filepath(self):

        f = QtGui.QFileDialog.getOpenFileName(self, 'Select file to open...',
                                              '', ".txt(*.txt)")
        
        self.EOS_FILE = str(f)

        self.eospath.setText(self.EOS_FILE)

        print(self.EOS_FILE)

    def get_exif_filepath(self):

        f = QtGui.QFileDialog.getOpenFileName(self, 'Select file to open...',
                                              '', ".csv(*.csv)")

        self.EXIF_FILE = str(f)

        self.exifpath.setText(self.EXIF_FILE)

        print(self.EXIF_FILE)

    def truncate_float_str(self, str, decimals):
        
        sides = str.split('.')
        
        return sides[0] + '.' + sides[1][0:decimals]

    #Reads EOS file
    #returns list if list
    #skips n lines from the start
    #EOS file uses tab separators
    def read_eos_file(self, filename, skip_n_lines):

        with open(filename) as f:
            
            return list(map(lambda x: x.split(), f.readlines()[skip_n_lines:]))

    #Read EXIF file
    #returns list if lists
    #skip one header line in EXIF
    #EXIF file uses comma separator
    def read_exif_file(self, filename):

        with open(filename) as g:
            
            return list(map(lambda x: x.split(','), g.readlines()[1:]))

    #Returns list of lines  
    def join_eos_exif(self, eos, exif):

        final_csv_header = ['CIR_Filena', 'Easting',
                        'Northing', 'Ellips', 'Omega', 'Phi', 'Kappa']
        final_csv_lines = [final_csv_header]

        num_matched = 0
        num_not_matched = 0

        joined = []

    # Go through each line in exif, find match eos time
        for exif_line in exif:
            
            match = ''
            
            eof_time = exif_line[3].split(':')[1]

            exif_filename = exif_line[0]
            
        # find matching time in EoS
            for eos_line in eos:
                
                eos_time = eos_line[1]
                
            # truncate either time to 3 decimal places and match
                if self.truncate_float_str(eos_time, self.MAX_DECIMALS) == self.truncate_float_str(eof_time, self.MAX_DECIMALS):
                    
                    new_filename = exif_filename[:-4] + '_rgbi.tif'
                    
                    joined = [new_filename, eos_line[2], eos_line[3],
                              eos_line[4], eos_line[5], eos_line[6], eos_line[7]]
                    
                    match = joined
                    
                    pass
                
            if match:
                
                final_csv_lines.append(joined)
                
                num_matched += 1
                
            else:
                
                print('No match found for file ' + exif_filename)
                
                num_not_matched += 1

        print("Matched records: " + str(num_matched))
        print("Unmatched records: " + str(num_not_matched))
        return final_csv_lines


    def list_2d_to_string(self, list_2d, separator):
        
        return "\n".join([separator.join(list) for list in list_2d])

    def joinData(self):

        eos = self.read_eos_file(self.EOS_FILE, self.EOS_FIRST_LINE)
        exif = self.read_exif_file(self.EXIF_FILE)
        joined = self.join_eos_exif(eos, exif)
        final_csv_lines = self.list_2d_to_string(joined, self.separator)

        outFile = QtGui.QFileDialog.getSaveFileName(self, 'Save As...', '', "*.txt")

        with open(outFile, 'w') as f:

            f.write(final_csv_lines)
            
            print("Data written to %s" % outFile)
            
app = QtGui.QApplication(sys.argv)

form = joinData_Form()

form.show()

app.exec_()
