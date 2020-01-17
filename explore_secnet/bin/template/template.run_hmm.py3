#2018-19 (C) Maxim Shapovalov, Dr. Roland Dunbrack Lab, Fox Chase Cancer Center, Philadelphia, PA, USA
#Version 1.0.2

import sys
import os
import shutil 

print('* script: %s' % (' '.join(sys.argv[:])))
#executale refers to the embedded python
app_directory = os.path.dirname(sys.executable)

#/app/secnet/new_fasta/5YDNA.fasta
_ffilename = sys.argv[1]
#{1, 2, 4, 8} or is not provided at all as the second argument
if len(sys.argv) >= 3:
    _cpu = sys.argv[2]
else:
    _cpu = None

if _cpu != None:
    _command_to_exe = 'bash %s/3rd_software/generic/process_hmm.bash -i %s -c %d' % (app_directory, _ffilename, int(_cpu))
else:
    _command_to_exe = 'bash %s/3rd_software/generic/process_hmm.bash -i %s' % (app_directory, _ffilename)
print('* command: %s' % (_command_to_exe))

os.system(_command_to_exe)

