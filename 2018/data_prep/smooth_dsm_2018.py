import os
from glob import glob
import numpy as np
from spectral.io import envi
from scipy.ndimage import gaussian_filter
from isofit.utils import skyview
from tqdm import tqdm

os.chdir('/store/carroll/col/data/2018')

nodata = -9999
sigma=9

fids = [x.split('/')[-1].removesuffix('_rdn_obs_ort.hdr') for x in glob('raw/L1/*/*_obs_ort.hdr')]
print(len(fids))

# smooth loc dsm
for fid in tqdm(fids):
    fp_loc = glob(f'raw/L1/*/{fid}_rdn_ort_igm_ort.hdr')[0]
    fp_obs = glob(f'raw/L1/*/{fid}_rdn_obs_ort.hdr')[0]

    loc = envi.open(fp_loc).open_memmap().copy()
    dsm_smooth = loc[...,2].copy()
    dsm_smooth[dsm_smooth==nodata] = np.nan
    na_mask = np.isnan(dsm_smooth)

    # gaussian smoothing ignoring na
    valid = np.isfinite(dsm_smooth)
    x_filled = np.where(valid, dsm_smooth, 0.0)
    smoothed = gaussian_filter(x_filled, sigma=sigma, mode='nearest')
    weights  = gaussian_filter(valid.astype(float), sigma=sigma, mode='nearest')
    dsm_smooth = smoothed / weights
    dsm_smooth[weights == 0] = np.nan

    # clip output for loc, export
    dsm_smooth_na = dsm_smooth.copy()
    dsm_smooth_na[na_mask] = nodata
    dsm_smooth_na[np.isnan(dsm_smooth_na)] = nodata
    loc[...,2] = dsm_smooth_na

    fp_out = fp_loc.replace('rdn_ort_igm_ort', 'loc_smooth')
    meta = envi.open(fp_loc).metadata
    envi.create_image(fp_out, meta, ext='', force=True)
    dst = envi.open(fp_out)
    dst_mm = dst.open_memmap(writable=True)
    dst_mm[...] = loc
    dst_mm.flush() 

    # calculate slope, aspect on extended smooth dsm
    slope, aspect = skyview.gradient_d8(dsm_smooth, dx=1, dy=1, aspect_rad=True) # slope, aspect in rad
    slope[na_mask] = np.nan
    aspect[na_mask] = np.nan

    # calculate cos i
    obs = envi.open(fp_obs).open_memmap().copy()
    solar_az = np.radians(obs[...,3])
    solar_zen = np.radians(obs[...,4])
    cos_i = (np.cos(solar_zen) * np.cos(slope) + np.sin(solar_zen) * np.sin(slope) * np.cos(solar_az - aspect))

    # put back into obs, reimpose na value
    obs[...,6] = slope
    obs[...,7] = aspect
    obs[...,8] = cos_i
    obs[na_mask, 6:9] = nodata

     # export
    fp_out = fp_obs.replace('rdn_obs_ort', 'obs_smooth')
    meta = envi.open(fp_obs).metadata
    envi.create_image(fp_out, meta, ext='', force=True)
    dst = envi.open(fp_out)
    dst_mm = dst.open_memmap(writable=True)
    dst_mm[...] = obs
    dst_mm.flush()