#!/usr/bin/env bash

# ############################
# How to launch this installer
# ############################
# 1. open a terminal window or command prompt
# 2. change the current directory to where you downloaded this installer, for example 'cd /home/user/Downloads'
# 3.1 launch the installer with 'bash ./install_secnet.bash' OR
# OR
# 3.2.1 give executable permission to the downloaded file with 'chmod u+ax ./install_secnet.bash'
# 3.2.2 launch the installer with './install_secnet.bash'

# #######
# Version
# #######
# Installer of 'SecNet', template-free protein secondary structure prediction software
InstallerVersion=1.0.19

# ########
# Platform
# ########
# 
# Supported on Unix and Mac

# #######
# License
# #######
# SecNet, template-free protein secondary structure prediction software
# Copyright (c) 2018-2019, Maxim Shapovalov (1,2), Roland L. Dunbrack, Jr. (1,^), Slobodan Vucetic (2,^)
# All rights reserved.
# 
# (1): Fox Chase Cancer Center, 333 Cottman Avenue, Philadelphia PA 19111, USA
# (2): Temple University, 1801 N Broad Street, Philadelphia PA 19122, USA
# (^): Corresponding Authors, roland dot dunbrack at fccc dot edu and vucetic at temple dot edu
# 
# BSD 3-Clause License
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE

echo "# "
echo "# Welcome to Installer of 'SecNet', template-free protein secondary structure prediction software"
echo "# (c) 2018-2019, Maxim Shapovalov, Roland L. Dunbrack, Jr., Slobodan Vucetic"
echo "# Installer version $InstallerVersion"
echo "# http:/dunbrack.fccc.edu/ss and https://github.com/sh-maxim/ss"
echo "# "
echo ""

UNAME=$(uname)
if [ "$UNAME" == "Linux" ] ; then
   OS_TYPE="unix"
   OS_TYPE_LONG="Unix"
   OS_EXAMPLE_INSTALL_DIR="/home/user/secnet"
elif [ "$UNAME" == "Darwin" ] ; then
   OS_TYPE="mac"
   OS_TYPE_LONG="Mac OS"
   OS_EXAMPLE_INSTALL_DIR="/Users/user/secnet"
elif [[ "$UNAME" == CYGWIN* || "$UNAME" == MINGW* ]] ; then
   OS_TYPE="win"
   OS_TYPE_LONG="Windows"
   OS_EXAMPLE_INSTALL_DIR="C:\\Users\\User\\secnet"
   echo ""
   echo "-----> ERROR: Windows is not supported yet"
   echo "Please use Unix or MacOS operating system."
   exit 1
fi
echo "* detected operating system family is $OS_TYPE_LONG"

SCRIPT="$(cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd)/$(basename $0)"
echo "* executing $SCRIPT"


if true; then
echo ""
echo "1) The installation takes between 1 and 6 hours and greatly depends on Internet speed"
echo "between you and our server. 95% of downloaded content is the required sequence databases"
echo "against which the software was trained to guarantee the stated accuracy in our publication."
echo ""
echo "2) The installer will NOT disrupt your systemwide or user-specific Python or shell environment"
echo "or alignment software; instead required Python and its libraries, all 3rd-party software and"
echo "databases will be installed locally to the SecNet kit directory."
echo ""
echo "3) This Installer will download files from our server, dunbrack.fccc.edu. If our server times out"
echo "or you have downloading problems or slow speed, please switch to a different installer, named"
echo "'install_secnet_from_dunbrack.bash'. It will download all files from our Github server."
echo ""
echo "4) Uninstallation of SecNet kit is simple as running the command, 'rm -rf ./secnet_kit_directory'"
echo ""
read -p "--> Full installation path with write permission, such as $OS_EXAMPLE_INSTALL_DIR? " InstallDir
fi


echo "* installing SecNet kit to $InstallDir"
echo "* installation started at `date`"
PARENT_OF_INSTALL_DIR=`dirname $InstallDir`
if [ ! -d $PARENT_OF_INSTALL_DIR ]; then
   echo ""
   echo "-----> ERROR: Directory $PARENT_OF_INSTALL_DIR does not exist. Please try again and enter a valid path."
   exit 2
fi
mkdir $InstallDir

if [ "$OS_TYPE" == "unix" ] ; then
   FREE=`df -BG --output=avail "$InstallDir" | tail -n1`
   FREE="${FREE%?}"
elif [ "$OS_TYPE" == 'mac' ] ; then
   FREE=`df -Pg $InstallDir | sed 1d | grep -v used | awk '{ print $4 }'`
fi
echo "* free space of $FREE GB is detected"
if [[ $FREE -lt 75 ]]; then
   echo ""
   echo "-----> ERROR: Not enough free disk space is detected."
   echo "SecNet kit requires at least 75 GB for installation, mostly for databases."
   echo "Please clean the disk and try again."
   exit 3
fi;


