import os
from glob import glob
import numpy as np
from spectral.io import envi
from scipy.ndimage import gaussian_filter
from isofit.utils import skyview
from tqdm import tqdm

os.chdir('/store/carroll/col/data/2018')

nodata = -9999

fids = [x.split('/')[-1].removesuffix('_rdn_obs_ort.hdr') for x in glob('raw/L1/*/*_obs_ort.hdr')]
print(len(fids))

# insert dtm to loc
for fid in tqdm(fids):
    fp_dtm = f'raw/L3/discreteLidar/DTM/{fid}_dtm.hdr'
    fp_loc = glob(f'raw/L1/*/{fid}_rdn_ort_igm_ort.hdr')[0]
    fp_obs = glob(f'raw/L1/*/{fid}_rdn_obs_ort.hdr')[0]

    dtm = envi.open(fp_dtm).open_memmap()[...,0].copy()
    loc = envi.open(fp_loc).open_memmap().copy()
    obs = envi.open(fp_obs).open_memmap().copy()
    na_mask = loc[...,2]==nodata

    # calculate slope, aspect on extended smooth dsm
    slope, aspect = skyview.gradient_d8(dtm, dx=1, dy=1, aspect_rad=True) # slope, aspect in rad

    # calculate cos i
    solar_az = np.radians(obs[...,3])
    solar_zen = np.radians(obs[...,4])
    cos_i = (np.cos(solar_zen) * np.cos(slope) + np.sin(solar_zen) * np.sin(slope) * np.cos(solar_az - aspect))
    
    # slope, aspect back to degrees
    slope = np.degrees(slope)
    aspect = np.degrees(aspect)

    # reimpose na mask
    dtm[na_mask] = nodata
    dtm[np.isnan(dtm)] = nodata
    slope[na_mask] = nodata
    aspect[na_mask] = nodata
    cos_i[na_mask] = nodata

    # put back into loc, export
    loc[...,2] = dtm
    fp_out = fp_loc.replace('rdn_ort_igm_ort', 'loc_dtm')
    meta = envi.open(fp_loc).metadata
    envi.create_image(fp_out, meta, ext='', force=True)
    dst = envi.open(fp_out)
    dst_mm = dst.open_memmap(writable=True)
    dst_mm[...] = loc
    dst_mm.flush() 

    # put back into obs, export
    obs[...,6] = slope
    obs[...,7] = aspect
    obs[...,8] = cos_i
    obs[np.isnan(obs)] = nodata
    fp_out = fp_obs.replace('rdn_obs_ort', 'obs_dtm')
    meta = envi.open(fp_obs).metadata
    envi.create_image(fp_out, meta, ext='', force=True)
    dst = envi.open(fp_out)
    dst_mm = dst.open_memmap(writable=True)
    dst_mm[...] = obs
    dst_mm.flush()