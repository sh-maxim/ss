# *SecNet*, template-free protein secondary structure prediction software

Copyright (c) 2018-2019, Maxim Shapovalov<sup>†,‡</sup>, Roland L. Dunbrack, Jr.<sup>†,*</sup>, Slobodan Vucetic<sup>‡,\*</sup>  
All rights reserved.  
† Fox Chase Cancer Center, 333 Cottman Avenue, Philadelphia PA 19111, USA  
‡ Temple University, 1801 N Broad Street, Philadelphia PA 19122, USA  
\* Corresponding authors, roland dot dunbrack at fccc dot edu and vucetic at temple dot edu

## Description:
### *SecNet*
a software tool which reads a protein sequence in FASTA format and predicts secondary structure. There are several options of the secondary structure label alphabet. Among them are 3 labels (harder Rule #1 or easier Rule #2) and unambiguous 8 labels. We also provide 2 new alphabets with 4 and 5 labels. The tool allows selection of one of these 5 alphabets for prediction purposes.

### *Set2018*
a rigorously prepared data set, **Set2018** which includes training, validation and **Test2018** testing sets.

## Operating Systems:

* **Unix**, all flavors
* **macOS** including the recent Catalina 10.15 which dropped support for 32-bit applications

The installer will not disrupt your systemwide or user-specific Python or shell environment or alignment software; instead required Python and its libraries, all 3rd-party software and databases will be installed locally to the SecNet kit directory.

## To unistall SecNet kit:
simply run a command: *rm -rf ./secnet_kit_directory*

## License
Open-source BSD 3-Clause License. [Full text is here.](http://dunbrack.fccc.edu/ss/explore/LICENSE)

## Download and Installation:

Download a tiny (11KB) **SecNet Kit Installer**. The installer will automatically download, install and configure all required components. Depending on Internet speed between you and our server, it usually takes between 1 and 6 hours. 95% of downloaded content is the required sequence databases against which the software was trained to guarantee the accuracy stated in our publication.

* **SecNet Kit Installer**
  * from [Github](http://dunbrack.fccc.edu/ss/explore/link) or [dunbrack.fccc.edu](http://dunbrack.fccc.edu/ss/explore/link)
  * open a terminal window or command prompt
  * change the current directory to the download location, for example *cd /home/user/Downloads*
  * launch the installer with:
    * *bash ./install_secnet.bash*
    * or give executable permission to the downloaded file with *chmod u+ax ./install_secnet.bash* and run with *./install_secnet.bash*
    * watch your favorite TV series for ~1-6 hours and come back :-)

* Download **Set2018** data set which includes training, validation and **Test2018** testing sets
  * from [Github](http://dunbrack.fccc.edu/ss/explore/link) or [dunbrack.fccc.edu](http://dunbrack.fccc.edu/ss/explore/link)

* Explore our SecNet Kit file and directory structure
  * from [Github](http://dunbrack.fccc.edu/ss/explore/link) or [dunbrack.fccc.edu](http://dunbrack.fccc.edu/ss/explore/link)

## Preprint:
Shapovalov MV, Dunbrack RL Jr., Vucetic S. Multifaceted analysis of training and testing convolutional neural networks for protein secondary structure prediction.PLoS ONE, Submitted. [Manuscript will be available soon.](https://journals.plos.org/plosone/)

## SecNet Tool Help:
<pre>
Quick start:
============
Please included QUICK_START file for a quick reference.

Proper execution of SecNet:
===========================
Please launch SecNet as an executable, i.e. ./secnet.py3; do NOT try to execute secnet.py3 with your own
python, for example please AVOID "/bin/python secnet.py3". Your python may not include required libraries.
Please execute secnet.py3 as executable, i.e. ./secnet.py3; for the proper execution the first line of
secnet.py3 includes a reference to Anaconda Python 3 locally installed to the SecNet kit directory.

Usage:
======
# SecNet, Protein secondary structure prediction software
# Version 1.1.4

usage: secnet.py3 [-h] -i INPUT -o OUTPUT -l {3,4,5,8,all} [-r {1,2,both}]
                  [-q] [-c CPU]

required named arguments:
  -i INPUT, --input INPUT
                        for example, -i abcd.fasta or --input
                        /home/user/abcd.seq or -i "./input_dir/*.fasta" or -i
                        "/data/*.seq" or -i /data/dir_with_sequences (for a
                        directory, processes all *.seq and *.fasta). Do not
                        forget to include "..." quotes for * or ? wildcard
                        matching.
  -o OUTPUT, --output OUTPUT
                        for example, -o /home/user/output or --output
                        ./project/
  -l {3,4,5,8,all}, --label {3,4,5,8,all}
                        for example, -l 8 or --label 3 --rule 1 or -l all

optional arguments:
  -h, --help            show this help message and exit
  -r {1,2,both}, --rule {1,2,both}
                        for example, -r 1 or --rule 2 or -r both
  -q, --quiet           limits standard output to reporting processed
                        sequences with -q or --quiet
  -c CPU, --cpu CPU     by default secnet uses all available CPU cores, for
                        example override it with -c 2 or --cpu 4 or -c 8

Labels and rules for 3 labels:
==============================
(1) 8 labels: H, E, C, T, G, S, B, I
    8 original DSSP labels are unchanged (C, S, B, T, I, G, H, E)
    Argument: --label 8 or -l 3

(2) 5 labels: H, E, C, T, G
    (C, S, B) -> C, (H, I) -> H, (E) -> E, (T) -> T, (G) -> G
    Argument: --label 5 or -l 5

(3) 4 labels: H, E, C, T
    (C, S, B, G) -> C, (H, I) -> H, (E) -> E, (T) -> T
    Argument: --label 4 or -l 4

(4) 3 harder to predict labels of Rule #1: H, E, C
    (C, S, T) -> C, (H, I, G) -> H, (E, B) -> E
    Argument: --label 3 or -l 3 or --label 3 --rule 1 or -l 3 -r 1
    Note: The rule option is only applicable to 3 labels. If no option is specified, Rule #1 is by default.

(5) 3 easier to predict labels of Rule #2: H, E, C
    (C, S, B, T, I, G) -> C, (H) -> H, (E) -> E
    Argument: --label 3 --rule 2 or -l 3 -r 2

(6) 3 labels with both Rule #1 and Rule #2
    Argument: --label 3 --rule both or -l 3 -r both

(7) all sets of the above will be predicted
    Argument: --label all or -l all

Input:
======
(1) Single file with FASTA-formatted sequence
    --input /home/user/secnet/input/example.fasta or -i ~/project/favorite.seq or --input ABCD4.sequence

(2) Directory with all sequence files matching *.seq and *.fasta extensions
    --input /data/myproject/dir_with_seqs -i ./all_seq/

(3) Wildcard matching, please use ' or " quotes
    otherwise a shell may expand all matching files into a set of program arguments and the program fails
    --input '/pdb/2A*.fasta' or -i "~/project_jan/*.seq" or -i "ABCD?.seq"

Output directory:
=================
Program will predict requested sets of labels with .ss8 or .ss5, .ss4, .ss3rule1 or .ss3rule2 extensions.
The base name of generated files will be taken from corresponding input files by removing their extensions,
for example example.fasta will lead to example.ss8 or ABCD4.seq will produce ABCD4.ss3rule1
    --output ./output or -o /mydata/output/

CPU:
====
By default, SecNet will detect a number of available CPU cores and will use all of them to run 3rd-party
software to generate input features and to process neural networks to make predictions.
A user can limit a number of used CPU cores to make the system more responsive during the prediction for
other user tasks. It will take longer time to make the predictions.
    --cpu 4 or -c 2 or --cpu 7

Quiet:
======
A user may reduce amount of standard output with the following optional flag. If no such flag is provided,
the output includes all information about running 3rd-party software for input feature generation and
additional information from neural networks such as 10 predictions from 10 neural networks before taking
the major vote. If you wish suppress any output during the execution, you may add "> /dev/null 2>&1"
at the end of your command.
    --quiet

Help:
=====
Prints required and optional arguments as well as this help.
    --help or -h

Kit directory and file structure:
=================================

3rd_databases      -- extracted downloaded sequence databases for psiblast and hmm feature generation
3rd_software       -- third-party software (psiblast and hmm)
                      with binaries for Unix and MacOS (supports Catalina with 64-bit support only)
anaconda3          -- locally installed Anaconda Python 3 with installed required Python libraries
bin                -- scripts with secnet subroutines
download           -- directory for temporary files during installation
EXAMPLE            -- directory with an example sequence and expected output with properly working software
features           -- saves generated input feature files, speeds up nnet computation for subsequent calls;
                      the content of the following subdirectories may be deleted later if needed
features/psiblast  -- saved input psiblast features with PSSM profiles from the 1st and 2nd rounds
                      (example.mtx.1 and exammple.mtx.2)
features/hhm       -- saved input hhm features with HHM parameters (example.hhm1)
features/temp      -- includes undeleted temporary files to track down errors for failed input features
input              -- includes example.fasta and 4 other sample sequences in FASTA format
models             -- trained neural networks for 5 sets of labels each with 10 cross-validation trainings
nnpython3          -- symbolic link to locally installed Anaconda Python 3
output             -- empty directory for output convenience
QUICK_START        -- quick start instructions with examples
README             -- a readme file with this content
secnet.py3         -- SecNet executable to be executed as ./secnet.py3 or /home/user/secnet_kit/secnet.py3
Test2018           -- files related to Test2018 data set from our paper
Test2018/input     -- 149 FASTA-formatted sequence files from Test2018
Test2018/expected  -- expected secondary-structure predictions for 5 label alphabets of 149 Test2018 sequences
Test2018/test.bash -- script testing your SecNet installation on Test2018 and saves results to Test2018/output.
                      You may compare your re-generated results with the expected ones from Test2018/expected.
                      It is a normal situation when due to different hardware & software your predictions and
                      expected predictions slightly vary by one or few labels. Your overall accurarcy will be
                      close within 0.01-0.03% to the one reported in our paper.
Test2018/output    -- an empty directory for output from Test2018/test.bash


Examples:
=========
#To predict secondary structure of a single sequence with the 8-label DSSP alphabet:
./secnet.py3 --input input/example.fasta --output output/ --label 8

#Please note you need to use double or single quotes around wildcard characters such as '*.seq' or '*.fasta":
./secnet.py3 --input "input/*.fasta" --output output/ --label 8

#If you wish to process all testing entries in Test2018:
./secnet.py3 --input Test2018/input --output Test2018/output --label 3 --rule 1

#To generate all available label sets: {8 labels, 5 labels, 4 labels and 3 labels of both Rule #1 and Rule #2):
./secnet.py3 --input input/5UB3B.fasta --output output/ --label all

#4 labels only:
./secnet.py3 --input input/5UB3B.fasta --output output/ --label 4

#5 labels only:
./secnet.py3 --input input/5UB3B.fasta --output output/ --label 5

#The easier 3 labels of Rule #2:
./secnet.py3 --input input/5UB3B.fasta --output output/ --label 3 --rule 2

#To limit CPU usage to a single core with longer execution time (by default all CPU cores are used):
./secnet.py3 --input "input/*.fasta" --output output/ --label 8 --cpu 1

#If you have 8 cores, you may limit to 4 cores:
./secnet.py3 --input "input/*.fasta" --output output/ --label 8 --cpu 4

#To reduce amount of standard output and only report whether each sequence was successfully processed:
./secnet.py3 --input "input/*.fasta" --output output/ --label 8 --quiet
</pre>
