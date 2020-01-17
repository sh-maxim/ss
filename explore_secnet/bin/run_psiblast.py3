#!./nnpython3
#2018-19 (C) Maxim Shapovalov, Dr. Roland Dunbrack Lab, Fox Chase Cancer Center, Philadelphia, PA, USA
#Version 1.0.3

import sys
import os

print('* script: %s' % (' '.join(sys.argv[:])))
#executale refers to the embedded python
app_directory = os.path.dirname(sys.executable)

#/app/secnet/new_fasta/5YDNA.fasta
_ffilename = sys.argv[1]
#{1, 2, 4, 8} or is not provided at all as the second argument
if len(sys.argv) >= 3:
    _cpu = int(sys.argv[2])
else:
    import multiprocessing
    _cpu = multiprocessing.cpu_count()
print('* script: psiblast is set to use %s CPU cores' % _cpu)

_output_for_mtx_with_slash = "%s/features/psiblast/" % (app_directory)
_basename_without_extension = os.path.splitext(os.path.basename(_ffilename))[0]

#detection of operating system family
_platform = sys.platform.lower()
if "linux" in _platform or "unix" in _platform:
    os_dir = 'unix'
elif "darwin" in _platform or "mac" in _platform:
    os_dir = 'macos'
elif "win" in _platform:
    os_dir = 'win'
    print('* error: Windows is not supported yet')
    exit(100)

if os.path.isfile('%s%s.mtx.2' % (_output_for_mtx_with_slash, _basename_without_extension)):
    print('* script: psiblast features already exist -- skipping their regeneration')
    exit(0)

_command_to_exe = "%s/3rd_software/%s/ncbi-blast-2.6.0+/bin/psiblast -db %s/3rd_databases/blast/uniref90.fasta -query %s -inclusion_ethresh 0.001 -evalue 10 -save_pssm_after_last_round -out_ascii_pssm %s%s.mtx -num_iterations 2 -num_threads %d -save_each_pssm > /dev/null 2>&1" % (app_directory, os_dir, app_directory, _ffilename, _output_for_mtx_with_slash, _basename_without_extension, _cpu)

print('* command: %s' % (_command_to_exe))
os.system(_command_to_exe)

