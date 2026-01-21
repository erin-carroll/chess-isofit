#!/bin/bash
#SBATCH --job-name=copy_neon_2018_fid_boundaries
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=350G
#SBATCH --output=/home/carroll/logs/%j_%x.out
#SBATCH --error=/home/carroll/logs/%j_%x.err

# add rclone installation to path
export PATH="/store/shared/rclone/bin:$PATH"

rclone copy neon_gcs:neon-aa-aop-crestedbutte/2018/FullSite/D13/2018_CRBU_1/Metadata/Spectrometer/FlightlineBoundary/ /store/carroll/col/data/2018/raw/FlightlineBoundary/ --progress