sleep 5
InstallDir="$(cd $InstallDir > /dev/null 2>&1 && pwd)"
InstallDir=${InstallDir%/}
echo "* full path of SecNet kit is $InstallDir"
cd $InstallDir
mkdir "$InstallDir/download"


if true; then
echo ""
echo "* 1 of 15: downloading secnet directory structure"
echo "*************************************************"
echo ""
sleep 5
URL_ROOT_DIR_TAR_GZ='http://dunbrack.fccc.edu/ss/downloads/secnet_root.tar.gz'
LOCAL_ROOT_DIR_TAR_GZ='download/secnet_root.tar.gz'
if [ "$OS_TYPE" == "unix" ] ; then
   wget $URL_ROOT_DIR_TAR_GZ -O $LOCAL_ROOT_DIR_TAR_GZ
elif [ "$OS_TYPE" == 'mac' ] ; then
   curl $URL_ROOT_DIR_TAR_GZ -o $LOCAL_ROOT_DIR_TAR_GZ
fi
echo ""
echo "* 2 of 15: extracting secnet directory structure"
echo "************************************************"
echo ""
tar -xvzf $LOCAL_ROOT_DIR_TAR_GZ --directory $InstallDir
rm $LOCAL_ROOT_DIR_TAR_GZ
fi


if true; then
echo ""
echo "* 3 of 15: downloading trained models"
echo "*************************************"
echo ""
sleep 5
URL_MODELS_TAR_GZ='http://dunbrack.fccc.edu/ss/downloads/models.tar.gz'
LOCAL_MODELS_TAR_GZ='download/models.tar.gz'
if [ "$OS_TYPE" == "unix" ] ; then
   wget $URL_MODELS_TAR_GZ -O $LOCAL_MODELS_TAR_GZ
elif [ "$OS_TYPE" == 'mac' ] ; then
   curl $URL_MODELS_TAR_GZ -o $LOCAL_MODELS_TAR_GZ
fi
echo ""
echo "* 4 of 15: extracting trained models"
echo "************************************"
echo ""
tar -xvzf $LOCAL_MODELS_TAR_GZ --directory $InstallDir
rm $LOCAL_MODELS_TAR_GZ
fi


if true; then
echo ""
echo "* 5 of 15: downloading third-party software"
echo "*******************************************"
echo ""
sleep 5
URL_3RD_SOFTWARE_TAR_GZ='http://dunbrack.fccc.edu/ss/downloads/3rd_software.tar.gz'
LOCAL_3RD_SOFTWARE_TAR_GZ='download/3rd_software.tar.gz'
if [ "$OS_TYPE" == "unix" ] ; then
   wget $URL_3RD_SOFTWARE_TAR_GZ -O $LOCAL_3RD_SOFTWARE_TAR_GZ
elif [ "$OS_TYPE" == 'mac' ] ; then
   curl $URL_3RD_SOFTWARE_TAR_GZ -o $LOCAL_3RD_SOFTWARE_TAR_GZ
fi
echo ""
echo "* 6 of 15: extracting third-party software"
echo "******************************************"
echo ""
tar -xvzf $LOCAL_3RD_SOFTWARE_TAR_GZ --directory $InstallDir
rm $LOCAL_3RD_SOFTWARE_TAR_GZ
fi


if true; then
echo ""
echo "* 7 of 15: downloading Anaconda3 of version 4.2.0 with Python 3.5.2"
echo "*******************************************************************"
echo ""
sleep 5
if [ "$OS_TYPE" == "unix" ] ; then
   URL_ANACONDA3="https://repo.anaconda.com/archive/Anaconda3-4.2.0-Linux-x86_64.sh"
   ANACONDA_LOCAL_FILENAME="download/Anaconda3-4.2.0-Linux-x86_64.sh"
elif [ "$OS_TYPE" == 'mac' ] ; then
   URL_ANACONDA3="https://repo.anaconda.com/archive/Anaconda3-4.2.0-MacOSX-x86_64.sh"
   ANACONDA_LOCAL_FILENAME="download/Anaconda3-4.2.0-MacOSX-x86_64.sh"
fi
if [ "$OS_TYPE" == "unix" ] ; then
   wget $URL_ANACONDA3 -O $ANACONDA_LOCAL_FILENAME
elif [ "$OS_TYPE" == 'mac' ] ; then
   curl $URL_ANACONDA3 -o $ANACONDA_LOCAL_FILENAME
fi
ANACONDA3_DIR="$InstallDir/anaconda3"
echo ""
echo "* 8 of 15: installing Anaconda3 of version 4.2.0 with Python 3.5.2 as standalone to the local SecNet kit directory, to $ANACONDA3_DIR"
echo "*************************************************************************************************************************************"
echo ""
bash $ANACONDA_LOCAL_FILENAME -b -p $ANACONDA3_DIR
rm $ANACONDA_LOCAL_FILENAME
fi


