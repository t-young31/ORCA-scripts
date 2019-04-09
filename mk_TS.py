#!/usr/bin/env python3
import os
import numpy as np
import argparse


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", action='store', help='ORCA scan output filename (.out)')
    parser.add_argument('-t', type=str, default=None, help='ORCA .input file to extract theory from')

    return parser.parse_args()


def get_inp_keywords(filename):

    keywords = []

    with open(filename, 'r') as inp_file:
        for line in inp_file:
            if line.startswith('!'):
                keywords = line.split()[1:]   # Split line apart from initial !
                break

    if 'OptTS' not in keywords:
        keywords.append('OptTS')
    if 'LooseOpt' in keywords:
        keywords.remove('LooseOpt')
    if 'Freq' not in keywords:
        keywords.append('Freq')

    return keywords


class Constants(object):
    ha_to_kcal_mol = 627.5


class ScanFile(object):

    def get_energies_and_rs(self):

        energies = []
        rs = []

        with open(self.filename, 'r') as scan_file:
            energies_block = False
            for line in scan_file:
                if len(line.split()) == 0:
                    energies_block = False
                if energies_block:
                    energies.append(float(line.split()[-1]))
                    rs.append(float(line.split()[-2]))
                if "The Calculated Surface using the 'Actual Energy'" in line:
                    energies_block = True

        relative_energies = Constants.ha_to_kcal_mol * (np.array(energies) - min(energies))
        return relative_energies, rs

    def get_r_at_max_energy(self):

        max_energy = 0.0
        r_at_max_energy = 0.0

        for i in range(self.n_points):

            if self.energies[i] > max_energy:
                max_energy = self.energies[i]
                r_at_max_energy = self.r_vals[i]

        return r_at_max_energy

    def asci_plot(self):
        n_energies = len(self.energies)

        rows, columns = 15, 60

        norm_energies = (np.array(self.energies) / max(self.energies)) * rows
        norm_r_vals = np.linspace(0, columns, n_energies)

        heights = []

        for i in range(len(norm_energies)):
            heights.append(int(norm_energies[i]) + 1)

        arr = np.chararray([rows, columns], unicode=True)
        arr[:] = ''

        for i in range(rows):
            for j in range(columns):
                for k in range(n_energies):
                    if int(norm_energies[k]) == i and int(norm_r_vals[k]) == j:
                        arr[i][j] = '+'
        print('-' * columns)
        for i in range(len(arr)):
            j = len(arr) - i - 1
            if i == 0:
                print('|', *arr[j], np.round(max(self.energies)))
            else:
                print('|', *arr[j])
        print('-' * columns)
        print(np.round(self.r_vals[0], 2), ' ' * (columns // 2 - 8), 'r / Å',
              ' ' * (columns // 2 - 8),  np.round(self.r_vals[-1], 2))

        return 0

    def get_scaned_bond_idxs(self):

        with open(self.filename, 'r') as scan_out_file:
            geom_block = False
            for line in scan_out_file:

                if geom_block:
                    bond_idxs = line.split()[3], line.split()[4]
                    return bond_idxs

                if '%geom Scan' in line:
                    geom_block = True

    def get_charge_and_mult(self):

        with open(self.filename, 'r') as scan_out_file:
            chg_mult_line = False
            for line in scan_out_file:

                if '*xyz' in line:
                    chg_mult_line = True

                if chg_mult_line:
                    chg_mult = line.split()[3], line.split()[4]
                    return chg_mult

    def __init__(self, filename):

        self.filename = filename
        self.name = os.path.basename(filename)
        self.energies, self.r_vals = self.get_energies_and_rs()        # kcal mol-1, Å
        self.n_points = len(self.energies)
        self.r_at_max_energy = self.get_r_at_max_energy()
        self.scaned_bond_idxs = self.get_scaned_bond_idxs()
        self.charge_and_mult = self.get_charge_and_mult()


class TSGuess(object):

    def get_xys(self):

        xyzs = []

        with open(self.scan_out_file.filename, 'r') as scan_file:

            scan_point_max_energy, xyz_block, opt_done = False, False, False

            for line in scan_file:
                if str(scan_out_file.r_at_max_energy) in line:
                    scan_point_max_energy = True
                if scan_point_max_energy and 'THE OPTIMIZATION HAS CONVERGED' in line:
                    opt_done = True
                if scan_point_max_energy and opt_done and 'CARTESIAN COORDINATES' in line:
                    xyz_block = True
                if xyz_block and len(line.split()) == 4:        # format:     atom label    x    y    z
                    xyzs.append(line.split())
                if len(line.split()) == 0 and xyz_block:        # break at the end of the xyz lines
                    break

        return xyzs

    def make_inp_file(self, keywords=None):

        with open(self.inp_filename, 'w') as inp_file:

            if keywords:
                print('!', *keywords, file=inp_file)
            else:
                print('!', 'Freq', 'PBE0', 'RIJCOSX', 'D3BJ', 'def2-SVP', 'def2/J', 'PAL4', 'OptTS', file=inp_file)
            print('%maxcore 4000', file=inp_file)
            print('%geom \nCalc_Hess true \nRecalc_Hess 40 \nTrust 0.2 \nMaxIter 100', file=inp_file)
            print('modify_internal \n{ B ', *self.scan_out_file.scaned_bond_idxs, 'A } end \nend', file=inp_file)
            print('*xyz', *self.scan_out_file.charge_and_mult, file=inp_file)
            for xyz_line in self.xyzs:
                print(*xyz_line, sep='\t', file=inp_file)
            print('*', file=inp_file)

        return 0

    def __init__(self, out_file):

        self.scan_out_file = out_file
        self.xyzs = self.get_xys()
        self.inp_filename = 'ts.inp'


if __name__ == '__main__':

    args = get_args()
    scan_out_file = ScanFile(args.filename)
    scan_out_file.asci_plot()

    ts_guess = TSGuess(scan_out_file)
    if args.t:
        ts_guess.make_inp_file(get_inp_keywords(args.t))
    else:
        ts_guess.make_inp_file()
