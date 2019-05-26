#!/usr/bin/env python3
"""
Extract all the final energies in the .out files in the current directory into a final_E.csv file
"""
import os
import subprocess


if __name__ == '__main__':

    open('final_E.csv', 'w').close()
    csv_file = open('final_E.csv', 'a')

    print('Filename', 'Energy / Ha', sep=',', file=csv_file)

    for filename in os.listdir(os.getcwd()):
        if filename.endswith('.out') and not filename.endswith('.smd.out'):
            e, orca_failed, line_n = 0.0, True, 0

            # Use tail for fast access to the last electronic energy in the ORCA output file
            tail = subprocess.Popen(['tail', '-n 200', filename], stdout=subprocess.PIPE)
            while True:
                line = tail.stdout.readline()
                line_n += 1
                if len(line.rsplit()) == 0 and line_n > 200:
                    break
                if 'FINAL SINGLE POINT ENERGY' in str(line):
                    e = float(line.rsplit()[4])
                if 'Electronic energy' in str(line):
                    e = float(line.rsplit()[3])
                if '****ORCA TERMINATED NORMALLY****' in str(line):
                    orca_failed = False

            if orca_failed:
                print('ORCA failed for', filename)
            else:
                print(filename, e, sep=',', file=csv_file)
