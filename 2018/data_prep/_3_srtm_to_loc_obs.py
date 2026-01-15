import os
from glob import glob
import numpy as np
from spectral.io import envi
from scipy.ndimage import gaussian_filter
from isofit.utils import skyview
from tqdm import tqdm

os.chdir('/store/carroll/col/data/2018')

nodata = -9999

fids = ['NIS01_20180612_155442','NIS01_20180619_162542','NIS01_20180620_162340']

# insert srtm to loc
for fid in fids:
    print(fid)
    fp_dtm = f'raw/L3/discreteLidar/DTM/{fid}_srtm.hdr'
    fp_loc = glob(f'raw/L1/*/{fid}_rdn_ort_igm_ort.hdr')[0]
    fp_obs = glob(f'raw/L1/*/{fid}_rdn_obs_ort.hdr')[0]

    dtm = envi.open(fp_dtm).open_memmap()[...,0].copy()
    loc = envi.open(fp_loc).open_memmap().copy()

    dtm[dtm==nodata] = np.nan
    na_mask = loc[...,2]==nodata

    # clip output for loc, export
    dtm_na = dtm.copy()
    dtm_na[na_mask] = nodata
    dtm_na[np.isnan(dtm_na)] = nodata
    loc[...,2] = dtm_na

    fp_out = fp_loc.replace('rdn_ort_igm_ort', f'loc_smooth_srtm')
    meta = envi.open(fp_loc).metadata
    envi.create_image(fp_out, meta, ext='', force=True)
    dst = envi.open(fp_out)
    dst_mm = dst.open_memmap(writable=True)
    dst_mm[...] = loc
    dst_mm.flush() 

    # calculate slope, aspect on extended smooth dsm
    slope, aspect = skyview.gradient_d8(dtm, dx=1, dy=1, aspect_rad=True) # slope, aspect in rad
    slope[na_mask] = np.nan
    aspect[na_mask] = np.nan

    # calculate cos i
    obs = envi.open(fp_obs).open_memmap().copy()
    solar_az = np.radians(obs[...,3])
    solar_zen = np.radians(obs[...,4])
    cos_i = (np.cos(solar_zen) * np.cos(slope) + np.sin(solar_zen) * np.sin(slope) * np.cos(solar_az - aspect))
    
    # slope, aspect back to degrees
    slope = np.degrees(slope)
    aspect = np.degrees(aspect)

    # put back into obs, reimpose na value
    obs[...,6] = slope
    obs[...,7] = aspect
    obs[...,8] = cos_i
    obs[na_mask, 6:9] = nodata

    # export
    fp_out = fp_obs.replace('rdn_obs_ort', f'obs_smooth_srtm')
    meta = envi.open(fp_obs).metadata
    envi.create_image(fp_out, meta, ext='', force=True)
    dst = envi.open(fp_out)
    dst_mm = dst.open_memmap(writable=True)
    dst_mm[...] = obs
    dst_mm.flush()