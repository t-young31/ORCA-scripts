from __future__ import print_function
import sys
import os

keywords = ['!', 'DLPNO-CCSD(T)', 'RIJCOSX', 'def2-TZVPP', 'def2-TZVPP/C', 'def2/J', 'TIGHTSCF', 'TightPNO', 'PAL4']

for f in sys.argv[1:]:
    xyzs = []

    with open(f, 'r') as in_file:

        #read the first line (natoms) and second (title) line
        in_file.readline()
        in_file.readline()

        for line in in_file:
            xyzs.append(line)

    if os.path.isdir('SP/'):

        sp_file = os.path.join('SP/', f.replace('.xyz', '.inp'))

        with open(sp_file, 'w') as out_file:
            print(' '.join(keywords), file=out_file)
            print('%maxcore 4000 \n', sep='', file=out_file)
            for xyz_line in xyzs:
                print(xyz_line, end='', file=out_file)

    else:
        exit()