if true; then
echo ""
echo "* 9 of 15: downloading current execution code"
echo "*********************************************"
echo ""
sleep 5
URL_CODE_TAR_GZ='http://dunbrack.fccc.edu/ss/downloads/source.tar.gz'
LOCAL_CODE_TAR_GZ='download/source.tar.gz'
if [ "$OS_TYPE" == "unix" ] ; then
   wget $URL_CODE_TAR_GZ -O $LOCAL_CODE_TAR_GZ
elif [ "$OS_TYPE" == 'mac' ] ; then
   curl $URL_CODE_TAR_GZ -o $LOCAL_CODE_TAR_GZ
fi
echo ""
echo "* 10 of 15: exctacting current execution code"
echo "*********************************************"
echo ""
tar -xvzf $LOCAL_CODE_TAR_GZ --directory $InstallDir
rm $LOCAL_CODE_TAR_GZ
fi


if true; then
echo ""
echo "* 11 of 15: configuring local paths in downloaded execution code"
echo "****************************************************************"
echo ""
sleep 5
echo "#!$InstallDir/nnpython3" > ./bin/template/template.nnpython3.shebang
cat ./bin/template/template.nnpython3.shebang ./bin/template/template.configure_secnet.py3 > ./bin/configure_secnet.py3
chmod a+x ./bin/configure_secnet.py3
cat ./bin/template/template.nnpython3.shebang ./bin/template/template.secnet.py3 > secnet.py3
chmod a+x secnet.py3
cat ./bin/template/template.nnpython3.shebang ./bin/template/template.run_psiblast.py3 > ./bin/run_psiblast.py3
chmod a+x ./bin/run_psiblast.py3
cat ./bin/template/template.nnpython3.shebang ./bin/template/template.run_hmm.py3 > ./bin/run_hmm.py3
chmod a+x ./bin/run_hmm.py3
cat ./bin/template/template.nnpython3.shebang ./bin/template/template.ss_nn_load_and_predict.py3 > ./bin/ss_nn_load_and_predict.py3
chmod a+x ./bin/ss_nn_load_and_predict.py3
fi


if true; then
echo ""
echo "* 12 of 15: executing configuration and installation of required libraries in Python3 installed locally in the SecNet kit directory, $ANACONDA3_DIR"
echo "***************************************************************************************************************************************************"
echo ""
sleep 5
ln -s "$ANACONDA3_DIR/bin/python3" ./nnpython3
./nnpython3 ./bin/configure_secnet.py3
fi


if true; then
echo ""
echo "* 13 of 15: downloading and extracting hmm database #1 of 2"
echo "***********************************************************"
echo ""
sleep 5
URL_NR70_TAR_GZ='http://dunbrack.fccc.edu/ss/databases/nr70.tar.gz'
LOCAL_NR70_TAR_GZ='download/nr70.tar.gz'
if [ "$OS_TYPE" == "unix" ] ; then
   wget $URL_NR70_TAR_GZ -O $LOCAL_NR70_TAR_GZ
elif [ "$OS_TYPE" == 'mac' ] ; then
   curl $URL_NR70_TAR_GZ -o $LOCAL_NR70_TAR_GZ
fi
tar -xvzf $LOCAL_NR70_TAR_GZ --directory $InstallDir/3rd_databases/hmm
rm $LOCAL_NR70_TAR_GZ
fi


if true; then
echo ""
echo "* 14 of 15: downloading and extracting hmm database #2 of 2"
echo "***********************************************************"
echo ""
sleep 5
URL_NR90_TAR_GZ='http://dunbrack.fccc.edu/ss/databases/nr90.tar.gz'
LOCAL_NR90_TAR_GZ='download/nr90.tar.gz'
if [ "$OS_TYPE" == "unix" ] ; then
   wget $URL_NR90_TAR_GZ -O $LOCAL_NR90_TAR_GZ
elif [ "$OS_TYPE" == 'mac' ] ; then
   curl $URL_NR90_TAR_GZ -o $LOCAL_NR90_TAR_GZ
fi
tar -xvzf $LOCAL_NR90_TAR_GZ --directory $InstallDir/3rd_databases/hmm
rm $LOCAL_NR90_TAR_GZ
fi


if true; then
echo ""
echo "* 15 of 15: downloading and extracting psiblast database"
echo "********************************************************"
echo ""
sleep 5
URL_BLAST_TAR_GZ='http://dunbrack.fccc.edu/ss/databases/uniref90.tar.gz'
LOCAL_BLAST_TAR_GZ='download/uniref90.tar.gz'
if [ "$OS_TYPE" == "unix" ] ; then
   wget $URL_BLAST_TAR_GZ -O $LOCAL_BLAST_TAR_GZ
elif [ "$OS_TYPE" == 'mac' ] ; then
   curl $URL_BLAST_TAR_GZ -o $LOCAL_BLAST_TAR_GZ
fi
tar -xvzf $LOCAL_BLAST_TAR_GZ --directory $InstallDir/3rd_databases/blast
rm $LOCAL_BLAST_TAR_GZ
fi


echo "* installation ended at `date`"
echo "* installation of SecNet is complete"

