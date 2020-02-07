# Ortho Rename Tool

# TODO this won't work if there are any values in the 'ID' field.

EOS_FILE = 'EoS.txt'
EOS_FIRST_LINE = 39
EXIF_FILE = 'ExifLog.csv'
FINAL_CSV_FILENAME = 'eos_exif_joined.csv'
# truncate times to 3 decimals to match them, eg 123.4567 becomes 123.456
MAX_DECIMALS = 3
separator = "\t"


def truncate_float_str(str, decimals):
    sides = str.split('.')
    return sides[0] + '.' + sides[1][0:decimals]


def read_eos_file(filename, skip_n_lines):
    '''
    Reads the EoS file
    returns list if lists
    skips n lines from the start
    EoS file uses tab separators
    '''
    with open(filename) as f:
        return list(map(lambda x: x.split(), f.readlines()[skip_n_lines:]))


def read_exif_file(filename):
    '''
    Read the Exif file
    returns list if lists
    skip one header line in EXIF
    EXIF file uses comma separator
    '''
    with open(filename) as g:
        return list(map(lambda x: x.split(','), g.readlines()[1:]))


def join_eos_exif(eos, exif):
    '''
    returns  list of lists
    '''
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
            if truncate_float_str(eos_time, MAX_DECIMALS) == truncate_float_str(eof_time, MAX_DECIMALS):
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


def list_2d_to_string(list_2d, separator):
    return "\n".join([separator.join(list) for list in list_2d])


# skip some header lines in eos file
eos = read_eos_file(EOS_FILE, EOS_FIRST_LINE)
exif = read_exif_file(EXIF_FILE)
joined = join_eos_exif(eos, exif)
final_csv_lines = list_2d_to_string(joined, separator)

with open(FINAL_CSV_FILENAME, 'w') as f:
    f.write(final_csv_lines)
    print("Wrote " + FINAL_CSV_FILENAME)
    f.close()
