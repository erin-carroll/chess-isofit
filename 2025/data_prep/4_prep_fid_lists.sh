#!/bin/bash
#SBATCH --job-name=prep_fid_lists
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH --output=/home/carroll/logs/%j_%x.out
#SBATCH --error=/home/carroll/logs/%j_%x.err

# set environmental variables
export MKL_NUM_THREADS=1
export OMP_NUM_THREADS=1

source /store/carroll/miniforge3/bin/activate isofit_env

python /store/carroll/repos/chess-isofit/2025/data_prep/3_prep_fid_lists.py