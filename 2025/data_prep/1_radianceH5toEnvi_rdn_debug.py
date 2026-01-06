import sys
sys.path.append('/store/carroll/repos/chess-isofit/2025/')
from data_prep import radianceH5toEnvi
import os
from glob import glob

os.chdir('/store/carroll/col/data/2025/')
outDir = 'raw/L1/radianceENVI/'
h5_dir = 'raw/L1/radianceH5/'
# h5_files = glob(os.path.join(h5_dir, '*/*/*.h5'))
h5_files = ['raw/L1/radianceH5/2025_UPTA_1/2025071213/NEON_D13_UPTA_DP1_L034-1_20250712_radiance.h5']
h5File = h5_files[0]

filePathToEnviProjCs = '/store/shared/ENVI6/envi61/idl/resource/pedata/predefined/EnviPEProjcsStrings.txt'

rasterNames = ['Radiance']
rasterName = rasterNames[0]

outFile = os.path.join(outDir,os.path.basename(h5File).replace('radiance.h5','rdn'))
print(h5File)

# radianceH5toEnvi.convertH5RasterToEnvi(h5File, rasterName, outFile, filePathToEnviProjCs)
spatialIndexesToRead = None
bandIndexesToRead = None
raster, metadata = radianceH5toEnvi.h5refl2array(h5File, rasterName,spatialIndexesToRead = spatialIndexesToRead, bandIndexesToRead = bandIndexesToRead )
print(raster.shape)

print('success', outFile)
