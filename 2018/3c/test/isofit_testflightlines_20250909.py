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
raw_dir = '/store/carroll/col/data/2018/test_flightlines/subsets/'

surface_path = '/store/carroll/col/data/2018/test_roi/surface_20240103_avirii_20250730.mat'
lut_config_path = '/store/carroll/col/data/2018/test_roi/lut_config_20250922.json'
channelized_uncertainty_path = '/store/carroll/col/data/avirisng_systematic_error_neon.txt'
rcc_path = '/store/carroll/col/data/2018/test_rccs/rcc_frankenstein_20250908.txt'

version = '6c_20250923'
flight_id = 'NIS01_20180612_155442'
working_dir = os.path.join(base_dir, f'{flight_id}_{version}')

# for each flightline subset,
apply_oe(
    # file paths
    input_radiance = os.path.join(raw_dir, f'{flight_id}_rdn'), # Radiance
    input_loc = os.path.join(raw_dir, f'{flight_id}_loc'), # Location - IGM (lon, lat, elev)
    input_obs = os.path.join(raw_dir, f'{flight_id}_obs'), # Observations
    working_directory = working_dir,
    surface_path = surface_path,
    lut_config_file = lut_config_path,

    # instrument, rte specifications
    sensor = 'neon',
    emulator_base = '/home/carroll/srtmnet6c/joint_dataset_wpoints_26.npz',
    rdn_factors_path = rcc_path,
    channelized_uncertainty_path = channelized_uncertainty_path,
    inversion_windows = [[400.0, 1360.0], [1410, 1800.0], [1970, 2450.0]],
    
    # implementation
    n_cores = os.cpu_count()-2,
    ray_temp_dir = '/tmp/ray',
    analytical_line=True,
    multiple_restarts=True
)