import os
from glob import glob
import numpy as np
from spectral.io import envi

os.chdir('/store/carroll/col/data/2025/raw/L1/radianceENVI/')

base='NIS01'

fp_obs = glob('*_OBS_Data.hdr')

for fp in fp_obs:
    domain = fp.split('_')[3]
    day = fp.split('_')[1]
    line = fp.split('_')[5]

    fid_out = fp.split('/')[-1].split('_OBS')[0]

    fp_fids = glob(f'*{domain}*{line}*{day}_IGM*') # get all of the file paths with that fid

    for fp_old in fp_fids:
        fid_old = fp_old.split('_IGM')[0]
        fp_out = fp_old.replace(fid_old, fid_out)
        os.rename(fp_old, fp_out)
        print(fp_old, '->', fp_out)