import pandas as pd

# NOTE: this should match csv label data
NAME = "name"
SZ = "sz"
DARK = "dark"
APPR = "appr"
TL = "tl"
REFERENCE = "ref"

FOUND = "dis"

def read_spin_parity_galaxies_label_from_csv(csv_path):
    the_csv = pd.read_csv(csv_path)

    galaxy_name_to_dark_side_dict = dict()

    for i in range(len(the_csv[NAME])):
        name = the_csv[NAME][i]
        dark = the_csv[DARK][i]

        galaxy_name_to_dark_side_dict[name] = dark

    return galaxy_name_to_dark_side_dict