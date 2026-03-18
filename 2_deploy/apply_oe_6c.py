import isofit
from isofit.utils.apply_oe import apply_oe 

import argparse
import os
import logging
from glob import glob

# Enable the ISOFIT logger
logging.getLogger().setLevel(logging.INFO)

# set up to submit flight id from batch script
parser = argparse.ArgumentParser()
parser.add_argument("--fid", required=True)
args = parser.parse_args()
fid = args.fid

os.chdir('/store/carroll/col/data')

version = 'deploy_6c_20260214'

# define file paths by year
if '2018' in fid:
    base_dir =  f'2018/{version}/'
    raw_dir = '2018/raw/L1/'
    rcc_path = '2018/rccs/rcc_white_tarp_mean_6c_processed.txt'
    input_radiance = glob(f'{raw_dir}/*/{fid}_rdn_ort')[0]
    input_loc = glob(f'{raw_dir}/*/{fid}_rdn_ort_igm_ort')[0]
    input_obs = glob(f'{raw_dir}/*/{fid}_obs')[0]
if '2025' in fid:
    base_dir =  f'2025/{version}/'
    raw_dir = '2025/raw/L1/radianceENVI/'
    rcc_path = '2025/rccs/rcc_snodgrass_mean_6c_processed.txt'
    input_radiance = f'{raw_dir}/{fid}_rdn'
    input_loc = f'{raw_dir}/{fid}_IGM_Data'
    input_obs = f'{raw_dir}/{fid}_obs'

working_dir = os.path.join(base_dir, f'{fid}')

surface_path = 'surface_20240103_avirii_20250730.mat'
channelized_uncertainty_path = 'avirisng_systematic_error_neon.txt'

if os.path.exists(working_dir) is False:
    apply_oe(
        # file paths
        input_radiance = input_radiance,
        input_loc = input_loc,
        input_obs = input_obs,
        working_directory = working_dir,
        surface_path = surface_path,
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