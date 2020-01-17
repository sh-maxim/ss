#!./nnpython3
#2018-19 (C) Maxim Shapovalov, Roland Dunbrack, Slobodan Vucetic, Philadelphia, PA, USA
#Prediction of protein secondary structure with neural networks
#Load and predict
_AppVersion = '1.16.4'
__return_value = 0

import sys
import os
#executale refers to the embedded python
app_directory = os.path.dirname(sys.executable)

print('* predict: %s of Version %s' % (sys.argv[0], _AppVersion))
print('* predict: application command: ' + ' '.join(sys.argv[0:]))
print('* predict: kit directory: ' + app_directory)
print('* predict: python version: ' + sys.version)

import argparse
#Arguments
myArgParser = argparse.ArgumentParser(add_help=True)

optionalNamed = myArgParser._action_groups.pop()
requiredNamed = myArgParser.add_argument_group('required named arguments')
requiredNamed.add_argument("-i", "--input", help='for example, -i abcd.fasta or --input abcd.seq', required=True)
requiredNamed.add_argument("-o", "--output", help='for example, -o /home/user/output or --output ./project', required=True)
requiredNamed.add_argument("-l", "--label", choices=[3, 4, 5, 8], type=int, help='for example, -l 8 or --label 3 --rule 1', required=True)

optionalNamed.add_argument("-r", "--rule", choices=[1, 2], type=int, help='for example, -r 1 or --rule 2')
optionalNamed.add_argument("-c", "--cpu", type=int, help='by default secnet uses all available cpu cores, for example override it with -c 2 or --cpu 4')
myArgParser._action_groups.append(optionalNamed)

#Argument parsing
args = myArgParser.parse_args()

#Static parameters
#{1, 2}: #1 has a progess bar, #2 is quite during prediction or training
VerboseLevel = 2
Hmm2SourcesIsOn = True

#Processing of static parameters
if Hmm2SourcesIsOn == True:
    HmmMode = 'hmm_div_99999'
    HMM_OUTSIDE_SEQ_DEFAULT_VALUE_1 = 99999.0
    HMM_OUTSIDE_SEQ_DEFAULT_VALUE_2 = 0.0
    if HmmMode == 'hmm_div_99999':
        HMM_NORMALIZATION_FACTOR = 99999.0
else:
    HmmMode = 'none'

#Argument processing
if args.label == 8:
    _output_extension = '.ss8'
    _labels_message = '8 labels: H, E, C, T, G, S, B, I'
    _labels_definition_during_training= '8 original DSSP labels unchanged (C, S, B, T, I, G, H, E)'
    _models_subpath = '8label'
elif args.label == 5:
    _output_extension = '.ss5'
    _labels_message = '5 labels: H, E, C, T, G'
    _labels_definition_during_training= '(C, S, B) -> C, (H, I) -> H, (E) -> E, (T) -> T, (G) -> G'
    _models_subpath = '5label_practical'
elif args.label == 4:
    _output_extension = '.ss4'
    _labels_message = '4 labels: H, E, C, T'
    _labels_definition_during_training= '(C, S, B, G) -> C, (H, I) -> H, (E) -> E, (T) -> T'
    _models_subpath = '4label_practical'
elif args.label == 3:
    if args.rule == None or args.rule == 1:
        _output_extension = '.ss3rule1'
        _labels_message = '3 labels of Rule #1: H, E, C'
        _labels_definition_during_training= '(C, S, T) -> C, (H, I, G) -> H, (E, B) -> E'
        _models_subpath = '3label_rule1_harder'
    elif args.rule == 2:
        _output_extension = '.ss3rule2'
        _labels_message = '3 labels of Rule #2: H, E, C'
        _labels_definition_during_training= '(C, S, B, T, I, G) -> C, (H) -> H, (E) -> E'
        _models_subpath = '3label_rule2_easier'
    else:
        raise(Exception('unexpected rule for 3 labels'))
else:
    raise(Exception('unexpected number of labels for secondary structure'))


print('* predict: labels for prediction: ' + _labels_message)
print('* predict: label definition: ' + _labels_definition_during_training)

FastaFInput = '/home/user/DebugID.fasta'
FastaFInput = args.input
#creating a list of sequence files to process
preFastaFList = []
if not os.path.isdir(FastaFInput):
    preFastaFList.append(FastaFInput)
else:
    import glob
    for _ffilename in glob.glob(FastaFInput + '*' + '.fasta'):
        preFastaFList.append(_ffilename)

