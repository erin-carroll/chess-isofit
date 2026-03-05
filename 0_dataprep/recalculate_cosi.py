import os
from glob import glob
import numpy as np
from spectral.io import envi
from scipy.ndimage import gaussian_filter
from isofit.utils import skyview
from tqdm import tqdm

os.chdir('/store/carroll/col/data')

nodata = -9999

fids_2018 = [x.split('/')[-1].removesuffix('_rdn_obs_ort.hdr') for x in glob('2018/raw/L1/*/*_obs_ort.hdr')]
fids_2025 = [x.split('/')[-1].removesuffix('_rdn.hdr') for x in glob('2025/raw/L1/radianceENVI/*_rdn.hdr')]
fids = fids_2018 + fids_2025

for fid in tqdm(fids):
    if '2018' in fid:
        fp_loc = glob(f'raw/L1/*/{fid}_rdn_ort_igm_ort.hdr')[0]
        fp_obs = glob(f'raw/L1/*/{fid}_rdn_obs_ort.hdr')[0]
        fp_out = fp_obs.replace('rdn_obs_ort', f'obs')
    if '2025' in fid:
        fp_out = fp_obs.replace('OBS_Data', f'obs')
        fp_loc = glob(f'raw/L1/radianceENVI/{fid}*_IGM_Data.hdr')[0]
        fp_obs = glob(f'raw/L1/radianceENVI/{fid}*_OBS_Data.hdr')[0]

    loc = envi.open(fp_loc).open_memmap()
    obs = envi.open(fp_obs).open_memmap().copy()
    na_mask = loc[...,2]==nodata

    # calculate cos i
    slope = np.radians(obs[...,6])
    aspect = np.radians(obs[...,7])
    solar_az = np.radians(obs[...,3])
    solar_zen = np.radians(obs[...,4])
    cos_i = (np.cos(solar_zen) * np.cos(slope) + np.sin(solar_zen) * np.sin(slope) * np.cos(solar_az - aspect))
    cos_i[cos_i<0.5] = 0.5 # clip negative and low values (threshold determined empirically)

    # put back into obs, reimpose na value
    cos_i[na_mask] = nodata
    obs[...,8] = cos_i

    # export
    meta = envi.open(fp_obs).metadata
    envi.create_image(fp_out, meta, ext='', force=True)
    dst = envi.open(fp_out)
    dst_mm = dst.open_memmap(writable=True)
    dst_mm[...] = obs
    dst_mm.flush()