#!/usr/bin/env bash

#Version 1.0.3

input_fasta="undefined.fasta"

UNAME=$(uname)
if [ "$UNAME" == "Linux" ] ; then
	cpu_cores_num=`nproc`
elif [ "$UNAME" == "Darwin" ] ; then
	cpu_cores_num=`sysctl -n hw.ncpu`
elif [[ "$UNAME" == CYGWIN* || "$UNAME" == MINGW* ]] ; then
   echo "Windows is not supported yet"
   exit 1
fi
echo "* hhm: number of detected CPU cores is $cpu_cores_num"

#argument parsing
while getopts ":i:c:" opt;
do
	case $opt in
	#required argument
	i)
		fasta=$OPTARG
		;;
	#optional argument
	c)
		cpu_cores_num=$OPTARG
		;;
	esac
done
echo "* hhm: $cpu_cores_num CPU cores will be used"
echo "* hhm: input fasta is $fasta"


if [ ! -f "$fasta" ]
then
	echo "* hhm: sequence file $fasta does not exist"
	exit 1
fi

basename_fasta=`basename $fasta`
root_filename_fasta=${basename_fasta%.*}

SCRIPT="$(cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd)/$(basename $0)"
SCRIPTPATH=`dirname $SCRIPT`
APPPATH="$SCRIPTPATH"
#to go two levels up
APPPATH="$(dirname "$APPPATH")"
APPPATH="$(dirname "$APPPATH")"
TEMPPATH="$APPPATH/features/temp"
HMMFEATUREPATH="$APPPATH/features/hhm"

if [ -f "$HMMFEATUREPATH/$root_filename_fasta.hhm1" ]
then
        echo "* hhm: hhm features already exist -- skipping their regeneration"
	exit 0
fi

UNAME=$(uname)
if [ "$UNAME" == "Linux" ] ; then
   OS_DIR="unix"
elif [ "$UNAME" == "Darwin" ] ; then
   OS_DIR="macos"
elif [[ "$UNAME" == CYGWIN* || "$UNAME" == MINGW* ]] ; then
   OS_DIR="win"
   echo "* hhm: Windows OS is not supported yet"
   exit 1
fi


temp="$TEMPPATH/${root_filename_fasta}_$RANDOM"
mkdir -p $temp
cp $fasta $temp/$root_filename_fasta.seq
buildali="$APPPATH/3rd_software/$OS_DIR/hh/hh/buildali2.pl"
hhmake="$APPPATH/3rd_software/$OS_DIR/hh/hh/hhmake"

string_buildali="$buildali $temp/$root_filename_fasta.seq -cpu $cpu_cores_num -noss 1>$temp/${root_filename_fasta}_alignment.output 2>$temp/${root_filename_fasta}_alignment.error"
echo "* hhm: $string_buildali"
eval $string_buildali
return_value=$?
if [ $return_value -ne 0 ]
then
	echo "* hhm: buildali failed"
	exit 1
fi

string_hhmake="$hhmake -i $temp/$root_filename_fasta.a3m -o $HMMFEATUREPATH/$root_filename_fasta.hhm1 1>$temp/${root_filename_fasta}_hhmake.output 2>$temp/${root_filename_fasta}_hhmake.error"
echo "* hhm: $string_hhmake"
eval $string_hhmake
return_value=$?
if [ $return_value -ne 0 ]
then
	echo "* hhm: hhmake failed"
	exit 2
else
	rm -rf $temp
fi

echo "* hhm: success"

