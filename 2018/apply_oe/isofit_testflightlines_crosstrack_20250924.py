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
base_dir =  '/store/carroll/col/data/2018/test_flightlines/'
raw_dir = '/store/carroll/col/data/2018/raw/rmbl/'

surface_path = '/store/carroll/col/data/2018/test_roi/surface_20240103_avirii_20250730.mat'
lut_config_path = '/store/carroll/col/data/2018/test_roi/lut_config_20250810.json'
channelized_uncertainty_path = '/store/carroll/col/data/avirisng_systematic_error_neon.txt'
rcc_path = '/store/carroll/col/data/2018/test_rccs/rcc_frankenstein_20250908.txt'
version = '20250924'

# get unique flights
flight_ids = ['NIS01_20180613_170023',
              'NIS01_20180613_171044',
              'NIS01_20180613_172129',
              'NIS01_20180613_173216',
              'NIS01_20180613_174241']

# for each flightline subset,
for flight_id in flight_ids:
    working_dir = os.path.join(base_dir, f'{flight_id}_{version}')
    
    # run apply_oe to generate config, file structure, LUT
    apply_oe(
            # file paths
            input_radiance = glob(os.path.join(raw_dir, '*', f'{flight_id}_rdn_ort'))[0], # Radiance
            input_loc = glob(os.path.join(raw_dir, '*', f'{flight_id}_rdn_ort_igm_ort'))[0], # Location - IGM (lon, lat, elev)
            input_obs = glob(os.path.join(raw_dir, '*', f'{flight_id}_rdn_obs_ort'))[0], # Observations
            working_directory = working_dir,
            surface_path = surface_path,
            lut_config_file = lut_config_path,
            
            # instrument, rte specifications
            sensor = 'neon',
            emulator_base = '/home/carroll/extra-downloads/srtmnet/sRTMnet_v120.h5',
            rdn_factors_path = rcc_path,
            channelized_uncertainty_path = channelized_uncertainty_path,
            inversion_windows = [[400.0, 1360.0], [1410, 1800.0], [1970, 2450.0]],
            
            # implementation
            n_cores = os.cpu_count()-2,
            ray_temp_dir = '/tmp/ray',
            analytical_line=True,
            multiple_restarts=True
        )