#creating the final list of sequences files to process based on previously predicted files
FastaFList = []
for FastaFFile in preFastaFList:
    my_seq_id = os.path.splitext(os.path.basename(FastaFFile))[0]
    if os.path.isdir(args.output) == True:
        _output_ss_ffile = os.path.join(args.output, my_seq_id + _output_extension)
    else:
        _output_ss_ffile = args.output

    if os.path.isfile(_output_ss_ffile):
        print('* predict: prediction file already exists -- skipping its regeneration: %s' % _output_ss_ffile)
    else:
        FastaFList.append(FastaFFile)

#return with success code -- prediction files were previously processed
if len(FastaFList) == 0:
    sys.exit(__return_value)

#loading and reporting some python libraries
os.environ["KERAS_BACKEND"] = 'theano'
import numpy as np
from keras.models import load_model
import theano
print('* theano: ' + theano.__version__)
import keras
print('* keras: ' + keras.__version__)

#cpu parsing
if args.cpu == None:
    import multiprocessing
    args.cpu = multiprocessing.cpu_count()

os.environ['OMP_NUM_THREADS'] = str(args.cpu)
print('* neural network calculations will use %d CPU cores' % args.cpu)


ModelsFPathNoSlash = "%s/models/%s" % (app_directory, _models_subpath)


nu_of_ensemble_models = 10
print('* predict: loading %d model from %s' % (nu_of_ensemble_models, ModelsFPathNoSlash))
sys.stdout.flush()
models = [None] * nu_of_ensemble_models
#reading one hdf5 file with everything: model, weights, optimizer, loss and optimizer state
for _cv in range(0, nu_of_ensemble_models):
    fpath_model_hdf5 = "%s/CV%d/model_config_weights_state_best_eps.hdf5" % (ModelsFPathNoSlash, _cv+1)
    print('* predict: loading model #' + str(_cv+1) + ", " + fpath_model_hdf5 + ' is %.2f MB' % (os.path.getsize(fpath_model_hdf5) / (1024.*1024.)))
    models[_cv] = load_model(fpath_model_hdf5)
    sys.stdout.flush()

    #using from the first model for all 10; they are all the same
    if _cv == 0:
        _fpath_required_input_npz = "%s/CV%d/required_input.npz" % (ModelsFPathNoSlash, _cv+1)
        required_input = np.load(_fpath_required_input_npz)

X_uniqueOrdered = required_input['X_uniqueOrdered']
y_uniqueOrdered = required_input['y_uniqueOrdered']
AaWindow = required_input['AaWindow']
MtxIntList = list(required_input['MtxIntList'])


