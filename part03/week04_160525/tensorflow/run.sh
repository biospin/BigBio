#!/bin/bash
#PBS-q gpu
#PBS-V
#PBS-l select=1:ppn=4:gpus=1
hidden=512
cd $PBS_O_WORKDIR
python fully_connected_feed.py --max_steps 10000 --hidden1 $hidden --hidden2 $hidden --hidden3 $hidden --log_dir 'layer3hidden$hidden'
