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
base_dir =  '/store/carroll/col/data/2018/deploy_6c_20251227/'
raw_dir = '/store/carroll/col/data/2018/raw/L1'
working_dir = os.path.join(base_dir, fid)

surface_path = '/store/carroll/col/data/surface_20240103_avirii_20250730.mat'
channelized_uncertainty_path = '/store/carroll/col/data/avirisng_systematic_error_neon.txt'
rcc_path = '/store/carroll/col/data/2018/rccs/rcc_frankenstein_20250908.txt'
skyview_path = f'/store/carroll/col/data/2018/sky_view/sky_view_fid/{fid}_sky_view'

if os.path.exists(working_dir) is False:
    apply_oe(
        # file paths
        input_radiance = glob(os.path.join(raw_dir, '*', f'{fid}_rdn_ort'))[0], # Radiance
        input_loc = glob(os.path.join(raw_dir, '*', f'{fid}_loc_smooth'))[0], # Location - IGM (lon, lat, elev)
        input_obs = glob(os.path.join(raw_dir, '*', f'{fid}_obs_smooth'))[0], # Observations
        working_directory = working_dir,
        rdn_factors_path = rcc_path,
        surface_path = surface_path,
        skyview_factor = skyview_path,
        
        # instrument, rte specifications
        sensor = 'neon',
        emulator_base = '/store/brodrick/repos/sRTMnet/joint_dataset_training/wpoints_-1_long/combined_model_random.6c',
        channelized_uncertainty_path = channelized_uncertainty_path,
        inversion_windows = [[400.0, 1360.0], [1410, 1800.0], [1970, 2450.0]],
        
        # implementation
        n_cores = os.cpu_count(),
        ray_temp_dir = '/tmp/ray',
        analytical_line=True,
        multiple_restarts=True,
        no_min_lut_spacing=True,
        pressure_elevation=True
    )