# Ortho Rename Tool

# TODO this won't work if there are any values in the 'ID' field.


class OrthoRenamer(object):
    
    def __init__(self):
        
        self.errors = []
        
        self.coordType = "Geographic"

    def truncate_float_str(self, str, decimals):
        sides = str.split('.')
        # Not sure if this case can occur
        if len(sides) != 2:
            raise ValueError("Can't parse float from: " + str)
        return sides[0] + '.' + sides[1][0:decimals]

    def read_eos_file(self, filename, headerOffset = 39):
        '''
        Reads the EoS file
        returns list if lists
        EoS file uses tab separators
        '''
        EOS_FIRST_LINE = headerOffset

        with open(filename) as f:
            return list(filter(lambda y: len(y),
                               map(lambda x: x.split(),
                                   f.readlines()[EOS_FIRST_LINE:])))

    def read_exif_file(self, filename):
        '''
        Read the Exif file
        returns list if lists
        skip one header line in EXIF
        EXIF file uses comma separator
        '''
        with open(filename) as g:
            return list(map(lambda x: x.split(','), g.readlines()[1:]))

    def join_eos_exif_lists(self, eos, exif):
        '''
        returns  list of lists
        '''
        
        # truncate times to 3 decimals to match them, eg 123.4567 -> 123.456
        MAX_DECIMALS = 3
        
        if self.coordType == "Geographic":
            
            final_csv_header = ['CIR_Filena', 'Lon', 'Lat', 'Ellips', 'Omega', 'Phi', 'Kappa']
            
        else:
            
            final_csv_header = ['CIR_Filena', 'Easting', 'Northing', 'Ellips', 'Omega', 'Phi', 'Kappa']
            
        final_csv_lines = [final_csv_header]

        num_matched = 0
        num_not_matched = 0

        joined = []

        # Go through each line in exif, find match eos time
        for exif_line in exif:
            if len(exif_line) < 4:
                print(exif_line)
                continue
            match = ''
            exif_time = exif_line[3].split(':')[1]

            exif_filename = exif_line[0]
            # find matching time in EoS
            for eos_line in eos:
                if len(eos_line) < 4:
                    print(eos_line)
                    continue

                eos_time = eos_line[1]

                # Skip line if can't parse floats
                # This could be the XXXXXX.XXXXXX time situation or
                # multiple CSV headers situation
                try:
                    float(exif_time)
                    float(eos_time)
                except Exception as e:
                    continue

                # truncate either time to 3 decimal places and match
                if (self.truncate_float_str(eos_time, MAX_DECIMALS) ==
                        self.truncate_float_str(exif_time, MAX_DECIMALS)):
                    new_filename = exif_filename[:-4] + '_rgbi.tif'
                    
                    if self.coordType == "Geographic":
                        
                        joined = [new_filename, eos_line[9], eos_line[8],
                                  eos_line[4], eos_line[5], eos_line[6], 
                                  eos_line[7]]
                        
                    else:
                        
                        joined = [new_filename, eos_line[2], eos_line[3],
                                  eos_line[4], eos_line[5], eos_line[6], 
                                  eos_line[7]]
                        
                    match = joined
                    pass
            if match:
                final_csv_lines.append(joined)
                num_matched += 1
            else:
                print('No match found for file ' + exif_filename)
                self.errors.append("No match found for file \t %s" % exif_filename)
                num_not_matched += 1

        print("Matched records: " + str(num_matched))
        print("Unmatched records: " + str(num_not_matched))
        return final_csv_lines

    def list_2d_to_string(self, list_2d, separator):
        return "\n".join([separator.join(list) for list in list_2d])

    def join_eos_exif_and_write_output(self, eos_filename, exif_filename,
                                       output_filename, separator="\t", headerOffset = 39):
        # skip some header lines in eos file
        eos = self.read_eos_file(eos_filename, headerOffset)
        exif = self.read_exif_file(exif_filename)
        joined = self.join_eos_exif_lists(eos, exif)
        final_csv_lines = self.list_2d_to_string(joined, separator)

        with open(output_filename, 'w') as f:
            f.write(final_csv_lines)
            print("Wrote " + output_filename)
            f.close()


if __name__ == "__main__":
    eos_file = 'EoS.txt'
    exif_file = 'ExifLog.csv'
    output_file = 'eos_exif_joined.csv'

    output_separator = "\t"

    ortho_renamer = OrthoRenamer()
    ortho_renamer.join_eos_exif_and_write_output(
        eos_file, exif_file, output_file, output_separator)
    pass
