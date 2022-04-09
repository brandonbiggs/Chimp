#!/bin/bash
#PBS -N $1
#PBS -l select=1:ncpus=1:mem=8gb
#PBS -l walltime=12:00:00
#PBS -j oe

module load conda
conda activate chimp
cd /home/biggbs/school/Chimp
python3 $2