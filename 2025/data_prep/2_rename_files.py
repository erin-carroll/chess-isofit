import os
from glob import glob
import numpy as np
from spectral.io import envi

home = '/store/carroll/col/data/2025/raw/L1/radianceENVI/'

base='NIS01'

fp_obs = glob(os.path.join(home, '*_OBS_Data.hdr'))

for fp in fp_obs:
    fid = fp.split('/')[-1].split('_OBS')[0]
    print(fid)
    fp_fids = glob(os.path.join(home, f'{fid}*')) # get all of the file paths with that fid

    ymd = fid.split('_')[5]
    site = '_'.join(fid.split('_')[2:5])

    obs = envi.open(fp).open_memmap()[...,9].copy() # get time from obs (utc decimal hours)
    obs[obs==-9999] = np.nan
    utc_dec = np.nanmean(obs)
    
    h = int(utc_dec) # convert to UTC HMS
    m = int((utc_dec - h) * 60)
    s = int((((utc_dec - h) * 60) - m) * 60)
    hms = f'{h:02d}{m:02d}{s:02d}'

    new_fid = '_'.join([base, ymd, hms, site])

    for fp_old in fp_fids:
        fp_out = fp_old.replace(fid, new_fid)
        os.rename(fp_old, fp_out)