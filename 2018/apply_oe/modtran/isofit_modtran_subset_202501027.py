import isofit
from isofit.utils.apply_oe import apply_oe 

import argparse
import os
from spectral.io import envi
import numpy as np
import ray
import logging
import json
from glob import glob

# Enable the ISOFIT logger
logging.getLogger().setLevel(logging.INFO)

# define file paths
base_dir =  '/store/carroll/col/data/2018/test_6c/'
raw_dir = '/store/carroll/col/data/2018/test_6c/subsets/'

surface_path = '/store/carroll/col/data/2018/surface_priors/surface_20240103_avirii_20250730.mat'
lut_config_path = '/store/carroll/col/data/2018/extra_data/lut_config_20251001.json'
channelized_uncertainty_path = '/store/carroll/col/data/avirisng_systematic_error_neon.txt'

version = '20251027_modtran'
flight_id = 'NIS01_20180612_155442'
rs = ['336000_4307000', '336000_4310000']

# dtm
for r in rs:
    working_dir = os.path.join(base_dir, f'{flight_id}_{version}_{r}')
    apply_oe(
        # file paths
        input_radiance = os.path.join(raw_dir, f'{flight_id}_rdn_ort_{r}'), # Radiance
        input_loc = os.path.join(raw_dir, 'dtm', f'loc_{r}.img'), # Location - IGM (lon, lat, elev)
        input_obs = os.path.join(raw_dir, 'dtm', f'obs_{r}.img'), # Observations
        skyview_factor = os.path.join(raw_dir, f'NIS01_20180612_155442_skyview_{r}'),
        working_directory = working_dir,
        surface_path = surface_path,
        lut_config_file = lut_config_path,
    
        # instrument, rte specifications
        sensor = 'neon',
        channelized_uncertainty_path = channelized_uncertainty_path,
        modtran_path = '/store/shared/MODTRAN6/MODTRAN6.0.0/', # path to modtran installation
        inversion_windows = [[400.0, 1360.0], [1410, 1800.0], [1970, 2450.0]],
        
        # implementation
        n_cores = os.cpu_count()-2,
        copy_input_files = True,
        ray_temp_dir = '/tmp/ray',
        multiple_restarts=True,
        analytical_line=True
    )
