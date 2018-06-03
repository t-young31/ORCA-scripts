import readline, glob

def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

'''
-----------------------------TS out file path-----------------------------
'''

raw_input = input("TS output file (.out):   ")
input_filename = raw_input.split('/')[-1]
input_path = '/'.join(raw_input.split('/')[0:-1])


'''
-----------------------------Pass the output file--------------------------
'''
vib_freq_section = opt_done = False
imag_freq = 999.0


with open(input_path + '/' + input_filename, 'r') as TS_output:

    for line in TS_output:
        if '*** OPTIMIZATION RUN DONE ***' in line:
            opt_done = True

        if opt_done:
            if line.startswith("VIBRATIONAL FREQUENCIES"):
                vib_freq_section = True

        if vib_freq_section:
                if '***imaginary mode***' in line:
                    if imag_freq == 999.0:
                        imag_freq = line.split()[1]
                    else:
                        print('Second imaginary mode found at', line.split()[1], 'TS is not true first order saddle point')

        if line.startswith('NORMAL MODES'):
            vib_freq_section = False

        if 'ERROR !!!' in line:
            print('TS search ended in an ERROR')


if float(imag_freq) < -100:
    print('TS search was probably SUCCESSFUL and has an imaginary frequnecy of  ', imag_freq, 'cm-1')
    opt_done = False

    with open(input_path + '/' + input_filename, 'r') as TS_output:
        for line in TS_output:

            if '*** OPTIMIZATION RUN DONE ***' in line:
                opt_done = True

            if 'Electronic energy' in line and opt_done:
                print(line)
            if 'Total Enthalpy' in line and opt_done:
                print(line)
            if 'Final Gibbs free enthalpy' in line and opt_done:
                print(line)

else:
    print('TS search was probably UNSUCCESSFUL and has an imaginry imaginary frequnecy of  ', imag_freq, 'cm-1')
