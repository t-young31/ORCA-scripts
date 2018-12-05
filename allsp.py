#!/usr/bin/env python3
"""
Make single point calculations for all .out files
"""

import os


def get_out_filepaths():
    filepath_list = []

    for dirpath, dirnames, filenames in os.walk(os.getcwd()):
        for filename in [f for f in filenames if f.endswith(".out")]:
            if not filename.startswith('.') and '_sp' not in filename:
                filepath_list.append(os.path.join(dirpath, filename))

    return filepath_list


def get_xyzs(filename):

    out_file_lines = [line for line in open(filename, 'r', encoding="utf-8")]
    end_block, start_block, orca_done = False, False, False
    xyz_lines = []

    for line in reversed(out_file_lines):

        if 'ORCA TERMINATED NORMALLY' in line:
            orca_done = True

        if 'CARTESIAN COORDINATES (ANGSTROEM)' in line:
            start_block = True

        if end_block and not start_block and orca_done:
            if len(line.split()) == 4:
                xyz_lines.append(line.split())

        if 'CARTESIAN COORDINATES (A.U.)' in line:
            end_block = True

    return xyz_lines


def get_charge_mult(filename):

    charge, mult = 0, 1

    out_file_lines = [line for line in open(filename, 'r', encoding="utf-8")]

    for line in out_file_lines:
        if 'Total Charge' in line:
            charge = line.split()[-1]
        if 'Multiplicity' in line:
            mult = line.split()[-1]
            break

    return [charge, mult]


def print_sp_inp_files(filepath_list):

    sp_folder_path = os.path.join(os.getcwd(), 'sp')

    if not os.path.exists(sp_folder_path):
        os.mkdir(sp_folder_path)

    for out_filepath in filepath_list:

        xyzs = get_xyzs(out_filepath)
        sp_filepath = os.path.join(sp_folder_path, os.path.basename(out_filepath).replace('.out', '_sp.inp'))

        with open(sp_filepath, 'w') as sp_file:
            print(' '.join(keywords), file=sp_file)
            print('%maxcore', 4000, file=sp_file)
            print('*xyz', *get_charge_mult(out_filepath), file=sp_file)
            for xyz_line in xyzs:
                print(*xyz_line, sep='\t', file=sp_file)
            print('*', file=sp_file)

    return 0


if __name__ == '__main__':

    keywords = ['!', 'DLPNO-CCSD(T)', 'RIJCOSX', 'def2-TZVPP', 'def2-TZVPP/C', 'def2/J', 'TIGHTSCF', 'TightPNO', 'PAL4']

    filepaths = get_out_filepaths()
    print_sp_inp_files(filepaths)
