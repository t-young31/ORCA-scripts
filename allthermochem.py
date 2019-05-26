#!/usr/bin/env python3
"""
Extract all the thermochemistry data for .out files in the current/subdirectories into a .csv named
thermochem.csv
"""

import os


def get_out_filepaths():
    filepath_list = []

    for dirpath, dirnames, filenames in os.walk(os.getcwd()):
        for filename in [f for f in filenames if f.endswith(".out")]:
            if not filename.startswith('.'):
                filepath_list.append(os.path.join(dirpath, filename))

    return filepath_list


def write_thermochem(filepaths):

    extract_file = open('thermochem.csv', 'w')
    print('Species,' + 'E,' + 'G,' + 'H' + '\n', file=extract_file)

    for out_file in filepaths:

        name = out_file.replace('.out', '')
        print(os.path.basename(name) + ',', end='', file=extract_file)

        vib_freq_section, opt_done, opt_ts, opt, freq = False, False, False, False, False
        E, H, G = 0.0, 0.0, 0.0

        with open(out_file, 'r') as out_file_r:

            for line in out_file_r:
                # Grab the keywords from the output file
                if '1> !' in line:
                    for item in line.split():
                        if item.lower() == 'opt':
                            opt = True
                        if item.lower() == 'opttS':
                            opt_ts = True
                        if item.lower() == 'freq':
                            freq = True

                if freq:

                    if '*** OPTIMIZATION RUN DONE ***' in line:
                        opt_done = True

                    if opt_done:
                        if line.startswith("VIBRATIONAL FREQUENCIES"):
                            vib_freq_section = True

                    if vib_freq_section:
                            if '***imaginary mode***' in line and opt:
                                print('imaginary freq in', os.path.basename(out_file), 'species is not a true minimum')

                            if '***imaginary mode***' in line and opt_ts:
                                imag_freq = line.split()[1]
                                print(os.path.basename(name), ' imaginary frequnecy is  ', imag_freq)

                    if opt_done == True and 'Electronic energy' in line:
                        E = float(line.split()[-2])
                    if opt_done == True and 'Total Enthalpy' in line:
                        H = float(line.split()[-2]) - E
                    if opt_done == True and 'Final Gibbs free enthalpy' in line:
                        G = float(line.split()[-2]) - E

        print(str(E) + ',' + str(G) + ',' + str(H) + '\n', file=extract_file)


if __name__ == '__main__':

    filepaths = get_out_filepaths()
    write_thermochem(filepaths)
