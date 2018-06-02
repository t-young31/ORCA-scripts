import os
import numpy as np
import matplotlib.pyplot as plt

#The following lines are required for tab autocomplete
import readline, glob
def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)


'''
-----------------------------Scan output file path-----------------------------
'''

raw_input = input('{:<50}'.format("Scan output file (.out):"))

if '.out' not in raw_input:             #Look for scan.out file in folder, default
    scan_out_filename = 'scan.out'
    scan_out_path = raw_input
else:
    scan_out_filename = raw_input.split('/')[-1]
    scan_out_path = '/'.join(raw_input.split('/')[0:-1])



'''
-----------------------------Pass the output file--------------------------
'''
dist_E_section = False
dist_array = []
E_array = []
charge = mult = None
scaned_atoms = [0, 0]

#If the scan output file is in the same directory as the script no slash is needed
if scan_out_path == '':
    scan_out_full_path = scan_out_filename
else:
    scan_out_full_path = scan_out_path + '/' + scan_out_filename



#Grab the values of d and the associated energy values from the output file
with open(scan_out_full_path) as scan_output:

    for line in scan_output:

        if 'Bond' in line and 'range=' in line and 'steps =' in line:
            scaned_atoms[0] = line.split()[2]
            scaned_atoms[1] = line.split()[3]
            tmp_atom1 = ''
            tmp_atom2 = ''


            for j in range(2):
                for i in range(len(scaned_atoms[j].strip())):
                    try:
                        int(scaned_atoms[j].strip()[i])
                        if j ==0:
                            tmp_atom1 = tmp_atom1 + str(scaned_atoms[j].strip()[i])
                        if j ==1:
                            tmp_atom2 = tmp_atom2 + str(scaned_atoms[j].strip()[i])
                    except:
                        pass

            scaned_atoms[0] = int(tmp_atom1)
            scaned_atoms[1] = int(tmp_atom2)



        if 'Total Charge' in line:
            charge = line.split()[-1]

        if 'Multiplicity' in line:
            mult = line.split()[-1]

        if line.startswith("The Calculated Surface using the 'Actual Energy'"):
            dist_E_section = True

        if dist_E_section == True:

            if not line.startswith("The Calculated Surface") and len(line.strip()) != 0:
                dist_array.append(float(line.split()[0]))
                E_array.append(float(line.split()[1]))

        if len(line.strip()) == 0:
            dist_E_section = False



E_np_array = np.array(E_array)                              #Easier to work with a numpy array
dist_max_E = str(dist_array[int(np.argmax(E_np_array))])    #Value of d for which the energy is maximal


#Locate peak in energy array (E_np_array), if there is one
peak = False
E_peak = -99999.0
dist_E_peak = ''
for i in range(len(E_np_array) - 2):
    if E_np_array[i+1] > E_np_array[i] and E_np_array[i+1] > E_np_array[i+2]:
        peak = True
        print('{:<50}{:<10}'.format('There is a peak in PES at r =',np.round(float(dist_array[i+1]), 3)))

        if E_np_array[i] > E_peak:
            E_peak = E_np_array[i]
            dist_E_peak = str(dist_array[i+1])                   #If there is a peak in the PES  use the highest




#If Emax is at the start or end of the PES there is no peak or TS along the coord
if dist_array[int(np.argmax(E_np_array))] == dist_array[0] and peak == False:
    print('Energy is monotomically decreasing. Using the generated TS is NOT reccomended')
if dist_array[int(np.argmax(E_np_array))] == dist_array[-1] and peak == False:
    print('Energy is monotomically increasing. Using the generated TS is NOT reccomended')



print('{:<50}{:<10}'.format('Will use peak in PES at   r =',np.round(float(dist_E_peak), 3)))

peak_section = False
geom_converged = False
opt_geom = []

#Grab the cartesian coordinates for the peak in the PES
with open(scan_out_full_path) as scan_output:

    for line in scan_output:
        if dist_E_peak in line:
            peak_section = True

        if peak_section == True:
            if '*** FINAL ENERGY EVALUATION AT THE STATIONARY POINT ***' in line:
                geom_converged = True
            if geom_converged == True:
                opt_geom.append(line)

                if len(line.strip()) == 0:      #if there is a blank line, break out of the for loop
                    break


#For ling in opt geoms, get just the xyzs in the format label, x, y, z
opt_geom_xyz = []

for line in opt_geom:
    if line != '\n':
        try:
            float(line.split()[-1])         # if the last string in the line can be converted to a float, i.e in coords
            opt_geom_xyz.append(line)
        except ValueError:
            pass


#Compute the distance matrix and atoms within 2 Å

hybrid_hess = False
hybrid_hess_input = input('{:<50}'.format('Compute hybrid hessian (yes/no)'))

if hybrid_hess_input == 'yes':
    hybrid_hess = True

if hybrid_hess:
    print(hybrid_hess)

    n_atoms = len(opt_geom_xyz)
    atoms_within_2 = []

    coord_scanned1 = np.ndarray.astype(np.array(opt_geom_xyz[scaned_atoms[0]].split()[1:]), float)
    coord_scanned2 = np.ndarray.astype(np.array(opt_geom_xyz[scaned_atoms[1]].split()[1:]), float)

    for i in range(n_atoms):
        coordi = np.ndarray.astype(np.array(opt_geom_xyz[i].split()[1:]), float)
        dist1 = np.linalg.norm(coordi - coord_scanned1)
        dist2 = np.linalg.norm(coordi - coord_scanned2)

        if dist1 < 2.0 and i not in atoms_within_2:
            atoms_within_2.append(i)
        if dist2 < 2.0 and i not in atoms_within_2:
            atoms_within_2.append(i)

    #convert to string list so can be output
    atoms_within_2_str = [str(x) for x in atoms_within_2]

