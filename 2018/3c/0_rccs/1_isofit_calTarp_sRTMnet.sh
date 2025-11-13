#!/bin/bash
#SBATCH --job-name=isofit_calTarp_sRTMnet_20250806
#SBATCH --time=10:00:00
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=60
#SBATCH --mem=100000
#SBATCH --mail-type=ALL
#SBATCH --mail-user=erin_carroll@berkeley.edu
#ssh carroll

# set environmental variables
export MKL_NUM_THREADS=1
export OMP_NUM_THREADS=1

source /store/carroll/miniforge3/bin/activate isofit_env

python /store/carroll/repos/chess-isofit/2018/3c/0_rccs/1_isofit_calTarp_sRTMnet_20250806.py
