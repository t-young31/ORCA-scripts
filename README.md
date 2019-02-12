# ORCA scripts

## analyse_TS

From a OptTS .out file extract the imaginary frequencies.If there is a single
negative frequency >100cm-1 the script will print the enthalpy and Gibbs free
energy.


## inp2xyz

From a .inp ORCA input file construct a .xyz file. Also implemented for
automator in MacOS.


## mk_scan_inp

Tool to generate geometry scans from: (1) a .inp file containing the geometry
(2) atom labels to scan e.g. C1 C2 to scan the first and second carbons in the
geometry. A number of options then are requested, all of which have reasonable
defaults.


## mk_TS

Tool to generate a TS search from a scan.out file. Once again reasonable defaults
are set.


## thermochemistry

Tool to extract E/H/G from all .out files in a folder and deposit them in a .csv.

## out2xyz
Tool to convert a .out file into a geometry. Will extract the last set of xyzs from the file.
Useful for visualising the progress of geometry optimisations. 