'''
----------------------------------Plot scan--------------------------------------
'''

E_rel_array = []

raw_input = input('{:<50}'.format("Type 'no' to skip plotting the scan:"))

if raw_input != 'no':
    for i in range(len(E_array)):
        E_rel_array.append((E_array[i] - E_array[0]) * 627.509)

    plt.plot(dist_array, E_rel_array, 'r-o')
    plt.xlabel('Distance / Å')
    plt.ylabel('Energy / kcal/mol')
    plt.show()




'''
-----------------------------Construct the TS input flie--------------------------
'''


raw_input = input('{:<50}'.format("inp file for theory etc:"))
input_filename = raw_input.split('/')[-1]
input_path = '/'.join(raw_input.split('/')[0:-1])
input_file_full_path =  n_procs = keywords = None
RIJK = False

#Construct full path
if input_path == '':
    input_file_full_path = input_filename
else:
    input_file_full_path = input_path + '/' + input_filename

#If raw input is empty use default keywords
if raw_input == '':
    keywords = ['!', 'OptTS', 'Freq', 'PBE0', 'RIJCOSX', 'D3BJ', 'def2-SVP', 'def2/J', 'TIGHTSCF', 'PAL4']
    n_procs = 4

else:
    #Read the options from the input file
    with open(input_file_full_path, 'r') as in_file:

        for line in in_file:

            #First line, containing all keywords
            if line.startswith('!'):
                keywords = line.split()
                for item in keywords:
                    if item.startswith("PAL"):
                        n_procs = item.strip()[-1]

                # Add keywords appropriate for TS search
                opt = True
                freq = True

                for i in range(len(keywords)):
                    if keywords[i] == 'Opt':
                        keywords[i] = 'OptTS'
                        opt = False
                    elif keywords[i] == 'Freq':
                        freq = False
                    elif keywords[i] == 'OptTS':
                        opt = False

                if opt == True:
                    keywords.append('OptTS')
                if freq == True:
                    keywords.append('Freq')


                #Replace RIJK with RIJCOX, which is supported in analytical frequency calculations

                for i in range(len(keywords)):
                    if keywords[i] == 'RIJK':
                        RIJK = True
                        print('RIJK is not supported with analytical frequincies, switching to RIJCOX')
                        keywords[i] = 'RIJCOSX'

                if RIJK == True:
                    for i in range(len(keywords)):
                        if '/JK' in keywords[i]:
                            keywords[i] = keywords[i].replace('/JK','/J')


#Number of recaucluations of the hessian. Default is 10, i.e recalc every 10 steps
raw_input = input('{:<50}'.format("Number of times to recompute the Hessian:"))
if raw_input == '':
    no_hess_recalc = 10
else:
    no_hess_recalc = int(raw_input)


#Trust raidus for TS search step. Default is 0.3
raw_input = input('{:<50}'.format("Trust radius:"))
if raw_input == '':
    trust_radius = 0.3
else:
    trust_radius = float(raw_input)


if scan_out_filename == 'scan.out':
    TS_full_path = scan_out_full_path.replace('scan.out', 'TS.inp')

else:
    TS_full_path=input('Specify the path for generated TS.inp:  ')


#Generate the TS file
with open(TS_full_path, 'w') as out_file:
    print(' '.join(keywords), file=out_file)
    print('%maxcore 4000 \n',sep='', file=out_file)
    print('%geom', '\n', 'Calc_Hess true', sep='', file=out_file)
    if hybrid_hess:
        print('Hybrid_Hess [', ' '.join(atoms_within_2_str), '] end', file=out_file)
    print('Recalc_Hess', no_hess_recalc, file=out_file)
    print('Trust', str(trust_radius),  file=out_file)
    print('MaxIter 100', '\n', 'end \n', sep='', file=out_file)     #Hardcoded value for the max number of geom iterations
    #Add the redundant coordinated that has been scanned, which accelerates convergence of the TS opt
    print('%geom', '\n', 'modify_internal', sep='', file=out_file)
    print('{ B ', scaned_atoms[0],' ', scaned_atoms[1], ' A } end \n', 'end',  sep='', file=out_file)
    print('*xyz', charge, mult, file=out_file)
    for line in opt_geom_xyz:
        print(line, end='', file=out_file)

    print('*', file=out_file)



'''
-----------------------------Construct the submision script--------------------------
'''

scan_sub_script = TS_full_path.replace('.inp', '.sh')
copy_command = 'cp ~/porca.sh ' +  scan_sub_script          #copy parallel sumbission script from home directory
os.system(copy_command)

scan_sub_script_lines = []
with open(scan_sub_script, 'r') as in_file:
    for line in in_file:                                    #Read in lines of generic script
        if line.startswith('#$ -pe smp'):
            line = '#$ -pe smp ' + str(n_procs) + '\n'      #Alter the nummber of processors
        elif line.startswith('#$ -l s_rt='):
            line = '#$ -l s_rt=' + '160' + ':00:00 \n'      #Hardcoded 160h wall time for the TS job
        elif '$1' in line:
            line = line.replace('$1', 'TS')
        scan_sub_script_lines.append(line)

with open(scan_sub_script, 'w') as out_file:
    for line in scan_sub_script_lines:                      #Print the output submission script
        print(line, file=out_file, end='')


print('{:<50}{:<10}'.format('TS .inp and .sh file generation','complete'))
