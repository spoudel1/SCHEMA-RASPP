SCHEMA-RASPP
============

This is a software package for protein engineers. It uses protein structure and sequence information to aid researchers in designing protein recombination libraries.

These tools can calculate SCHEMA energies of chimeric proteins and run the RASPP algorithm to find optimal library designs. The package includes documentation and examples. 

SCHEMA was developed in the laboratory of Frances H. Arnold at the California Institute of Technology.

References:

Voigt, C. et al., "Protein building blocks preserved by recombination," Nature Structural Biology 9(7):553-558 (2002).
Meyer, M. et al., "Library analysis of SCHEMA-guided recombination," Protein Science 12:1686-1693 (2003).
Otey, C. et al., "Functional evolution and structural conservation in chimeric cytochromes P450: Calibrating a structure-guided approach," Chemistry & Biology 11:1-20 (2004)
Silberg, J. et al., "SCHEMA-guided protein recombination," Methods in Enzymology 388:35-42 (2004).
Endelman, J. et al., "Site-directed protein recombination as a shortest-path problem," Protein Engineering, Design & Selection 17(7):589-594 (2005).


To run this version follow the steps:
1) Download/clone the folder locally to your computer
2) copy the run_schema.sh from the folder to your working directory. Make sure your working directory has atleast two other files: 1) prealinged file that includes all the sequences that you want to align where the first seq is your reference sequence. 2) pdb file. Pdb file name has to match the ref seq name in the sequence file
3) update SCHEMADIR path in run_schema.sh to point to the folder where you downloaded/cloned the program
4) to run cal run_schema.sh and it takes three inputs: 1)prealigned seq file 2) pdb file 3) number of crosspoints you want. see eg as below
     ./run_schema.sh prealigned.txt model.pdb 5
4) Step 4 will give you three files: 1) clustal.aln (this the file containing aligned sequences in clustal format), 2) contacts.txt (this contains contacts positions), 3) opt.txt - this contains the crossover points and their E and m scores. 
5) Pick the best crossover points from opt.txt file that you want to create the library from and save it to a file (say it's called xo.txt) so the xo.txt should only have one row as shown below if you picked 5 crossover points
    5 9 13 107 111
6) run run_schema.txt to get the chimera sequences. You will need to pass the file containing the best crossover points (e.g., xo.txt)
    ./run_schema.sh xo.txt
7) Step 6 will create two files: 1) energies.txt - this will contain all possible combination of chimeras and their E and m score, 2) Chimera_sequences.fasta - this contains the chimera sequence
