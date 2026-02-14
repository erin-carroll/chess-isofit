import isofit
from isofit.utils.apply_oe import apply_oe 

import argparse
import os
import logging
from glob import glob

# Enable the ISOFIT logger
logging.getLogger().setLevel(logging.INFO)

# set up parser so flight id submitted from batch script
parser = argparse.ArgumentParser()
parser.add_argument("--fid", required=True)
args = parser.parse_args()
fid = args.fid

os.chdir('/store/carroll/col/data')

# define file paths
base_dir =  '2018/deploy_6c_20260214/'
raw_dir = '2018/raw/L1/'

working_dir = os.path.join(base_dir, f'{fid}')

surface_path = 'surface_20240103_avirii_20260211.mat'
channelized_uncertainty_path = 'avirisng_systematic_error_neon.txt'
rcc_path = '2018/rccs/rcc_white_tarp_mean_6c_processed.txt'

if os.path.exists(working_dir) is False:
    apply_oe(
        # file paths
        input_radiance = glob(f'{raw_dir}/*/{fid}_rdn_ort')[0], # Radiance
        input_loc = glob(f'{raw_dir}/*/{fid}_rdn_ort_igm_ort')[0], # Location - IGM (lon, lat, elev)
        input_obs = glob(f'{raw_dir}/*/{fid}_obs')[0], # Observations
        working_directory = working_dir,
        surface_path = surface_path,
        # skyview_factor = f'2018/sky_view/sky_view_fid/{fid}_sky_view', # still not working
        rdn_factors_path = rcc_path,
        
        # instrument, rte specifications
        sensor = 'neon',
        emulator_base = '/store/brodrick/repos/sRTMnet/joint_dataset_training/wpoints_-1_long/combined_model_random.6c',
        channelized_uncertainty_path = channelized_uncertainty_path,
        inversion_windows = [[400.0, 1360.0], [1410, 1800.0], [1970, 2450.0]],
        
        # implementation
        n_cores = 64,
        analytical_line=True,
        no_min_lut_spacing=True,
        pressure_elevation=True,
        presolve=True,
    )