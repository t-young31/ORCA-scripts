import os
import numpy as np
import argparse


def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", action='store', help='.inp file')

    return parser.parse_args()


args = get_args()
input_path = args.filename

'''
-----------------------------Parse the input file--------------------------
'''

charge = mult = n_procs = None
xyzs = []

with open(input_path, 'r') as in_file:
    keywords = in_file.readline().split()

    for item in keywords:
        if item.startswith("PAL"):
            n_procs = item.strip()[-1]

    xyz_start = False
    while xyz_start == False:
        in_file_line = in_file.readline()

        if "*xyz" in in_file_line:
            xyz_start = True
            _xyz, charge, mult = in_file_line.split()

    xyz_end = False
    while not xyz_end:
        in_file_line = in_file.readline()

        if "*" in in_file_line:
            xyz_end = True
            break

        xyzs.append(in_file_line)

n_atoms = len(xyzs)

'''
----------------------------Fix keywords-----------------------
'''

for i in range(len(keywords)):
    if keywords[i] == 'OptTS' or keywords[i] == 'Opt':
        keywords[i] = 'LooseOpt'
    if keywords[i] == 'TightOpt':
        keywords[i] = 'LooseOpt'

if 'LooseOpt' not in keywords:
    keywords.append('LooseOpt')
if 'Freq' in keywords:
    keywords.remove('Freq')

'''
--------------------Generate and write a new geometry scan file----------

'''

# Get input for atoms to scan
raw_input = input('{:<50}'.format("Atoms to scan, seperated by a space:"))
print("NOTE:    multiple character atoms are not supported")

atom1 = 0
atom2 = 0
# If only the indicies are defined use them directly
try:
    atom1, atom2 = [int(x) for x in raw_input.split()]

# Else determine the indicies from label e.g. C1
except ValueError:
    atom1_labeled, atom2_labeled = [x for x in raw_input.split()]

    atom1_iterator = 0
    for i in range(len(xyzs)):
        line = xyzs[i]
        if atom1_labeled.strip()[0] == line.split()[0]:
            atom1_iterator +=1
            if atom1_iterator == int(atom1_labeled.strip()[1:]):
                atom1 = i

    atom2_iterator = 0
    for i in range(len(xyzs)):
        line = xyzs[i]
        if atom2_labeled.strip()[0] == line.split()[0]:
            atom2_iterator +=1
            if atom2_iterator == int(atom2_labeled.strip()[1:]):
                atom2 = i

    print('{:<50}''{:<10}'.format('Will scan indicies:',(str(atom1) + ' ' + str(atom2))))


xyz_atom1 = np.zeros(3)
xyz_atom2 = np.zeros(3)

atom1_label, xyz_atom1[0], xyz_atom1[1], xyz_atom1[2] = xyzs[atom1].split()
atom2_label, xyz_atom2[0], xyz_atom2[1], xyz_atom2[2] = xyzs[atom2].split()

distance = np.round(np.linalg.norm(xyz_atom1 - xyz_atom2),5)
print('{:<50}{:<10}'.format(atom1_label + '––' + atom2_label + " distance is",  distance))

final_distance = input('{:<50}'.format("Final distance:"))

if final_distance == "":
    if distance > 2.0:                     #2.0 Å is used as the cutoff between intially bonded and not
        if atom1_label == "H":
            final_distance = 1.1
        elif atom2_label == "H":
            final_distance = 1.1
        else:
            final_distance = 1.5
    if distance <= 2.0:
            final_distance = 2.8           #Default final distance for initally non-bonded atoms
    print('{:<50}{:<10}'.format("Defaulted to a final distance of:", final_distance))

else:
    float(final_distance)


no_steps = input('{:<50}'.format("Number of geometry scan steps:"))

if no_steps == "":
    no_steps = int(np.round(np.abs(float(final_distance) - float(distance))/0.1, 0))      #Default 0.1Å step size
    print('{:<50}''{:<10}'.format("Defaulted to ", str(no_steps) + " scan steps"))

else:
    int(no_steps)

# --------------------------Construct the output scan file--------------

with open('scan.inp', 'w') as out_file:
    print(' '.join(keywords), file=out_file)
    print('%maxcore 4000 \n', '%geom Scan', sep='', file=out_file)
    print('B', atom1, atom2, '=', end=' ', file=out_file)
    print(distance, final_distance, no_steps, sep=', ', file=out_file)
    print('end \n', 'end',sep='', file=out_file)
    print('*xyz', charge, mult, file=out_file)
    [print(line, file=out_file, end='') for line in xyzs]
    print('*', file=out_file)
