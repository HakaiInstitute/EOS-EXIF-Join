from abc import ABC, abstractmethod
from collections import OrderedDict

import numpy as np
import pandas as pd


class OrthoRenamer(ABC):
    def __init__(self, verbose=True):
        super().__init__()
        self.verbose = verbose
        self.errors = []  # list of filenames that can not be matched.

    @staticmethod
    def _get_eos_header_offset(filename: str) -> int:
        offset = 0
        with open(filename) as f:
            while f.readline().strip() != "Record Format:":
                offset += 1
        return offset + 7  # Additional 7 lines of info after "Record Format:"

    def read_eos_file(self, filename: str) -> pd.DataFrame:
        """
        Reads the EoS file
        returns list if lists
        EoS file uses tab delimiters
        """
        header_offset = self._get_eos_header_offset(filename)
        with open(filename) as f:
            lines = f.readlines()

        # columns represents names for the data columns as give in the file header
        columns = lines[header_offset - 5]
        columns = [z for x in columns.split(",") if (z := x.strip())[0] != "#"]

        # data are the actual numerical data values corresponding to the column names
        data = lines[header_offset:]
        data = [d.strip().split() for d in data]

        return pd.DataFrame(data, columns=columns)

    @staticmethod
    def read_exif_file(filename: str) -> pd.DataFrame:
        """
        Read the Exif file
        returns list if lists
        skip one header line in EXIF
        EXIF file uses comma separator
        """
        return pd.read_csv(filename)

    @staticmethod
    def truncate_float(number: float, decimals: int = 3) -> float:
        return np.floor(number * 10 ** decimals) / 10 ** decimals

    def log(self, message):
        if self.verbose:
            print(message)

    def join_eos_exif_data(self, eos: pd.DataFrame, exif: pd.DataFrame) -> pd.DataFrame:
        """
        Truncates times to 3 decimals to match them, eg 123.4567 -> 123.456

        returns list of lists
        """
        # Truncate EOS Times
        eos['TIME (s)'] = pd.to_numeric(eos['TIME (s)'], errors='coerce', downcast='float').dropna()
        eos['TIME (s)'] = self.truncate_float(eos['TIME (s)'])

        # Truncate Exif Times
        exif[['Weeks', 'Seconds']] = exif['Weeks:Seconds'].str.split(":", n=1, expand=True)
        exif['Seconds'] = pd.to_numeric(exif['Seconds'], errors='coerce', downcast='float').dropna()
        exif['Seconds'] = self.truncate_float(exif['Seconds'])

        # Inner join on times
        joined = pd.merge(eos, exif, left_on='TIME (s)', right_on='Seconds')

        # Create updated filename column
        joined['CIR_Filename'] = joined['Filename'].str[:-4] + "_rgbi.tif"

        # Populate the errors list
        unmatched_exif = exif[(~exif['Filename'].isin(joined['Filename']))]
        self.errors = list(unmatched_exif['Filename'])

        # Print some info
        num_matched = len(joined)
        num_not_matched = len(exif) - num_matched

        self.log(f"Matched records: {num_matched}")
        self.log(f"Unmatched records: {num_not_matched}")

        for fn in self.errors:
            self.log(f"No match found for file \t{fn}")

        return joined

    @property
    @abstractmethod
    def csv2df_map(self) -> OrderedDict:
        """Define a mapping from the output CSV column header names
            to the corresponding joined Pandas dataframe column name."""
        raise NotImplemented

    @property
    def output_csv_column_names(self) -> list:
        return list(self.csv2df_map.keys())

    @property
    def dataframe_columns_to_output(self) -> list:
        return list(self.csv2df_map.values())

    def join_eos_exif_and_write_output(self, eos_path: str, exif_path: str, output_path: str, separator: str = ","):
        # skip some header lines in eos file
        eos = self.read_eos_file(eos_path)
        exif = self.read_exif_file(exif_path)
        joined = self.join_eos_exif_data(eos, exif)

        # Create a dataframe with just the output data and write it to file
        csv_data = joined[self.dataframe_columns_to_output]
        csv_data.columns = self.output_csv_column_names
        csv_data.to_csv(output_path, sep=separator, index=False)
        self.log("Wrote " + output_path)

    def __call__(self, *args, **kwargs):
        """Call self.join_eos_exif_and_write_output when instance is called."""
        return self.join_eos_exif_and_write_output(*args, **kwargs)


class GeographicOrthoRenamer(OrthoRenamer):
    @property
    def csv2df_map(self):
        """Defines the mapping from the output CSV column header names to appropriate Pandas dataframe column name."""
        return OrderedDict({
            'CIR_Filename': 'CIR_Filename',
            'Lon': 'LONG',
            'Lat': 'LAT',
            'Ellips': 'ELLIPSOID HEIGHT',
            'Omega': 'OMEGA',
            'Phi': 'PHI',
            'Kappa': 'KAPPA'
        })


class UTMOrthoRenamer(OrthoRenamer):
    @property
    def csv2df_map(self):
        """Defines the mapping from the output CSV column header names to appropriate Pandas dataframe column name."""
        return OrderedDict({
            'CIR_Filename': 'CIR_Filename',
            'Easting': 'EASTING',
            'Northing': 'NORTHING',
            'Altitude': 'ORTHOMETRIC HEIGHT',
            'Omega': 'OMEGA',
            'Phi': 'PHI',
            'Kappa': 'KAPPA'
        })


if __name__ == "__main__":
    eos_file = '../sample_files/4/EoS.txt'
    exif_file = '../sample_files/4/ExifLog.csv'
    output_file = '../sample_files/4/eos_exif_joined.txt'

    ortho_renamer = UTMOrthoRenamer()
    ortho_renamer.join_eos_exif_and_write_output(eos_file, exif_file, output_file)
