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

fp_mosaic = 'sky_view/bbox_srtm_mosaic'
fids = [x.split('/')[-1].removesuffix('_rdn_ort_igm_ort') for x in glob('raw/L1/*/*rdn_ort_igm_ort')]

for fid in fids:
    print(fid)
    # define filepaths
    fp_ref = glob(f'raw/L1/*/{fid}_rdn_ort_igm_ort')[0]
    fp_out = f'raw/L3/discreteLidar/DTM/{fid}_srtm'
    # resample
    clip_dtm_per_flightline(fp_mosaic, fp_ref, fp_out)