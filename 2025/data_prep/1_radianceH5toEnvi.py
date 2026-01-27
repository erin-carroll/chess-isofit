import sys
sys.path.append('/store/carroll/repos/chess-isofit/2025/')
from data_prep import radianceH5toEnvi
import os
from glob import glob

os.chdir('/store/carroll/col/data/2025/')
outDir = 'raw/L1/radianceENVI/'
h5_dir = 'raw/L1/radianceH5/'
h5_files = glob(os.path.join(h5_dir, '*/*/*.h5'))

filePathToEnviProjCs = '/store/shared/ENVI6/envi61/idl/resource/pedata/predefined/EnviPEProjcsStrings.txt'

rasterNames = ['IGM_Data','OBS_Data','Radiance']

for h5_filename in h5_files:
    print(h5_filename)
    for rasterName in rasterNames:
        print(rasterName)
        outFile = os.path.join(outDir,os.path.basename(h5_filename).replace('radiance.h5',rasterName))
        try:
            radianceH5toEnvi.convertH5RasterToEnvi(h5_filename, rasterName, outFile, filePathToEnviProjCs)
        except Exception as e:
            print(f"FAILED for {outFile}")
            print(f"Error: {e}")