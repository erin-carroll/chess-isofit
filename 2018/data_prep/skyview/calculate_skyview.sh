#!/bin/bash
#SBATCH --job-name=skyview
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --cpus-per-task=64
#SBATCH --mem=0
#SBATCH --output=/home/carroll/logs/%j_%x.out
#SBATCH --error=/home/carroll/logs/%j_%x.err

# set environmental variables
export MKL_NUM_THREADS=1
export OMP_NUM_THREADS=1

source /store/carroll/miniforge3/bin/activate isofit_env

input=/store/carroll/col/data/2018/sky_view/bbox_srtm_mosaic
output_directory=/store/carroll/col/data/2018/sky_view/

isofit skyview $input $output_directory --n_cores=64 --resolution=30