import readline, glob, os

def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)



dir = input("Folder from which to extract themochemistry  ")

if dir.endswith('/'):
    pass
else:
    dir = dir + '/'


with open(dir + 'thermochem.csv', 'w') as extract_file:
    extract_file.write('Species,' + 'E,' + 'G,' + 'H' + '\n')


for out_file in glob.glob(dir + "*.out"):

    extract_file = open(dir + 'thermochem.csv', 'a')
    extract_file.write(os.path.basename(out_file).replace('.out', '') + ',')

    '''
    -----------------------------Pass the output file--------------------------
    '''

    vib_freq_section = False
    opt_done = False
    imag_freq = None
    OptTS = False
    Opt = False
    Freq = False
    E = 0
    H = 0
    G = 0


    with open(out_file, 'r') as out_file_r:

        for line in out_file_r:
            #Grab the keywords from the output file
            if '1> !' in line:
                for item in line.split():
                    if item == 'Opt':
                        Opt = True
                    if item == 'OptTS':
                        OptTS = True
                    if item == 'Freq':
                        Freq = True

            if Freq == True:
                #If a frequnecy calculation has been requested then output themochemistry

                if '*** OPTIMIZATION RUN DONE ***' in line:
                    opt_done = True

                if opt_done == True:
                    if line.startswith("VIBRATIONAL FREQUENCIES"):
                        vib_freq_section = True

                if vib_freq_section == True:
                        if '***imaginary mode***' in line and Opt == True:
                            print('imaginary freq in', out_file, 'species is not a true minimum')

                        if '***imaginary mode***' in line and OptTS == True:
                            imag_freq = line.split()[1]
                            print(os.path.basename(out_file).replace('.out', ''), ' imaginary frequnecy is  ', imag_freq)


                if opt_done == True and 'Electronic energy' in line:
                    E = float(line.split()[-2])
                if opt_done == True and 'Total Enthalpy' in line:
                    H = float(line.split()[-2]) - E
                if opt_done == True and 'Final Gibbs free enthalpy' in line:
                    G = float(line.split()[-2]) - E


    extract_file.write(str(E) + ',' + str(G) + ',' + str(H) + '\n')