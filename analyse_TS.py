#!/usr/bin/env python3
"""
Analyse a transition state calculation to check wether it was sucessful
"""
import argparse


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", action='store', help='.out file to analyse')

    return parser.parse_args()


def analyse_TS(filename):

    vib_freq_section = opt_done = False
    imag_freq = 999.0

    with open(filename) as TS_output:

        for line in TS_output:
            if '*** OPTIMIZATION RUN DONE ***' in line:
                opt_done = True

            if opt_done:
                if line.startswith("VIBRATIONAL FREQUENCIES"):
                    vib_freq_section = True

            if vib_freq_section:
                    if '***imaginary mode***' in line:
                        if imag_freq == 999.0:
                            imag_freq = line.split()[1]
                        else:
                            print('Second imaginary mode found at', line.split()[1],
                                  'TS is not true first order saddle point')

            if line.startswith('NORMAL MODES'):
                vib_freq_section = False

            if 'ERROR !!!' in line:
                print('TS search ended in an ERROR')

    if float(imag_freq) < -100:
        print('TS search was probably SUCCESSFUL and has an imaginary frequnecy of  ', imag_freq, 'cm-1')

    else:

        opt_done = False
        print('TS search was probably UNSUCCESSFUL and has an imaginry imaginary frequnecy of  ', imag_freq, 'cm-1')

        with open(filename, 'r') as TS_output:
            for line in TS_output:

                if '*** OPTIMIZATION RUN DONE ***' in line:
                    opt_done = True

                if 'Electronic energy' in line and opt_done:
                    print(line)
                if 'Total Enthalpy' in line and opt_done:
                    print(line)
                if 'Final Gibbs free enthalpy' in line and opt_done:
                    print(line)


if __name__ == '__main__':

    args = get_args()
    analyse_TS(args.filename)
