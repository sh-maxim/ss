# SecNet, template-free protein secondary structure prediction software

Copyright (c) 2018-2019, Maxim Shapovalov†,‡, Roland L. Dunbrack, Jr.†,*, Slobodan Vucetic‡,*
All rights reserved.
† Fox Chase Cancer Center, 333 Cottman Avenue, Philadelphia PA 19111, USA
‡ Temple University, 1801 N Broad Street, Philadelphia PA 19122, USA
* Corresponding authors, roland dot dunbrack at fccc dot edu and vucetic at temple dot edu

## Description:
### SecNet
a software tool which reads a protein sequence in FASTA format and predicts secondary structure. There are several options of the secondary structure label alphabet. Among them are 3 labels (harder Rule #1 or easier Rule #2) and unambiguous 8 labels. We also provide 2 new alphabets with 4 and 5 labels. The tool allows selection of one of these 5 alphabets for prediction purposes.

### Set2018
a rigorously prepared data set, Set2018 which includes training, validation and Test2018 testing sets.

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

