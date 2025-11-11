import sys
sys.path.append('/store/carroll/repos/neon-isofit/')
from h5_to_envi import radianceH5toEnvi
import os
from glob import glob

home = '/store/carroll/col/data/2025/'
domains = ['2025_ALMO_1', '2025_CRBU_2', '2025_UPTA_1']

filePathToEnviProjCs = '/store/shared/ENVI6/envi61/idl/resource/pedata/predefined/EnviPEProjcsStrings.txt'

rasterName = 'Reflectance'

for domain in domains:
    outDir = os.path.join(home, f'raw/L3/reflectanceENVI/{domain}/')
    os.makedirs(outDir, exist_ok=True)
    h5_dir = os.path.join(home, f'raw/L3/spectrometer/reflectance/{domain}/')
    h5_files = glob(os.path.join(h5_dir, '*.h5'))
    
    for h5_filename in h5_files:
        outFile = os.path.join(outDir,os.path.basename(h5_filename).removesuffix('.h5'))
        try:
            radianceH5toEnvi.convertH5RasterToEnvi(h5_filename, rasterName, outFile, filePathToEnviProjCs)
        except:
            print('failed', outFile)