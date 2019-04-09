#!/usr/bin/env python3
"""
Plot the energy as a function of optimisation step
"""
import os
import numpy as np
import argparse


class Constants(object):
    ha_to_kcal_mol = 627.5


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", action='store', help='ORCA output filename (.out)')

    return parser.parse_args()


def get_rel_energies(out_filename):

    energies = []

    if out_filename.endswith('.out'):
        with open(out_filename, 'r', encoding="utf-8") as out_file:
            for line in out_file:
                if 'FINAL SINGLE POINT ENERGY' in line:
                    energies.append(float(line.split()[4]))

        return Constants.ha_to_kcal_mol * (np.array(energies) - energies[0])


def plot_energies(energies):

    sorted_ids = np.argsort(energies)[::-1]                                               # high to low
    printed_zero = False

    print('--------------------------------------------------------------', np.round(energies[sorted_ids[0]], 1))

    for i in sorted_ids:
        if energies[i] <= 0.0 and not printed_zero:
            print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 0.0')
            printed_zero = True
        elif energies[i] <= 0.0:
            print(2*i*' ', '+')
        else:
            print(2*i*' ', '+')

    print('--------------------------------------------------------------', np.round(energies[sorted_ids[-1]], 1))

    return 0


if __name__ == '__main__':

    filename = get_args().filename
    rel_energies = get_rel_energies(out_filename=filename)
    plot_energies(rel_energies[::(1 if len(rel_energies) < 30 else 2 if len(rel_energies) < 60 else 3)])
