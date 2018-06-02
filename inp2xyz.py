import os
import readline, glob
def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

'''
-----------------------------Input file path-----------------------------
'''

raw_input = input("Input file:   ")

input_filename = raw_input.split('/')[-1]
input_path = '/'.join(raw_input.split('/')[0:-1])

'''
-----------------------------Pass the input file--------------------------
'''

xyzs = []

with open(os.path.join(input_path, input_filename), 'r') as in_file:

    xyz_start = False
    while xyz_start == False:
        in_file_line = in_file.readline()

        if "*xyz" in in_file_line:
            xyz_start = True
            *xyz, charge, mult = in_file_line.split()

    xyz_end = False
    while xyz_end == False:
        in_file_line = in_file.readline()

        if "*" in in_file_line:
            xyz_end = True
            break

        xyzs.append(in_file_line)

n_atoms = len(xyzs)



'''
-----------------------------Write xyz file---------------------------------
'''


with open(os.path.join(input_path, input_filename.replace('.inp', '.xyz')), 'w') as out_file:
    print(n_atoms,'\n', file=out_file)
    for xyz_line in xyzs:
        print(xyz_line,end='', file=out_file)



