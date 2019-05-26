#!/usr/bin/env python3
"""
Convert a .out file into a .xyz
"""
import argparse


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", action='store', help='.out file to convert to a .xyz. Does not need to be finished')

    return parser.parse_args()


def get_xyzs(filename):

    out_file_lines = [line for line in open(filename, 'r', encoding="utf-8")]
    end_block, start_block = False, False
    xyz_lines = []

    for line in reversed(out_file_lines):

        if 'CARTESIAN COORDINATES (ANGSTROEM)' in line:
            start_block = True

        if end_block and not start_block:
            if len(line.split()) == 4:
                xyz_lines.append(line.split())

        if 'CARTESIAN COORDINATES (A.U.)' in line:
            end_block = True

    return xyz_lines


def xyzs_to_xyz_file(xyzs, filename):

    with open(filename, 'w') as xyz_file:
        print(len(xyzs), '\n', filename, sep='', file=xyz_file)
        [print(*line, sep='\t', file=xyz_file) for line in xyzs]


if __name__ == '__main__':

    args = get_args()
    xyz_list = get_xyzs(args.filename)
    xyzs_to_xyz_file(xyz_list, filename=args.filename.replace('.out', '.xyz'))
