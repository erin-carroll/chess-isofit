import os
from isofit.utils.surface_model import surface_model
from spectral.io import envi
from spectral.io.envi import read_envi_header

surface_out = '/store/carroll/col/data/2018/surface_priors/'

# minimum adaptations to https://github.com/emit-sds/emit-sds-l2a/blob/develop/surface/surface_20240103_avirii.json
surface_model_path = os.path.join(surface_out, 'surface_20240103_avirii_20250730.json')
output_surface_file = os.path.join(surface_out, 'surface_20240103_avirii_20250730.mat')
surface_model(**{
    'config_path': surface_model_path,
    'output_path': output_surface_file,
    'wavelength_path': '/store/carroll/col/data/2018/raw/L1/2018061214/NIS01_20180612_154959_rdn_ort.hdr'
}
)