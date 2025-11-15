import sys
sys.path.append('/store/carroll/repos/chess-isofit/')
from h5_to_envi import radianceH5toEnvi
import os
from glob import glob

home = '/store/carroll/col/data/2025/'
outDir = os.path.join(home, 'raw/L1/radianceENVI/')
h5_dir = os.path.join(home, 'raw/L1/radianceH5/')
h5_files = glob(os.path.join(h5_dir, '*/*/*.h5'))

filePathToEnviProjCs = '/store/shared/ENVI6/envi61/idl/resource/pedata/predefined/EnviPEProjcsStrings.txt'

rasterNames = ['IGM_Data','OBS_Data','GLT_Data']

for h5_filename in h5_files:
    for rasterName in rasterNames:
        outFile = os.path.join(outDir,os.path.basename(h5_filename).replace('radiance.h5',rasterName))
        try:
            radianceH5toEnvi.convertH5RasterToEnvi(h5_filename, rasterName, outFile, filePathToEnviProjCs)
        except:
            print('failed', outFile)