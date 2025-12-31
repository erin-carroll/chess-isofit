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
fid = args.fid

# define file paths
base_dir =  '/store/carroll/col/data/2025/rccs/'
raw_dir = '/store/carroll/col/data/2025/rccs/subsets/'

version = '6c'
working_dir = os.path.join(base_dir, f'{fid}_{version}')

surface_path = '/store/carroll/col/data/surface_20240103_avirii_20250730.mat'
channelized_uncertainty_path = '/store/carroll/col/data/avirisng_systematic_error_neon.txt'

if os.path.exists(working_dir) is False:
    apply_oe(
        # file paths
        input_radiance = f'{raw_dir}/{fid}_rdn', # Radiance
        input_loc = f'{raw_dir}/{fid}_loc', # Location - IGM (lon, lat, elev)
        input_obs = f'{raw_dir}/{fid}_obs', # Observations
        working_directory = working_dir,
        surface_path = surface_path,
        skyview_factor = f'{raw_dir}/{fid}_sky_view',
        
        # instrument, rte specifications
        sensor = 'neon',
        emulator_base = '/store/brodrick/repos/sRTMnet/joint_dataset_training/wpoints_-1_long/combined_model_random.6c',
        channelized_uncertainty_path = channelized_uncertainty_path,
        inversion_windows = [[400.0, 1360.0], [1410, 1800.0], [1970, 2450.0]],
        
        # implementation
        n_cores = os.cpu_count(),
        ray_temp_dir = '/tmp/ray',
        # analytical_line=True,
        multiple_restarts=True,
        no_min_lut_spacing=True,
        pressure_elevation=True
    )