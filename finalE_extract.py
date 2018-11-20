#!/home/dirac/tmcs/ball4935/opt/anaconda3/bin/python

import glob, readline, os


def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]


readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

if __name__ == '__main__':

    directory = input("Folder from which to extract single point energies  ")

    sp_E_extract_file = os.path.join(directory, 'final_E.csv')

    names_energies = []

    for out_file in glob.glob(os.path.join(directory, '*.out')):

        basename = os.path.basename(out_file).replace('.out', '')
        final_out_file_lines = os.popen('tail -n 1000 ' + out_file).read().splitlines()

        energy = 0.0

        for line in final_out_file_lines:
            if 'FINAL SINGLE POINT ENERGY' in line:
                energy = float(line.split()[-1])  # Energy is the last item in this line

        names_energies.append([basename, energy])

    extract_file = open(sp_E_extract_file, 'w')
    print('Species,' + 'E,', '\n', file=extract_file)
    for [name, energy] in sorted(names_energies):
        print(name + ',' + str(energy), file=extract_file)
        print(name + ',' + str(energy))
    extract_file.close()
