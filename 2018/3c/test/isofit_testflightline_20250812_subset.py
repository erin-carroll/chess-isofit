import isofit
from isofit.core.fileio import IO
from isofit.core.forward import ForwardModel
from isofit.inversion.inverse import Inversion
from isofit.inversion.inverse_simple import invert_algebraic, invert_simple
from isofit.configs import configs
from isofit.core.geometry import Geometry
from isofit.utils.apply_oe import apply_oe 

import os
from spectral.io import envi
import ray
import logging
import json
from glob import glob

# Enable the ISOFIT logger
logging.getLogger().setLevel(logging.INFO)

# define file paths
home = '/store/carroll/col/2018/'
raw_dir = home+'test_flightlines/subsets/'
version = '20250808'
flight_id = 'NIS01_20180612_155442'
extra_data = '/store/carroll/col/'
data = '/home/carroll/isofit/extra-downloads/data/' # ancillary data (e.g. reflectance libraries used to construct the surface prior, and the available instrument models)
surface_model_path = os.path.join(home, 'test_roi', 'surface_20240103_avirii_20250730.json')
output_surface_file = os.path.join(home, 'test_roi', 'surface_20240103_avirii_20250730.mat')
lut_config_path = os.path.join(home, 'test_roi', 'lut_config_20250810.json')

working_dir = os.path.join(home, 'test_flightlines', f'{flight_id}_sRTMnet_{version}_subset')
wavelength_path = os.path.join(raw_dir, f'{flight_id}_rdn.hdr')

fp_rcc = '/store/carroll/col/2018/test_roi/rcc_white_tarp_mean_20250807.txt'

fp_prebuilt_lut = '/store/carroll/col/2018/test_flightlines/NIS01_20180612_155442_sRTMnet_20250808/lut_full/lut.nc'

# run apply_oe to generate config, file structure, LUT
apply_oe(
        # file paths
        input_radiance = os.path.join(raw_dir, f'{flight_id}_rdn'), # Radiance
        input_loc = os.path.join(raw_dir, f'{flight_id}_loc'), # Location - IGM (lon, lat, elev)
        input_obs = os.path.join(raw_dir, f'{flight_id}_obs'), # Observations
        working_directory = os.path.join(working_dir), # Output directory
        surface_path = output_surface_file, # Surface priors (.mat file)
        lut_config_file = lut_config_path, # Path to a look up table configuration file, which will override default choices
        
        # instrument, rte specifications
        sensor = 'neon', # right now this 3allows datetimes to be read in the right format but doesn't call any instrument models
        modtran_path = None, # path to modtran installation
        emulator_base = '/home/carroll/isofit/extra-downloads/srtmnet/sRTMnet_v120.h5', # path to sRTMnet installation
        surface_category = "multicomponent_surface", # The type of ISOFIT surface priors to use. best practices: The multicomponent surface model is most universal and forgiving
        aerosol_climatology_path = None, # MODTRAN - ??
        atmosphere_type = "ATM_MIDLAT_SUMMER", # MODTRAN
        rdn_factors_path = fp_rcc, # RCC update used 'on the fly'
        channelized_uncertainty_path = extra_data + 'avirisng_systematic_error_neon.txt', # adapted avirisng model to neon wavelengths
        model_discrepancy_path = extra_data + 'avirisng_model_discrepancy_neon.mat', # Model discrepancy term - handle things like unknown radiative transfer model effects
        inversion_windows = [[400.0, 1300.0], [1450, 1780.0], [2050.0, 2450.0]], # from best practices documentation
        
        # implementation
        n_cores = os.cpu_count()-2, # number of cores to run ISOFIT with. Substantial parallelism is available, and full runs will be very slow in serial. Suggested to max this out on the available system (testing idea that leaving this as none will allow ray to set up all of the workers across multiple nodes?
        copy_input_files = True, # Flag to choose to copy input_radiance, input_loc, and input_obs locally into the working_directory
        presolve = False, # Attempts to solve for the right wv range (advisable only to use with small cubes or in concert with the empirical_line setting, or a significant speed penalty will be incurred)
        config_only = False, # Generates the configuration then exits before execution. If presolve is enabled, that run will still occur.
        ray_temp_dir = "/tmp/ray",
        pressure_elevation = False, # flag to retrieve elevation. Don't need to retrieve it because we have it at high resolution w DEM
        prebuilt_lut = fp_prebuilt_lut, # Use this pre-constructed look up table for all retrievals. Must be an ISOFIT-compatible RTE NetCDFs
        analytical_line=False,
        empirical_line=False,
        multiple_restarts=True
    )