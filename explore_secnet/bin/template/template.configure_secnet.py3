# ########
# Platform
# ########
# 
# Supported on Unix/Mac/Windows with Python 3

# #########
# Execution
# #########
# This program is written for Python 3.
# Please make sure you are running this program with Python 3, NOT Python 2.
# 'python' from your terminal needs to link to Python 3, NOT Python 2.
# 
# For execution from a terminal, you may try:
# 
# Unix/Mac/Windows:
# -----------------
# python3 configure_secnet.py3
# python configure_secnet.py3
#
# Unix/Mac:
# ---------
# /usr/bin/python BetaTurnTool18.py2
# /usr/bin/python2 BetaTurnTool18.py2
# /usr/bin/env python BetaTurnTool18.py2
# /usr/bin/env python2 BetaTurnTool18.py2
#
# For Shebang (Hashbang) in Unix/Mac:
# -----------------------------------
# Make sure in the top line 'python3' links to Python 3
# If Python 3 is not linked with python3 but with python, please modify the top line to "#!/usr/bin/env python"
#
# Windows:
# --------
# C:\Python3\python3.exe configure_secnet.py3

# #######
# License
# #######
# Copyright (c) 2018-2019, Maxim Shapovalov (1,2), Slobodan Vucetic (2), Roland L. Dunbrack, Jr. (1,^)
# All rights reserved.
# 
# (1): Fox Chase Cancer Center, 333 Cottman Avenue, Philadelphia PA 19111, USA
# (2): Temple University, 1801 N Broad Street, Philadelphia PA 19122, USA
# (^): Corresponding Author, Roland dot Dunbrack at fccc dot edu
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

import sys
print('* python directory = ' + sys.prefix)
print('* python executable = ' + sys.executable)
print('* python version:\n' + sys.version)

global glob_operating_system; glob_operating_system = 'unix'
global glob_operating_system_full; glob_operating_system_full = 'Unix'

#detection of operating system family
_platform = sys.platform.lower()
if "linux" in _platform or "unix" in _platform:
    glob_operating_system = 'unix'
    glob_operating_system_full = 'Unix'
elif "darwin" in _platform or "mac" in _platform:
    glob_operating_system = 'mac'
    glob_operating_system_full = 'Mac OS'
elif "win" in _platform:
    glob_operating_system = 'win'
    glob_operating_system_full = 'Windows'

print("* detected operating system family = \'%s\'" % glob_operating_system_full)
if glob_operating_system in ['win', 'unix', 'mac']:
    import os
    _can_write_to_python_folder = os.access(sys.prefix, os.W_OK)
    if _can_write_to_python_folder:
        print("* can install to the selected python folder, %s" % sys.prefix)
        print("* therefore trying to install required python modules there")
    else:
        print("* cannot install to the selected python folder, %s" % sys.prefix)
        print("* therefore trying to install required python modules locally in your home directory")

import os
os.environ["KERAS_BACKEND"] = 'theano'

#automatic installation of required python packages in Unix/Mac/Windows
_required_packages = [ \
                       ['h5py','h5py==2.6.0'], \
                       ['numpy','numpy==1.11.1'], \
                       ['scipy','scipy==0.18.1'], \
                       ['six','six==1.10.0'], \
                       ['theano','theano==0.8.2'], \
                       ['keras','keras==1.1.2'] \
                     ]

for _package in _required_packages:
        try:
            import pip
            try:
                from pip import main as pipmain
                print("* installing required module, \'%s\' with detected older python module installer, \'pip\'" % _package[1])
            except ImportError:
                from pip._internal import main as pipmain
                print("* installing required module, \'%s\' with detected newer python module installer, \'pip\'" % _package[1])
            if _can_write_to_python_folder == True:
                pipmain(['install', _package[1]])
            else:
                pipmain(['install', '--user', _package[1]])
            #exec(_package[0] + " = __import__(_package[0])")
        except Exception as _e:
            print("* configuration encountered a problem: %s" % _e)