for FastaFFile in FastaFList:
    print('* predict: FASTA-formatted sequence file is %s' % FastaFFile)
    fasta_file = open(FastaFFile, 'rt')
    my_seq_id = os.path.splitext(os.path.basename(FastaFFile))[0]
    print('* predict: base name of entry is %s' % my_seq_id)
    my_sequence = ''
    while True:
       fline = fasta_file.readline()
       if not fline:
          break
       fline = fline.rstrip()
       if len(fline) == 0 or '>' in fline:
           continue
       my_sequence += fline
    fasta_file.close()

    print('* predict: parsed sequence from the input file is:')
    print(my_sequence)
    if len(my_sequence) == 0:
        print('\n-----> predict: error: (-) empty protein sequence was parsed for %s => skipping entry altogether\n' % my_seq_id)
        __return_value = 10
        continue

    row = {}
    row['aa'] = my_sequence
    row['pdb5'] = my_seq_id

    if os.path.isdir(args.output) == True:
        _output_ss_ffile = os.path.join(args.output, row['pdb5'] + _output_extension)
    else:
        _output_ss_ffile = args.output
    print('* predict: prediction file will be %s' % _output_ss_ffile)

    if os.path.isfile(_output_ss_ffile):
        print('\n.....> predict: warning: prediction file, %s already exists, running again and overwritting it\n' % _output_ss_ffile)

    #HMM parsing
    if Hmm2SourcesIsOn == True:
        hmm_folder_with_slash = app_directory + '/features/hhm/'
        _hmm_ffileName = hmm_folder_with_slash + row['pdb5'] + '.' + 'hhm1'

        if os.path.isfile(_hmm_ffileName) == False:
            print('\n-----> predict: error: (-) hhm feature file does not exist for %s => skipping entry altogether\n' % row['pdb5'])
            __return_value = 20
            continue
        _fid_hmm = open(_hmm_ffileName, 'r')
        _isAtNULL = False
        _length_hmm = -1
        while True:
            _line = _fid_hmm.readline()
            if not _line:
                break

            if _length_hmm == -1 and len(_line) >= 4 and _line[0:4] == 'LENG':
                _length_hmm = int(_line.split()[1])

            if _length_hmm >=0 and len(_line) >= 7 and _line[0:7] == 'NULL   ':
                _isAtNULL = True
                #skip 3 more NULL related lines
                _line = _fid_hmm.readline()
                _line = _fid_hmm.readline()
                _line = _fid_hmm.readline()
                break

        #np.finfo('float32').max --> 3.4028235e+38
        _hmm_matrix = None
        _aa_from_hmm = ''
        _count_hmm = 0
        if _length_hmm >=0 and _isAtNULL == True:
            _hmm_matrix = np.zeros([_length_hmm, 30], 'float32')
            while True:
                _line = _fid_hmm.readline()
                if not _line:
                    if _count_hmm != _length_hmm:
                        raise Exception('predict: error: total number should be read before seing EOF.')
                    break


                if len(_line) >= 2 and _line[0:2] == '//':
                   if _count_hmm != _length_hmm:
                        raise Exception('precit: error: total number of records should match before seeing the end of the hmm-file line marker.')
                   else:
                        continue

                _split_line_1 = _line.split()
                _count_hmm += 1
                if _count_hmm != int(_split_line_1[1]):
                    raise Exception('predict: error: hmm numbering mismatch')
                _aa_from_hmm += _split_line_1[0]
                _line = _fid_hmm.readline()
                _split_line_2 = _line.split()
                _split_line = _split_line_1[2:(len(_split_line_1)-1)] + _split_line_2[0:len(_split_line_2)]
                _line = _fid_hmm.readline()

                for _i in range(0, len(_split_line)):
                    if _split_line[_i] == '*':
                        _hmm_matrix[_count_hmm-1, _i] = np.float32(99999.0)
                    else:
                        _hmm_matrix[_count_hmm-1, _i] = np.float32(_split_line[_i])
        else:
            raise Exception('precit: error: either LEN record was not found or the beginning of NULL model record was not found.')
        _fid_hmm.close()
        if len(row['aa']) != len(_aa_from_hmm):
            if len(_aa_from_hmm) > len(row['aa']) and _aa_from_hmm.find(row['aa']) >= 0:
                _startInd = _aa_from_hmm.find(row['aa'])
                _aa_from_hmm = _aa_from_hmm[_startInd:_startInd+len(row['aa'])]
                _hmm_matrix = _hmm_matrix[_startInd:_startInd+len(row['aa']), :]
                pass
            else:
                raise Exception('precict: error: hmm aa seq has to be identical or sub-sequence of fasta sequence.')
        if row['aa'] != _aa_from_hmm:
            if _hmm_ffileName[-4:] == 'hhm1':
                raise Exception('predict: error: contents of aa seq from fasta and their hmm have to be the same.')
        if _hmm_ffileName[-4:] == 'hhm1':
            row['hmm_original'] = _hmm_matrix
            row['hmm'] = row['hmm_original']
    #end of #HMM parsing


    #psiblast profile parsing
    mtxRoundCount = len(MtxIntList)
    if mtxRoundCount > 0:
        #ApplicationMode-specific
        pssm_folder_with_slash = app_directory + '/features/psiblast/'
        UseFromPssmFile = required_input['UseFromPssmFile']

        _pssm_matrix = np.zeros([len(row['aa']), 20*mtxRoundCount], 'float32')
        is_this_pssm_record_ok = False
        #_mtx stands for elements number in the list, not the actual mtx round
        for _mtx in range(1, mtxRoundCount+1):
            is_this_pssm_record_ok = False

            if MtxIntList == [0]:
                ActualToTryRange = range(MtxIntList[_mtx-1],-1,-1)
            else:
                #for range(0, 0, -1) it will not loop:
                ActualToTryRange = range(MtxIntList[_mtx-1],0,-1)

            #This additional loop allows to go to mtx.3 if mtx.4 does not exist due to PsiBlast early convergence
            for _actual in ActualToTryRange:
                if _actual == 0:
                    pssm_ffile = pssm_folder_with_slash + row['pdb5'] + '.' + 'mtx'
                else:
                    pssm_ffile = pssm_folder_with_slash + row['pdb5'] + '.' + 'mtx' + '.' + str(_actual)
                if not os.path.isfile(pssm_ffile):
                    continue

                is_this_pssm_record_ok = True
                break

            #for some reason no mtx does not exist or it cannot be opened (locked file), so skip this PDB5 record altogether
            if is_this_pssm_record_ok == False:
                break

            with open(pssm_ffile) as pssm_fid:
                _line = pssm_fid.readline()
                _line = pssm_fid.readline()
                _line = pssm_fid.readline()

                for _ind in range(len(row['aa'])):
                    _line = pssm_fid.readline()
                    _split_line = _line.split()
                    if len(_split_line) != 44:
                        #number of items per line is not what is expected
                        is_this_pssm_record_ok = False
                        break

                    if UseFromPssmFile == 'score_sigmoid':
                        _pssm_arr = np.array(_split_line[2:2+20], 'float32')
                        _pssm_arr = 1. / (1. + np.exp(_pssm_arr))
                    elif UseFromPssmFile == 'score':
                        _pssm_arr = np.array(_split_line[2:2+20], 'float32')
                    elif UseFromPssmFile == 'weighted_percentage':
                        _pssm_arr = np.array(_split_line[2+20:2+40], 'float32')
                        _pssm_arr /= 100.
                    else:
                        raise Exception('predict: error: unsupported UseFromPssmFile')

                    if row['aa'][_ind] != _split_line[1]:
                        #aa mismatch in pssm
                        is_this_pssm_record_ok = False
                        break

                    _pssm_matrix[_ind, 0+20*(_mtx-1) : 20+20*(_mtx-1)] = _pssm_arr
                    #end of for _ind in range(len(row['aa'])):
                pssm_fid.close()
                #end of with open(pssm_ffile) as pssm_fid:

            if is_this_pssm_record_ok == False:
                break
            #end of for _mtx in MtxIntList:

        if is_this_pssm_record_ok == True:
            row['pssm'] = _pssm_matrix
        else:
            #ApplicationMode-specific
            print('\n-----> predict: error: (-) problems with psiblast profile %s for %s => skipping entry altogether\n' % (pssm_ffile, row['pdb5']))
            __return_value = 30
            continue
    #end of if mtxRoundCount > 0:

    #ApplicationMode-specific
    aaTotal = len(row['aa'])

    #to make sure 21 aa alphabet = 20 standard aa + 1 other X aminoacid
    _aa_array = np.array(row['aa'], 'c')
    _aa_is_other_array = ~np.in1d(_aa_array, [b'A', b'C', b'D', b'E', b'F', b'G', b'H', b'I', b'K', b'L', b'M', b'N', b'P', b'Q', b'R', b'S', b'T', b'V', b'W', b'Y'])
    if float(np.array('X','c').view(np.uint8)) in X_uniqueOrdered:
        _aa_array[_aa_is_other_array] = 'X'
    else:
        _aa_array[_aa_is_other_array] = '?'
    row['aa'] = _aa_array.tostring().decode("utf-8")

    X_whole = np.empty((aaTotal, AaWindow, 1),  'float32')
    if HmmMode == 'none':
        Z_whole = np.empty((aaTotal, AaWindow, 20*mtxRoundCount),  'float32')
    else:
        Z_whole = np.empty((aaTotal, AaWindow, 20*mtxRoundCount + 30),  'float32')
    halfWindow = int((AaWindow-1)/2)

    if required_input['HowToTreat_N_C_termini'] in ['none']:
        readFrameShift = halfWindow
    elif required_input['HowToTreat_N_C_termini'] in ['addQMtoEnds']:
        readFrameShift = 0
    else:
        raise Exception('predict: error: unsupported HowToTreat_N_C_termini')

    recnu = 0
    for j in range(readFrameShift, len(row['aa'])-readFrameShift):

        if j >= halfWindow and j+halfWindow+1 <= len(row['aa']):
            #normal
            _temp_aa = row['aa'][j-halfWindow:j+halfWindow+1]
        elif j < halfWindow and j+halfWindow+1 <= len(row['aa']):
            #left missing
            _temp_aa = row['aa'][0:j+halfWindow+1]
            _temp_aa = '?' * (halfWindow-j) + _temp_aa
        elif j+halfWindow+1 > len(row['aa']) and j >= halfWindow:
            #right missing
            _temp_aa = row['aa'][j-halfWindow:]
            _temp_aa = _temp_aa + '?' * (j+halfWindow+1 - len(row['aa']))
        elif j < halfWindow and j+halfWindow+1 > len(row['aa']):
            #both left and right are missing
            _temp_aa = row['aa'][0:]
            _temp_aa = '?' * (halfWindow-j) + _temp_aa + '?' * (j+halfWindow+1 - len(row['aa']))
        else:
            raise Exception('predict: error: unexpected situation')

        X_whole[recnu] = np.array(_temp_aa, 'c').reshape(AaWindow, 1).view(np.uint8)

        if mtxRoundCount > 0:
            if j >= halfWindow and j+halfWindow+1 <= len(row['aa']):
                _temp_pssm = row['pssm'][j-halfWindow:j+halfWindow+1, :]
            elif j < halfWindow and j+halfWindow+1 <= len(row['aa']):
                _temp_pssm = row['pssm'][0:j+halfWindow+1, :]
                _temp_pssm = np.concatenate((np.ones([halfWindow-j, 20*mtxRoundCount], 'float32')*-19,  _temp_pssm))
            elif j+halfWindow+1 > len(row['aa']) and j >= halfWindow:
                _temp_pssm = row['pssm'][j-halfWindow:, :]
                _temp_pssm = np.concatenate((_temp_pssm, np.ones([j+halfWindow+1 - len(row['aa']), 20*mtxRoundCount], 'float32')*-19))
            elif j < halfWindow and j+halfWindow+1 > len(row['aa']):
                _temp_pssm = row['pssm'][0:, :]
                _temp_pssm = np.concatenate((np.ones([halfWindow-j, 20*mtxRoundCount], 'float32')*-19, _temp_pssm, np.ones([j+halfWindow+1 - len(row['aa']), 20*mtxRoundCount], 'float32')*-19))
            Z_whole[recnu, :,  0:(20*mtxRoundCount)] = _temp_pssm


        if HmmMode != 'none':
            if j >= halfWindow and j+halfWindow+1 <= len(row['aa']):
                _temp_hmm = row['hmm'][j-halfWindow:j+halfWindow+1, :]
            elif j < halfWindow and j+halfWindow+1 <= len(row['aa']):
                _temp_hmm = row['hmm'][0:j+halfWindow+1, :]
                _temp = np.ones([halfWindow-j, 30], 'float32')*HMM_OUTSIDE_SEQ_DEFAULT_VALUE_1
                _temp[:, 27:30] = HMM_OUTSIDE_SEQ_DEFAULT_VALUE_2
                _temp_hmm = np.concatenate((_temp,  _temp_hmm))
            elif j+halfWindow+1 > len(row['aa']) and j >= halfWindow:
                _temp_hmm = row['hmm'][j-halfWindow:, :]
                _temp = np.ones([j+halfWindow+1 - len(row['aa']), 30], 'float32')*HMM_OUTSIDE_SEQ_DEFAULT_VALUE_1
                _temp[:, 27:30] = HMM_OUTSIDE_SEQ_DEFAULT_VALUE_2
                _temp_hmm = np.concatenate((_temp_hmm, _temp))
            elif j < halfWindow and j+halfWindow+1 > len(row['aa']):
                _temp_hmm = row['hmm'][0:, :]
                _temp1 = np.ones([halfWindow-j, 30], 'float32')*HMM_OUTSIDE_SEQ_DEFAULT_VALUE_1
                _temp1[:, 27:30] = HMM_OUTSIDE_SEQ_DEFAULT_VALUE_2
                _temp2 = np.ones([j+halfWindow+1 - len(row['aa']), 30], 'float32')*HMM_OUTSIDE_SEQ_DEFAULT_VALUE_1
                _temp2[:, 27:30] = HMM_OUTSIDE_SEQ_DEFAULT_VALUE_2
                _temp_hmm = np.concatenate((_temp1, _temp_hmm, _temp2))
            if HmmMode == 'hmm_conv_to_true_prob_and_diversity' or HmmMode == 'hmm_conv_to_true_prob_and_diver_div_16':
                _temp_hmm[:,0:27] = np.power(2.0, _temp_hmm[:,0:27] / -1000.0)
                _temp_hmm[:,27:30] = _temp_hmm[:,27:30] * 0.001
                if HmmMode == 'hmm_conv_to_true_prob_and_diver_div_16':
                    _temp_hmm[:,27:30] = _temp_hmm[:,27:30] / 16.0
                Z_whole[recnu, :,  (20*mtxRoundCount):] = _temp_hmm
            else:
                Z_whole[recnu, :,  (20*mtxRoundCount):] = _temp_hmm / HMM_NORMALIZATION_FACTOR

        recnu += 1
    #end of for j

    #print("*** recnu = %i ***" % recnu)
    X_whole = X_whole[range(recnu)]
    Z_whole = Z_whole[range(recnu)]

    #represent X not as a depth-1 float32 vector but depth-(20~21) float32 vector
    #converting
    if True:
        for i in range(0, len(X_uniqueOrdered)):
            X_whole[X_whole == X_uniqueOrdered[i]] = i
        # one hot encode outputs np_utils.to_categorical() does not work on a tensor of 3D and higher; it produces multiple one's
        X_whole_temp = X_whole.astype(np.uint8)
        new_shape = (X_whole_temp.shape[0], X_whole_temp.shape[1], len(X_uniqueOrdered))
        X_whole = np.zeros(shape=new_shape)
        (I1,I2) = np.unravel_index(np.arange(new_shape[0]*new_shape[1]), (new_shape[0], new_shape[1]))
        I3 = X_whole_temp.ravel()
        X_whole[I1, I2, I3] = 1.
        del X_whole_temp
        del I1
        del I2
        del I3

        old_shape = X_whole.shape
        if HmmMode == 'none':
            new_shape = (old_shape[0], old_shape[1], old_shape[2] + 20*mtxRoundCount)
        else:
            new_shape = (old_shape[0], old_shape[1], old_shape[2] + (20*mtxRoundCount) + 30)
        new_X_whole = np.zeros(shape=new_shape)
        new_X_whole[:, :, 0:old_shape[2]] = X_whole
        del X_whole
        if HmmMode == 'none':
            new_X_whole[:, :, old_shape[2]:old_shape[2]+20*mtxRoundCount] = Z_whole
        else:
            new_X_whole[:, :, old_shape[2]:old_shape[2]+(20*mtxRoundCount)+30] = Z_whole
        del Z_whole
        X_whole = new_X_whole
        del new_X_whole

    #ApplicationMode-specific
    X_probe =  X_whole
    print('predict: predicted secondary structure for %d models' % (nu_of_ensemble_models))
    array_of_pred_classes = np.empty([nu_of_ensemble_models, len(X_probe)], dtype='c')
    for _cv in range(0, nu_of_ensemble_models):
        pred_classes_probe = models[_cv].predict_classes(X_probe, verbose=VerboseLevel)
        array_of_pred_classes[_cv,:] = y_uniqueOrdered[pred_classes_probe].view('c')
        _pred_classes_print_as_string = array_of_pred_classes[_cv,:].tostring().decode("utf-8")
        print(_pred_classes_print_as_string)

    top_vote_pred_class = np.empty([len(X_probe), ], dtype='c')
    for _j in range(len(X_probe)):
        (_vals, _counts) = np.unique(array_of_pred_classes[:, _j], return_counts=True)
        top_vote_pred_class[_j] = _vals[np.argmax(_counts)]
    top_vote_pred_class_as_string = top_vote_pred_class.tostring().decode("utf-8")
    print('predict: major vote:')
    print(top_vote_pred_class_as_string)

    fidout = open(_output_ss_ffile, 'wt')
    fidout.write('#command:\t' + ' '.join(sys.argv[0:]) + '\n')
    fidout.write('#format_version:\t' + '1.0.2' + '\n')
    fidout.write('#ensemble of %d nnet models:\t%s\n' % (nu_of_ensemble_models, ModelsFPathNoSlash))
    fidout.write('#id:\t' + row['pdb5'] + '\n')
    fidout.write('#app:\t' + 'SecNet of version, ' + _AppVersion + '\n')
    fidout.write('#labels:\t' + _labels_message + '\n')
    fidout.write('#label_definition:\t' + _labels_definition_during_training + '\n')
    fidout.write('#recnu:\t%d\n' % recnu)
    fidout.write('#seq:\t' + row['aa'] + '\n')
    fidout.write('#ss:\t' + top_vote_pred_class_as_string + '\n')
    fidout.close()
    print('* predict: successful (+) prediction at %s' % _output_ss_ffile)

print('* predict: returned code is %d (0 = success, non-zero = failure)' % __return_value)
sys.exit(__return_value)

