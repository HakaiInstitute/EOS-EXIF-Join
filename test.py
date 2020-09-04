'''
Test files in multiple directories, in a structure laid out like:

    sample_files/any_foldername/any_text_file.txt
             - and -
    sample_files/any_foldername/any_csv.csv

eg sample_files/2/eov.txt and sample_files/2/exif.csv


'''
from core.OrthoRenamer import UTMOrthoRenamer
import os
import glob
sample_files_folder = 'sample_files'
ortho_renamer = UTMOrthoRenamer()

for folder_name in os.listdir(sample_files_folder):
    folder_prefix = sample_files_folder + '/' + folder_name

    print('---------------------------------------------')
    print(f"Testing files in {folder_prefix}")

    text_files_in_dir = glob.glob(f"{folder_prefix}/*.txt")
    csv_files_in_dir = glob.glob(f"{folder_prefix}/*.csv")

    eos_filename = text_files_in_dir[0] if len(text_files_in_dir) else ""
    exif_filename = csv_files_in_dir[0] if len(csv_files_in_dir) else ""

    if os.path.isfile(eos_filename) and os.path.isfile(exif_filename):
        OUTPUT_FILE = f"test_output_{folder_name}.txt"
        SEPARATOR = ""

        try:
            ortho_renamer.join_eos_exif_and_write_output(
                eos_filename, exif_filename, OUTPUT_FILE)
        except Exception as e:
            print(e)
    else:
        print(f"Can't find {eos_filename} or {exif_filename}")
