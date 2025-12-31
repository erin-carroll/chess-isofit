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

os.chdir('/store/carroll/col/data/2025/')

fp_sky_view = 'sky_view/sky_view_factor'
fids = [x.split('/')[-1].removesuffix('_loc') for x in glob('rccs/subsets/*loc')]

for fid in fids:
    print(fid)
    # define filepaths
    fp_ref = f'2025/rccs/subsets/{fid}_loc'
    fp_out = f'2025/rccs/subsets/{fid}_sky_view'
    # resample
    clip_skyview_per_flightline(fp_sky_view, fp_ref, fp_out)

