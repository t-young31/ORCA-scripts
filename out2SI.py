#!/usr/bin/env python3
import argparse
from codecs import open


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", action='store', nargs='+',
                        help='.out file(a) to extract E, ZPE, H, TS, G corr, G and append it to SI.csv')

    return parser.parse_args()


def get_e_h_s_g(out_filename):

    e, zpe, h, ts, g_corr, g = 0, 0, 0, 0, 0, 0
    thermo_done = False

    if filename.endswith('.out'):
        for line in open(out_filename, 'r',encoding="utf-8", errors="ignore"):
            if 'THERMOCHEMISTRY' in line:
                thermo_done = True

            if 'FINAL SINGLE POINT ENERGY' in line:
                e = float(line.split()[4])
            if 'Zero point energy' in line:
                zpe = float(line.split()[4])
            if 'Total Enthalpy' in line:
                h = float(line.split()[3])
            if 'Final entropy term' in line:
                ts = float(line.split()[4])
            if 'G-E(el)' in line:
                g_corr = float(line.split()[2])
            if 'Final Gibbs free enthalpy' in line:
                g = float(line.split()[5])

    if not thermo_done:
        print('Theremochemistry is not done in \t', filename)
    if not all([e, zpe, h, ts, g_corr, g]) != 0:
        print('Error in extracting thermochemical data from \t', filename)

    return [e, zpe, h, ts, g_corr, g]


if __name__ == '__main__':

    args = get_args()
    with open('Si.csv', 'a') as csv_file:
        print('Name, Eel, ZPE, H, Tqh-S, Total corr, qh-G', file=csv_file)
        for filename in args.filenames:
            print(filename[:-4], end=',', file=csv_file)
            print(*get_e_h_s_g(filename), sep=',', file=csv_file)
