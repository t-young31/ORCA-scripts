from __future__ import print_function
import sys

for f in sys.argv[1:]:
    xyzs = []

    with open(f, 'r') as in_file:

        xyz_start = False
        while xyz_start == False:
            in_file_line = in_file.readline()

            if "*xyz" in in_file_line:
                xyz_start = True

        xyz_end = False
        while xyz_end == False:
            in_file_line = in_file.readline()

            if "*" in in_file_line:
                xyz_end = True
                break

            xyzs.append(in_file_line)

    n_atoms = len(xyzs)

    with open(f.replace('.inp', '.xyz'), 'w') as out_file:
        print(n_atoms, '\n', file=out_file)
        for xyz_line in xyzs:
            print(xyz_line, end='', file=out_file)

