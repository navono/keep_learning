#!/bin/bash

set -e
set -x

BASEDIR=$(dirname "$0")
pushd "$BASEDIR"

eval "$(conda shell.bash hook)"
conda activate pdfDetection

export LD_LIBRARY_PATH=/home/super/anaconda3/envs/pdfDetection/lib/:$LD_LIBRARY_PATH
paddleocr --image_dir ./test_data/55601-29DD-186000IN-DW06-0001_v0_A0.jpg --use_angle_cls true --lang ch --use_gpu true
paddleocr --image_dir ./test_data/55601-29DD-186000IN-DW06-0001_v0_A0.jpg --lang ch --use_gpu true --type=structure
