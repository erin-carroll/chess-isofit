import os
os.environ["GDAL_PAM_ENABLED"] = 'NO'
import numpy as np
from glob import glob
from spectral.io import envi
import matplotlib.pyplot as plt
import rasterio
from rasterio.warp import reproject, Resampling
import sys
sys.path.append('/store/carroll/repos/neon-isofit')
from utilities import *

home = '/store/carroll/col/data/2018/'
fp_skyview = os.path.join(home, 'skyview', 'sky_view_factor_10m')
flights = [x.split('/')[-1].replace('_rdn_ort_igm_ort','') for x in glob(os.path.join(home, 'raw/rmbl', '*', '*rdn_ort_igm_ort'))]

for flight in flights:
    # define filepaths
    fp_ref = glob(os.path.join(home, 'raw/rmbl', '*', f'{flight}_rdn_ort_igm_ort'))[0]
    fp_out = os.path.join(home, 'skyview', 'skyview10_flightlines', f'skyview10_{flight}')
    # resample
    clip_skyview_per_flightline(fp_skyview, fp_ref, fp_out)

