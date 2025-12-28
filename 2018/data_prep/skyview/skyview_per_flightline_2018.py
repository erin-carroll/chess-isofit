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

os.chdir('/store/carroll/col/data/2018/')

fp_sky_view = 'sky_view/sky_view_factor'
fids = [x.split('/')[-1].removesuffix('_loc_smooth') for x in glob('raw/L1/*/*loc_smooth')]

for fid in fids:
    print(fid)
    # define filepaths
    fp_ref = glob(f'raw/L1/*/{fid}_loc_smooth')[0]
    fp_out = os.path.join('sky_view', 'sky_view_fid', f'{fid}_sky_view')
    # resample
    clip_skyview_per_flightline(fp_sky_view, fp_ref, fp_out)

