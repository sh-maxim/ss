#2018-19 (C) Maxim Shapovalov, Dr. Roland Dunbrack Lab, Fox Chase Cancer Center, Philadelphia, PA, USA
print('')
print('# SecNet, Protein secondary structure prediction software')
print('# 2018-19 (C) Maxim Shapovalov, Roland Dunbrack Lab, Slobodan Vucetic, Fox Chase Cancer Center and Temple University, Philadelphia, PA, USA')
print('# Version 1.1.4')
print('# Jan 13, 2020')
print('')

import os
import sys
app_directory = os.path.dirname(sys.executable)

#Loading additional help from README file
with open('%s/README' % app_directory, 'r') as _readme_file:
    readme_epilog = _readme_file.read()

import argparse
#Arguments
myArgParser = argparse.ArgumentParser(add_help=True, epilog=readme_epilog, formatter_class=argparse.RawDescriptionHelpFormatter)

optionalNamed = myArgParser._action_groups.pop()
requiredNamed = myArgParser.add_argument_group('required named arguments')
requiredNamed.add_argument("-i", "--input", help='for example, -i abcd.fasta or --input /home/user/abcd.seq or -i "./input_dir/*.fasta" or -i "/data/*.seq" or -i /data/dir_with_sequences (for a directory, processes all *.seq and *.fasta). Do not forget to include "..." quotes for * or ? wildcard matching.', required=True)
requiredNamed.add_argument("-o", "--output", help='for example, -o /home/user/output or --output ./project/', required=True)
requiredNamed.add_argument("-l", "--label", choices=['3', '4', '5', '8', 'all'], help='for example, -l 8 or --label 3 --rule 1 or -l all', required=True)
optionalNamed.add_argument("-r", "--rule", choices=['1', '2', 'both'], help='for example, -r 1 or --rule 2 or -r both')
optionalNamed.add_argument("-q", "--quiet", action='store_true', help='limits standard output to reporting processed sequences with -q or --quiet')
optionalNamed.add_argument("-c", "--cpu", type=int, help='by default secnet uses all available CPU cores, for example override it with -c 2 or --cpu 4 or -c 8')
myArgParser._action_groups.append(optionalNamed)

#Argument parsing
args = myArgParser.parse_args()
python_symbolic_link = "%s/nnpython3" % app_directory

#/app/secnet/new_fasta
#/app/secnet/new_fasta/
#'/app/secnet/new_fasta/*.fasta'
#'/app/secnet/new_fasta/*.seq'
#'/app/secnet/new_fasta/5V*.fasta'
#'/app/secnet/new_fasta/ab*.seq'
#'/app/secnet/new_fasta/6B*.*'
#'/app/secnet/new_fasta/?BSUB.fasta'
#/app/secnet/new_fasta/6BSUB.fasta
#/app/secnet/new_fasta/abcd1.seq
expression_with_fasta_files = args.input

if not args.quiet:
    print('None:\n=====\nIf wildcard characters such as * or ? are used to select input sequence files,\nplease make sure to quote the input argument\nwith either single or double quotes, for example \"/my_input_folder/*.fasta\" or \'*.seq\'\n')
    print('INPUT for processing <-- %s' % expression_with_fasta_files)


#/home/user/work/pred
dir_with_output_ss_files = args.output

if not args.quiet:
    print('OUTPUT --> %s' % dir_with_output_ss_files)
    print('')

import glob
if os.path.isdir(expression_with_fasta_files):
   glob_to_process = glob.glob(expression_with_fasta_files + '/' + '*' + '.fasta')
   glob_to_process += glob.glob(expression_with_fasta_files + '/' + '*' + '.seq')
else:
   glob_to_process = glob.glob(expression_with_fasta_files)

