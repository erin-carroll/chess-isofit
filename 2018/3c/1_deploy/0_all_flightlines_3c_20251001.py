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

# set up parser so flight id submitted from batch script
parser = argparse.ArgumentParser()
parser.add_argument("--fid", required=True)
args = parser.parse_args()
flight_id = args.fid

# define file paths
base_dir =  '/store/carroll/col/data/2018/deploy_3c_20251001/'
raw_dir = '/store/carroll/col/data/2018/raw/L1/'

surface_path = '/store/carroll/col/data/2018/surface_priors/surface_20240103_avirii_20250730.mat'
lut_config_path = '/store/carroll/col/data/2018/extra_data/lut_config_20251001.json'
channelized_uncertainty_path = '/store/carroll/col/data/avirisng_systematic_error_neon.txt'
rcc_path = '/store/carroll/col/data/2018/rccs/1c/rcc_frankenstein_20250908.txt'

working_dir = os.path.join(base_dir, flight_id)

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
    multiple_restarts=True,
    no_min_lut_spacing=True
)