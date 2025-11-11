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
base_dir =  '/store/carroll/col/data/2018/test_rccs/'
subset_dir = os.path.join(base_dir, 'subsets')

surface_path = '/store/carroll/col/data/2018/test_roi/surface_20240103_avirii_20250730.mat'
lut_config_path = '/store/carroll/col/data/2018/test_roi/lut_config_20250810.json'
channelized_uncertainty_path = '/store/carroll/col/data/avirisng_systematic_error_neon.txt'
rcc_path = '/store/carroll/col/data/2018/test_roi/rcc_white_tarp_mean_20250807.txt'

# get unique flights
flight_ids = os.listdir(subset_dir)
flight_ids = set(['_'.join(x.split('_')[:3]) for x in flight_ids if x.startswith('.')==False])

# for each flightline subset,
for flight_id in flight_ids:
    working_dir = os.path.join(base_dir, flight_id)
    
    # run apply_oe to generate config, file structure, LUT
    apply_oe(
            # file paths
            input_radiance = os.path.join(subset_dir, f'{flight_id}_rdn'),
            input_loc = os.path.join(subset_dir, f'{flight_id}_igm'),
            input_obs = os.path.join(subset_dir, f'{flight_id}_obs'),
            working_directory = working_dir,
            surface_path = surface_path,
            lut_config_file = lut_config_path,
            
            # instrument, rte specifications
            sensor = 'neon',
            emulator_base = '/home/carroll/isofit/extra-downloads/srtmnet/sRTMnet_v120.h5',
            rdn_factors_path = rcc_path,
            channelized_uncertainty_path = channelized_uncertainty_path,
            inversion_windows = [[400.0, 1360.0], [1410, 1800.0], [1970, 2450.0]],
            
            # implementation
            n_cores = os.cpu_count()-2,
            ray_temp_dir = '/tmp/ray',
            analytical_line=False,
            multiple_restarts=True
        )