#!/bin/bash
#SBATCH --job-name=copy_neon_2018_dtm
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=350G
#SBATCH --output=/home/carroll/logs/%j_%x.out
#SBATCH --error=/home/carroll/logs/%j_%x.err

# add rclone installation to path
export PATH="/store/shared/rclone/bin:$PATH"

rclone copy neon_gcs:neon-aa-aop-crestedbutte/2018/FullSite/D13/2018_CRBU_1/L3/DiscreteLidar/DTMGtif/ /store/carroll/col/data/2018/raw/L3/discreteLidar/DTM/ --progress

# start with one test file
# rclone copy neon_gcs:neon-aa-aop-crestedbutte/2018/FullSite/D13/2018_CRBU_1/L3/DiscreteLidar/DTMGtif/NEON_D13_CRBU_DP3_335000_4307000_DTM.tif /store/carroll/col/data/2018/raw/L3/discreteLidar/DTM/ --progress
# rclone copy neon_gcs:neon-aa-aop-crestedbutte/2018/FullSite/D13/2018_CRBU_1/L3/DiscreteLidar/DTMGtif/NEON_D13_CRBU_DP3_335000_4308000_DTM.tif /store/carroll/col/data/2018/raw/L3/discreteLidar/DTM/ --progress
# rclone copy neon_gcs:neon-aa-aop-crestedbutte/2018/FullSite/D13/2018_CRBU_1/L3/DiscreteLidar/DTMGtif/NEON_D13_CRBU_DP3_335000_4309000_DTM.tif /store/carroll/col/data/2018/raw/L3/discreteLidar/DTM/ --progress
# rclone copy neon_gcs:neon-aa-aop-crestedbutte/2018/FullSite/D13/2018_CRBU_1/L3/DiscreteLidar/DTMGtif/NEON_D13_CRBU_DP3_335000_4310000_DTM.tif /store/carroll/col/data/2018/raw/L3/discreteLidar/DTM/ --progress
# rclone copy neon_gcs:neon-aa-aop-crestedbutte/2018/FullSite/D13/2018_CRBU_1/L3/DiscreteLidar/DTMGtif/NEON_D13_CRBU_DP3_336000_4307000_DTM.tif /store/carroll/col/data/2018/raw/L3/discreteLidar/DTM/ --progress
# rclone copy neon_gcs:neon-aa-aop-crestedbutte/2018/FullSite/D13/2018_CRBU_1/L3/DiscreteLidar/DTMGtif/NEON_D13_CRBU_DP3_336000_4308000_DTM.tif /store/carroll/col/data/2018/raw/L3/discreteLidar/DTM/ --progress
# rclone copy neon_gcs:neon-aa-aop-crestedbutte/2018/FullSite/D13/2018_CRBU_1/L3/DiscreteLidar/DTMGtif/NEON_D13_CRBU_DP3_336000_4309000_DTM.tif /store/carroll/col/data/2018/raw/L3/discreteLidar/DTM/ --progress
# rclone copy neon_gcs:neon-aa-aop-crestedbutte/2018/FullSite/D13/2018_CRBU_1/L3/DiscreteLidar/DTMGtif/NEON_D13_CRBU_DP3_336000_4310000_DTM.tif /store/carroll/col/data/2018/raw/L3/discreteLidar/DTM/ --progress