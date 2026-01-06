#!/bin/bash
#SBATCH --job-name=copy_neon_2025_rdn
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH --output=/home/carroll/logs/%j_%x.out
#SBATCH --error=/home/carroll/logs/%j_%x.err

# add rclone installation to path
export PATH="/store/shared/rclone/bin:$PATH"

# copy 2025 radiance (.h5)
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_UPTA_1/L1/Spectrometer/RadianceH5/2025071213/NEON_D13_UPTA_DP1_L034-1_20250712_radiance.h5 /store/carroll/col/data/2025/raw/L1/radianceH5/2025_UPTA_1/ --progress