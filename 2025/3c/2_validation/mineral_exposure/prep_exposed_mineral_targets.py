import os
import numpy as np
import pandas as pd
from spectral.io import envi
from spectral.io.envi import read_envi_header
from pyproj import Transformer
from glob import glob
import pickle
from pyproj import Transformer
import rasterio
from rasterio.transform import array_bounds

import sys
sys.path.append('/store/carroll/repos/chess-isofit/')
from utilities import *

os.chdir('/store/carroll/col/data/')

wl = np.loadtxt('wavelengths_neon.txt')[:,1]*1000 # nm

targets = pd.read_csv('min_exposure_sites_KG.csv')
site_names = list(targets['site'])
coords = list(zip(targets['utm_x'], targets['utm_y']))
for name, coord in zip(site_names, coords):
    print(name, coord)

# # 2025
# raw = '2025/raw/L1/radianceENVI/'
# out = '2025/validation/subsets/'

# # identify all flightlines that cover the targets
# buf = 500
# fids = glob(os.path.join(raw, '*IGM_Data'))
# target_flights = []
# for f in fids:
#     with rasterio.open(f) as src:
#         bounds = src.bounds  # (left, bottom, right, top)
#         left, bottom, right, top = bounds
#         for name, coord in zip(site_names, coords):
#             x = coord[0]; y = coord[1]
#             if (left <= x <= right) and (bottom <= y <= top):
#                 target_flights.append((f, name, x, y))
# print(len(target_flights))
# print(target_flights)

# # extract subset regions for rdn, obs, loc
# buf = 350
# for f, name, x, y in target_flights:
#     print(f, name)
#     try:
#         subset_region_2025(
#             fp_rdn = f.replace('IGM_Data', 'rdn.hdr'),
#             fp_obs = f.replace('IGM_Data', 'OBS_Data.hdr'),
#             fp_igm = f.replace('IGM_Data', 'IGM_Data.hdr'),
#             output_dir = out,
#             site_name = name,
#             x = x,
#             y = y,
#             buf = buf)
#     except:
#         print('     failed')

# 2018
raw = '2018/raw/L1/'
out = '2025/validation/subsets/'

# identify all flightlines that cover the targets
buf = 500
fids = glob(os.path.join(raw, '*', '*igm_ort'))
print('fids', fids)
target_flights = []
for f in fids:
    with rasterio.open(f) as src:
        bounds = src.bounds  # (left, bottom, right, top)
        left, bottom, right, top = bounds
        for name, coord in zip(site_names, coords):
            x = coord[0]; y = coord[1]
            if (left <= x <= right) and (bottom <= y <= top):
                target_flights.append((f, name, x, y))
print(len(target_flights))
print(target_flights)

# extract subset regions for rdn, obs, loc
buf = 350
for f, name, x, y in target_flights:
    print(f, name)
    try:
        subset_region_2018(
            fp_rdn = f.replace('rdn_ort_igm_ort', 'rdn_ort.hdr'),
            fp_obs = f.replace('rdn_ort_igm_ort', 'rdn_obs_ort.hdr'),
            fp_igm = f.replace('rdn_ort_igm_ort', 'rdn_ort_igm_ort.hdr'),
            output_dir = out,
            site_name = name,
            x = x,
            y = y,
            buf = buf)
    except:
        print('     failed')