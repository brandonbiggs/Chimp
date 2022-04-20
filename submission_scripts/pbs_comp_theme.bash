#!/bin/bash
#PBS -N comp-theme
#PBS -l select=1:ncpus=1:mem=8gb
#PBS -q router
#PBS -P edu_res
#PBS -l walltime=12:00:00
#PBS -j oe

echo $command
module load conda
conda activate chimp
cd /home/biggbs/school/Chimp
python3 $command