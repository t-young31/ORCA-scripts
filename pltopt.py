#!/usr/bin/env python3
"""
Plot the energy as a function of optimisation step
"""
import os
import numpy as np
import argparse

ha_to_kcal_mol = 627.5


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", action='store', help='ORCA output filename (.out)')

    return parser.parse_args()


def get_rel_energies_and_last_de(out_filename):

    energies, last_de = [], 0.0

    if out_filename.endswith('.out'):
        with open(out_filename, 'r', encoding="utf-8") as out_file:
            for line in out_file:
                if 'FINAL SINGLE POINT ENERGY' in line:
                    energies.append(float(line.split()[4]))
                if 'Energy change' in line and len(line.split()) == 5:
                    last_de = float(line.split()[2])

        if len(energies) == 0:
            exit("Couldn't find any energy evaluations")

        return ha_to_kcal_mol * (np.array(energies) - energies[0]), ha_to_kcal_mol * last_de


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
    rel_energies, last_delta_energy = get_rel_energies_and_last_de(out_filename=filename)
    plot_energies(rel_energies[::(1 if len(rel_energies) < 30 else 2 if len(rel_energies) < 60 else 3)])
    print('Final ∆E =', np.round(last_delta_energy, 4), 'kcal / mol-1')
