#!/bin/bash
#SBATCH --job-name=copy_neon_2025_rfl
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=0
#SBATCH --output=/home/carroll/logs/%j_%x.out
#SBATCH --error=/home/carroll/logs/%j_%x.err

# add rclone installation to path
export PATH="/store/shared/rclone/bin:$PATH"

# copy 2025 rfl for insitu val sites (.h5)
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062614/NEON_D13_CRBU_DP1_L014-1_20250626_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062614/NEON_D13_CRBU_DP1_L015-1_20250626_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062614/NEON_D13_CRBU_DP1_L031-1_20250626_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062614/NEON_D13_CRBU_DP1_L032-1_20250626_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062614/NEON_D13_CRBU_DP1_L033-1_20250626_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress

rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062714/NEON_D13_CRBU_DP1_L027-1_20250627_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062714/NEON_D13_CRBU_DP1_L028-1_20250627_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062714/NEON_D13_CRBU_DP1_L030-1_20250627_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress

rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062813/NEON_D13_CRBU_DP1_L016-1_20250628_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062813/NEON_D13_CRBU_DP1_L022-1_20250628_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062813/NEON_D13_CRBU_DP1_L023-1_20250628_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062813/NEON_D13_CRBU_DP1_L024-1_20250628_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062813/NEON_D13_CRBU_DP1_L025-1_20250628_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062813/NEON_D13_CRBU_DP1_L029-1_20250628_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062813/NEON_D13_CRBU_DP1_L034-1_20250628_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress

rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062913/NEON_D13_CRBU_DP1_L026-1_20250629_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062913/NEON_D13_CRBU_DP1_L046-1_20250629_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress
rclone copy neon_gcs:neon-aa-aop-crestedbutte/2025/FullSite/D13/2025_CRBU_2/L1/Spectrometer/DirectionalReflectanceH5/2025062913/NEON_D13_CRBU_DP1_L047-1_20250629_directional_reflectance.h5 /store/carroll/col/data/2025/raw/L1/directionalReflectanceH5/ --progress

