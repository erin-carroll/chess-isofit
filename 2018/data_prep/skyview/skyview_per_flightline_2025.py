import os
os.environ["GDAL_PAM_ENABLED"] = 'NO'
import numpy as np
from glob import glob
from spectral.io import envi
import rasterio
from rasterio.warp import reproject, Resampling

import sys
sys.path.append('/store/carroll/repos/chess-isofit')
from utilities import *

os.chdir('/store/carroll/col/data/')

fp_sky_view = '2018/sky_view/sky_view_factor'
fids = [x.split('/')[-1].removesuffix('_loc_smooth') for x in glob('2025/raw/L1/radianceENVI/*_loc_smooth')]

for fid in fids:
    print(fid)
    # define filepaths
    fp_ref = f'2025/raw/L1/radianceENVI/{fid}_loc_smooth'
    fp_out = os.path.join('2025/sky_view', 'sky_view_fid', f'{fid}_sky_view')
    # resample
    clip_skyview_per_flightline(fp_sky_view, fp_ref, fp_out)

