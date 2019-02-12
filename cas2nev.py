#!/usr/bin/env python3
import argparse
import os
import shutil
from codecs import open


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("basename",
                        action='store',
                        help='basename of the .xyz and .gbw file to extract. The script will use all files with a'
                             'matching basename. e.g. for test.001.xyz, test.002.xyz.. basename = test')

    return parser.parse_args()


def get_all_xyz_gbw_names(basename):

    filenames_with_gbw_xyz_extensions = []

    for filename in os.listdir(os.getcwd()):

        has_gbw_ext = False
        if basename in filename:

            if os.path.exists(filename.replace('.xyz', '.gbw')):
                has_gbw_ext = True

            if filename.endswith('.xyz') and has_gbw_ext:
                filenames_with_gbw_xyz_extensions.append(filename.replace('.xyz', ''))

    return sorted(filenames_with_gbw_xyz_extensions)


def get_xyzs(xyz_filename):
    return [line for line in open(xyz_filename, 'r',
                                  encoding="utf-8",
                                  errors="ignore") if len(line.split()) == 4 and line.split()[-1][-1].isdigit()]


def make_inp_file(filename):

    dir_name = filename

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    shutil.copy(filename + '.xyz', dir_name)
    shutil.copy(filename + '.gbw', dir_name)

    with open(os.path.join(dir_name, filename + '_nev.inp'), 'w') as inp_file:
        print('! def2-TZVPP AutoAux PAL4 Normalprint MOREAD RI-NEVPT2', file=inp_file)
        print('%moinp \"', filename + '.gbw\"', sep='', file=inp_file)
        print('%maxcore 4000\n', '%casscf\n   trafostep ri\n   nel 8\n   norb 8\n   mult 1\nend', sep='', file=inp_file)
        print('*xyz 0 1', file=inp_file)
        for line in get_xyzs(filename + '.xyz'):
            print(line, end='', file=inp_file)
        print('*', file=inp_file)

    return 0


if __name__ == '__main__':

    args = get_args()
    for filename_no_ext in get_all_xyz_gbw_names(basename=args.basename):
        make_inp_file(filename_no_ext)
