#!/usr/bin/env bash

#This script tests SecNet protein sequences from the Test2018 data set from our paper.
#It saves the results to Test2018/output. You may compare your re-generated results with
#the expected ones stored in Test2018/expected. It is a normal situation when due to
#different hardware and software your predictions and expected predictions slightly vary
#by one or few labels. Your overall accurarcy will be close within 0.01-0.03% to the one
#reported in our paper.

COMMAND="../secnet.py3 --input ./input --output ./output --label 8 --quiet"
echo $COMMAND
eval $COMMAND

