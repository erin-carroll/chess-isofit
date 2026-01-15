import sys
sys.path.append('/store/carroll/repos/chess-isofit/2025/')
from data_prep import radianceH5toEnvi
import os
from glob import glob

os.chdir('/store/carroll/col/data/2025/')
outDir = 'raw/L1/radianceENVI/'
h5_dir = 'raw/L1/radianceH5/'
h5_files = ['raw/L1/radianceH5/2025_UPTA_1/2025071213/NEON_D13_UPTA_DP1_L034-1_20250712_radiance.h5']

filePathToEnviProjCs = '/store/shared/ENVI6/envi61/idl/resource/pedata/predefined/EnviPEProjcsStrings.txt'

rasterNames = ['Radiance']
bands = [400,426]

for h5_filename in h5_files:
    print(h5_filename)
    for rasterName in rasterNames:
        outFile = os.path.join(outDir,os.path.basename(h5_filename).replace('radiance.h5',f'rdn_{bands[0]}'))
        print(outFile)
        print(bands)
        try:
            radianceH5toEnvi.convertH5RasterToEnvi(h5_filename, rasterName, outFile, filePathToEnviProjCs, bandIndexesToRead=bands)
            print('success', outFile)
        except:
            print('failed', outFile)