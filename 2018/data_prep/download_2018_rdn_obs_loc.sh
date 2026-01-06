#!/bin/bash
#SBATCH --job-name=copy_neon_2018_rdn
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=350G
#SBATCH --output=/home/carroll/logs/%j_%x.out
#SBATCH --error=/home/carroll/logs/%j_%x.err

# add rclone installation to path
export PATH="/store/shared/rclone/bin:$PATH"

# rclone sync neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/ /store/carroll/col/data/2018/raw/L1/ --progress

# repair dumb deletes
rclone copy neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/2018061214/NIS01_20180612_154959_rdn_ort /store/carroll/col/data/2018/raw/L1/2018061214/ --progress
rclone copy neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/2018061214/NIS01_20180612_154959_rdn_ort.hdr /store/carroll/col/data/2018/raw/L1/2018061214/ --progress

rclone copy neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/2018061214/NIS01_20180612_155442_rdn_ort /store/carroll/col/data/2018/raw/L1/2018061214/ --progress
rclone copy neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/2018061214/NIS01_20180612_155442_rdn_ort.hdr /store/carroll/col/data/2018/raw/L1/2018061214/ --progress

rclone copy neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/2018061214/NIS01_20180612_155857_rdn_ort /store/carroll/col/data/2018/raw/L1/2018061214/ --progress
rclone copy neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/2018061214/NIS01_20180612_155857_rdn_ort.hdr /store/carroll/col/data/2018/raw/L1/2018061214/ --progress

rclone copy neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/2018061214/NIS01_20180612_160340_rdn_ort /store/carroll/col/data/2018/raw/L1/2018061214/ --progress
rclone copy neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/2018061214/NIS01_20180612_160340_rdn_ort.hdr /store/carroll/col/data/2018/raw/L1/2018061214/ --progress

rclone copy neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/2018061214/NIS01_20180612_160819_rdn_ort /store/carroll/col/data/2018/raw/L1/2018061214/ --progress
rclone copy neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/2018061214/NIS01_20180612_160819_rdn_ort.hdr /store/carroll/col/data/2018/raw/L1/2018061214/ --progress

rclone copy neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/2018061214/NIS01_20180612_161352_rdn_ort /store/carroll/col/data/2018/raw/L1/2018061214/ --progress
rclone copy neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/2018061214/NIS01_20180612_161352_rdn_ort.hdr /store/carroll/col/data/2018/raw/L1/2018061214/ --progress

rclone copy neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/2018061214/NIS01_20180612_161935_rdn_ort /store/carroll/col/data/2018/raw/L1/2018061214/ --progress
rclone copy neon_gcs:neon-dev-aop-private-share/JPL/2018_CRBU_1/L1/Spectrometer/Radiance/2018061214/NIS01_20180612_161935_rdn_ort.hdr /store/carroll/col/data/2018/raw/L1/2018061214/ --progress