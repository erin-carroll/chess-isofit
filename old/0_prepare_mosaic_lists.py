import os
from glob import glob
import numpy as np

os.chdir('/store/carroll/col/data/2018/')

# get ordered fids from list manually prepared by PGB, KDC
with open('/store/brodrick/col/mosaics/file_lists/top_priority_isofit_refl.txt', 'r') as f:
    fids = f.readlines()
fids = [x.strip().split('/')[-1].removesuffix('_rfl') for x in fids]

# split fids into 10 sub lists
chunks = np.array_split(np.array(fids), 10)

# create an obs file for each sublist
for idx, chunk in enumerate(chunks):
    fp_out = f'/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_obs_{idx}.txt'
    obs_files = [f'/store/carroll/col/data/2018/raw/rmbl/*/{x}_rdn_obs_ort' for x in chunk]
    obs_files = [glob(x)[0] for x in obs_files]
    with open(fp_out, 'w') as f:
        f.writelines(f'{x}\n' for x in obs_files)

# make list of obs lists
fp_out = '/store/carroll/col/data/2018/mosaic/file_lists/obs_chunks.txt'
obs_lists = glob('/store/carroll/col/data/2018/mosaic/file_lists/top_*obs*.txt')
with open(fp_out, 'w') as f:
    f.writelines(f'{x}\n' for x in obs_lists)

# prepare joint_glt_file_list
# glt_files (list): List of GLT files to stack, in order.
fp_out = '/store/carroll/col/data/2018/mosaic/file_lists/joint_glt_file_list.txt'
glt_list = []
for idx in range(len(obs_lists)):
    fp = f'/store/carroll/col/data/2018/mosaic/neon_2018_mosaic_glt_{idx}.tif'
    glt_list.append(fp)
with open(fp_out, 'w') as f:
    f.writelines(f'{x}\n' for x in glt_list)

# prepare joint_obs_file_list
# obs_file_lists (list): List of observation file lists, matching order to glt_files
# we already have this, it's obs_chunks