from __future__ import print_function
import readline, glob, os


def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]


def run():
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)

    directory = str(raw_input("Folder from which to create single point calculations      "))

    sp_dir = os.path.join(directory, 'SP')

    if os.path.isdir(sp_dir) is False:
        os.system('mkdir %s/SP' % directory)

    xyz_files = os.path.join(directory, '*.xyz')

    for file in glob.glob(xyz_files):

        xyzs = []

        with open(file, 'r') as xyz_file:

            for line in xyz_file:
                if len(line.split()) == 4 and len(line.split()[0].strip()) < 3:
                    xyzs.append(line)

        filename = os.path.split(file)[1]

        sp_file = os.path.join(sp_dir, filename.replace('.xyz', '.inp'))

        with open(sp_file, 'w') as out_file:
            print(' '.join(keywords), file=out_file)
            print('%maxcore', maxcore, file=out_file)
            print('*xyz', charge, mult, file=out_file)
            for xyz_line in xyzs:
                print(xyz_line, end='', file=out_file)
            print('*', file=out_file)


keywords = ['!', 'DLPNO-CCSD(T)', 'RIJCOSX', 'def2-TZVPP', 'def2-TZVPP/C', 'def2/J', 'TIGHTSCF', 'TightPNO', 'PAL4']

charge = 0
mult = 1
maxcore = 4000

run()
