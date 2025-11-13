import subprocess
import os
from glob import glob

# define filepaths
today = '20251109'

home = '/store/carroll/col/data/2018/mosaic/'
obs_chunks = os.path.join(home, 'file_lists/obs_chunks.txt')

# generate mosiac glt for each obs chunk
# with open(obs_chunks, 'r') as f:
#     obs_chunks = f.readlines()
# for fp in obs_chunks:
#     all_obs_files = fp.strip()
#     idx = all_obs_files.split('_')[-1].removesuffix('.txt')
#     mosaic_glt_out = f'/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_glt_{idx}.tif'
#     cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py build-obs-nc {mosaic_glt_out} {all_obs_files} --x_resolution 1 --output_epsg 32613 --log_file /home/carroll/logs/mosaic_glt_{idx}_{today}.log --n_cores 64 --criteria_band 5 --criteria_mode min'
#     print(cmd_str)
#     subprocess.run(cmd_str, shell=True)

# stack chunked glt_mosaics into one
joint_glt_file_list = os.path.join(home, 'file_lists/joint_glt_file_list.txt')
joint_obs_file_list = os.path.join(home, 'file_lists/obs_chunks.txt')
output_glt_file = os.path.join(home, 'neon_2018_mosaic_glt.tif')
output_obs_file_list = os.path.join(home, 'file_lists/joint_obs_files.txt')
cmd_str = f'python /store/carroll/repos/SpectralUtil/spectral_util/mosaic.py stack-glts {joint_glt_file_list} {joint_obs_file_list} {output_glt_file} {output_obs_file_list}'
print(cmd_str)
subprocess.run(cmd_str, shell=True)