_success_count = 0
_count = 0
for _ffilename in glob_to_process:
    _count += 1

    _ensured_ffile = os.path.abspath(_ffilename)
    if not args.quiet:
        print("")
        print('%d of %d] processing of %s' % (_count, len(glob_to_process), _ensured_ffile))
    else:
        print('%d of %d] processing of %s' % (_count, len(glob_to_process), _ensured_ffile), end = "")
    sys.stdout.flush()

    if args.cpu == None:
        cpu_string = ''
        cpu_string_nu2 = ''
    else:
        cpu_string = ' %d' % args.cpu
        cpu_string_nu2 = ' --cpu %d' % args.cpu

    if not args.quiet:
        _quiet_redirection = ''
    else:
        _quiet_redirection = ' > /dev/null 2>&1'

    os.system('%s %s/bin/run_psiblast.py3 %s%s%s' % (python_symbolic_link, app_directory, _ensured_ffile, cpu_string, _quiet_redirection))
    sys.stdout.flush()

    os.system('%s %s/bin/run_hmm.py3 %s%s%s' % (python_symbolic_link, app_directory, _ensured_ffile, cpu_string, _quiet_redirection))
    sys.stdout.flush()

    _basename_without_extension = os.path.splitext(os.path.basename(_ensured_ffile))[0]

    if args.label == 'all':
        __return_value = os.system('%s %s/bin/ss_nn_load_and_predict.py3 -l 8 -i %s -o %s%s%s' % (python_symbolic_link, app_directory, _ensured_ffile, dir_with_output_ss_files, cpu_string_nu2, _quiet_redirection))
        __return_value = os.system('%s %s/bin/ss_nn_load_and_predict.py3 -l 5 -i %s -o %s%s%s' % (python_symbolic_link, app_directory, _ensured_ffile, dir_with_output_ss_files, cpu_string_nu2, _quiet_redirection))
        __return_value = os.system('%s %s/bin/ss_nn_load_and_predict.py3 -l 4 -i %s -o %s%s%s' % (python_symbolic_link, app_directory, _ensured_ffile, dir_with_output_ss_files, cpu_string_nu2, _quiet_redirection))
        __return_value = os.system('%s %s/bin/ss_nn_load_and_predict.py3 -l 3 -r 1 -i %s -o %s%s%s' % (python_symbolic_link, app_directory, _ensured_ffile, dir_with_output_ss_files, cpu_string_nu2, _quiet_redirection))
        __return_value = os.system('%s %s/bin/ss_nn_load_and_predict.py3 -l 3 -r 2 -i %s -o %s%s%s' % (python_symbolic_link, app_directory, _ensured_ffile, dir_with_output_ss_files, cpu_string_nu2, _quiet_redirection))
    else:
        if args.rule == 'both' and args.label == '3':
            __return_value = os.system('%s %s/bin/ss_nn_load_and_predict.py3 -l %s -r 1 -i %s -o %s%s%s' % (python_symbolic_link, app_directory, args.label, _ensured_ffile, dir_with_output_ss_files, cpu_string_nu2, _quiet_redirection))
            __return_value = os.system('%s %s/bin/ss_nn_load_and_predict.py3 -l %s -r 2 -i %s -o %s%s%s' % (python_symbolic_link, app_directory, args.label, _ensured_ffile, dir_with_output_ss_files, cpu_string_nu2, _quiet_redirection))
        else:
            if args.rule == None or args.rule == 'both':
                string_rule = ''
            else:
                string_rule = ' -r %s' % args.rule
            __return_value = os.system('%s %s/bin/ss_nn_load_and_predict.py3 -l %s%s -i %s -o %s%s%s' % (python_symbolic_link, app_directory, args.label, string_rule, _ensured_ffile, dir_with_output_ss_files, cpu_string_nu2, _quiet_redirection))

    if __return_value == 0:
        _success_count = _success_count + 1
        if args.quiet:
            print(' +')
    else:
        if args.quiet:
            print(' -')

print("")
print("%d succeeded out of total of %d" % (_success_count, len(glob_to_process)))
print('<== ALL TASKS COMPLETED ==>\n')

