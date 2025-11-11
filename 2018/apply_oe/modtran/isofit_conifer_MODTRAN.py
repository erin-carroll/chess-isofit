import isofit
from isofit.utils.apply_oe import apply_oe 

import os
from spectral.io import envi
import numpy as np
import ray
import logging
import json

# Enable the ISOFIT logger
logging.getLogger().setLevel(logging.INFO)

# define file paths
home = '/store/carroll/col/2018/test_roi/'
subset_dir = home+'conifer/subset/'
flight_id = os.listdir(subset_dir)[1].split('_rdn')[0]
working_dir = home+f'conifer/{flight_id}_MODTRAN/'
data = '/home/carroll/isofit/extra-downloads/data/' # ancillary data (e.g. reflectance libraries used to construct the surface prior, and the available instrument models)
surface_model_path = os.path.join(home, 'surface.json')
output_surface_file = os.path.join(home, 'surface.mat')
lut_config_path = os.path.join(home, 'lut_config.json')
wavelength_path = os.path.join(subset_dir, f'{flight_id}_rdn.hdr')

# generate config files & LUT
apply_oe(
        # file paths
        input_radiance = os.path.join(subset_dir,f'{flight_id}_rdn'), # Radiance
        input_loc = os.path.join(subset_dir,f'{flight_id}_rdn_igm'), # Location - IGM (lon, lat, elev)
        input_obs = os.path.join(subset_dir,f'{flight_id}_rdn_obs'), # Observations
        working_directory = os.path.join(working_dir), # Output directory
        surface_path = output_surface_file, # Surface priors (.mat file)
        lut_config_file = lut_config_path, # Path to a look up table configuration file, which will override default choices
        # instrument, rte specifications
        sensor = 'neon', # right now this allows datetimes to be read in the right format but doesn't call any instrument models
        modtran_path = '/store/shared/MODTRAN6/MODTRAN6.0.0/', # path to modtran installation
        surface_category = "multicomponent_surface", # The type of ISOFIT surface priors to use. best practices: The multicomponent surface model is most universal and forgiving
        aerosol_climatology_path = None, # MODTRAN - ??
        atmosphere_type = "ATM_MIDLAT_SUMMER", # MODTRAN
        rdn_factors_path = None, # RCC update used 'on the fly'
        channelized_uncertainty_path = None, # Channelized uncertainty - if you have an instrument model. We don't have one for NEON yet that I know of
        model_discrepancy_path = None, # Model discrepancy term - handle things like unknown radiative transfer model effects
        inversion_windows = [[400.0, 1300.0], [1450, 1780.0], [2050.0, 2450.0]], # from best practices documentation
        # implementation
        n_cores = os.cpu_count()-4, # number of cores to run ISOFIT with. Substantial parallelism is available, and full runs will be very slow in serial. Suggested to max this out on the available system
        copy_input_files = False, # Flag to choose to copy input_radiance, input_loc, and input_obs locally into the working_directory
        presolve = False, # Attempts to solve for the right wv range (advisable only to use with small cubes or in concert with the empirical_line setting, or a significant speed penalty will be incurred)
        config_only = False, # Generates the configuration then exits before execution. If presolve is enabled, that run will still occur.
        ray_temp_dir = "/tmp/ray",
        pressure_elevation = False, # flag to retrieve elevation. Don't need to retrieve it because we have it?
        prebuilt_lut = None, # Use this pre-constructed look up table for all retrievals. Must be an ISOFIT-compatible RTE NetCDF
        analytical_line=False,
        empirical_line=False
    )