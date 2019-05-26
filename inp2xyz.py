#!/usr/bin/env python3
"""
Convert an ORCA input file/files (.inp) into a standard .xyz file
"""
import argparse


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", action='store', help='.inp file', nargs='+')

    return parser.parse_args()


def get_xyz_lines(inp_filename):

    xyz_lines, xyz_section = [], False
    for line in open(inp_filename, 'r').readlines():
        if '*' in line and xyz_section:
            break
        if xyz_section:
            xyz_lines.append(line)
        if '*' in line:
            xyz_section = True

    return xyz_lines


def print_xyz_file(xyz_lines):

    if len(xyz_lines) > 0:
        with open(filename.replace('.inp', '.xyz'), 'w') as xyz_file:
            print(len(xyz_lines), '\n', file=xyz_file)
            [print(xyz_line, end='', file=xyz_file) for xyz_line in xyz_lines]

    return 0


if __name__ == '__main__':

    args = get_args()
    for filename in args.filename:
        if filename.endswith('.inp'):
            xyzs = get_xyz_lines(inp_filename=filename)
            print_xyz_file(xyz_lines=xyzs)
