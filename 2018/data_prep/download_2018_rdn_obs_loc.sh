#!/bin/bash
#SBATCH --job-name=copy_neon_2018_rdn
#SBATCH --time=12:00:00
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH --output=/home/carroll/logs/%j_%x.out
#SBATCH --error=/home/carroll/logs/%j_%x.err

# add rclone installation to path
export PATH="/store/shared/rclone/bin:$PATH"

rclone sync neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/ /store/carroll/col/data/2018/raw/L1/ --progress