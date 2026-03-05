import os
import numpy as np
from spectral.io.envi import read_envi_header
from scipy.interpolate import interp1d

extra_data = '/home/carroll/isofit/extra-downloads/data/'

# channelized uncertainty - ang to neon wavelengths
systematic_error = np.loadtxt(os.path.join(extra_data, 'avirisng_systematic_error.txt'))
wvl = systematic_error[...,0]
error = systematic_error[...,1]
wvl_neon = [float(x) for x in read_envi_header('/store/carroll/col/data/2018/raw/L1/2018061914/NIS01_20180619_153052_rdn.hdr')['wavelength']]

interp_ = interp1d(wvl, error, kind='linear', fill_value='extrapolate')
error_new = interp_(wvl_neon)

systematic_error_neon = np.column_stack([wvl_neon, error_new])
header = '# Wavelength, 1-sigma systematic calibration / radiative transfer errors'
np.savetxt('/store/carroll/col/data/avirisng_systematic_error_neon.txt', systematic_error_neon, fmt='%.7f', header=header, comments='')