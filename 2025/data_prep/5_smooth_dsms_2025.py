import os
from glob import glob
import numpy as np
from spectral.io import envi
from scipy.ndimage import gaussian_filter, distance_transform_edt
from isofit.utils import skyview

os.chdir('/store/carroll/col/data/2025')

nodata = -9999
fids = [x.split('/')[-1].removesuffix('_IGM_Data.hdr') for x in glob('raw/L1/radianceENVI/*_IGM_Data.hdr')]

# smooth loc dsm
for fid in fids:
    fp_loc = f'raw/L1/radianceENVI/{fid}_IGM_Data.hdr'
    loc = envi.open(fp_loc).open_memmap().copy()
    
    loc[loc==nodata] = np.nan
    na_mask = np.isnan(loc[...,2])

    # fill na px with nearest non-na value
    indices = distance_transform_edt(na_mask, return_distances=False, return_indices=True)
    dsm_smooth = loc[...,2][tuple(indices)]

    # gaussian filter
    dsm_smooth = gaussian_filter(dsm_smooth, sigma=7)

    # reimpose na mask
    dsm_smooth[na_mask] = nodata
    loc[...,2] = dsm_smooth
    
    # export
    fp_out = fp_loc.replace('IGM_Data', 'loc_smooth')
    meta = envi.open(fp_loc).metadata
    envi.create_image(fp_out, meta, ext='', force=True)
    dst = envi.open(fp_out)
    dst_mm = dst.open_memmap(writable=True)
    dst_mm[...] = loc
    dst_mm.flush()

# smooth slope, aspect, cos i
for fid in fids:
    fp_obs = f'raw/L1/radianceENVI/{fid}_OBS_Data.hdr'
    obs = envi.open(fp_obs).open_memmap().copy()
    dsm = envi.open(f'raw/L1/radianceENVI/{fid}_loc_smooth.hdr').open_memmap()[...,2].copy()
    
    obs[obs==nodata] = np.nan
    dsm[dsm==nodata] = np.nan
    na_mask = np.isnan(dsm)

    # calculate smoothed slope, aspect
    slope, aspect = skyview.gradient_d8(dsm, dx=1, dy=1, aspect_rad=True) # slope, aspect in rad

    # calculate cos i
    solar_az = np.radians(obs[...,3])
    solar_zen = np.radians(obs[...,4])
    cos_i = (np.cos(solar_zen) * np.cos(slope) + np.sin(solar_zen) * np.sin(slope) * np.cos(solar_az - aspect))

    # update obs, loc files
    obs[...,6] = np.degrees(slope)
    obs[...,7] = np.degrees(aspect)
    obs[...,8] = cos_i

    # export
    fp_out = fp_obs.replace('OBS_Data', 'obs_smooth')
    meta = envi.open(fp_obs).metadata
    envi.create_image(fp_out, meta, ext='', force=True)
    dst = envi.open(fp_out)
    dst_mm = dst.open_memmap(writable=True)
    dst_mm[...] = obs
    dst_mm.flush()