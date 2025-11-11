# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import re
import h5py
import numpy as np
from osgeo import gdal
import time

filePathToEnviProjCs = '/store/shared/ENVI6/envi61/idl/resource/pedata/predefined/EnviPEProjcsStrings.txt'

def getRasterGdalDtype(inDtype):

#There is more...we just don't use them
    if inDtype == np.float32: 
        gdalDtype = gdal.GDT_Float32    
    elif inDtype ==  np.float64:
        gdalDtype = gdal.GDT_Float64
    elif inDtype == np.int8 or inDtype == np.uint8:
        gdalDtype = gdal.GDT_Byte
    elif inDtype == np.int16:
        gdalDtype = gdal.GDT_Int16
    elif inDtype == np.int32:
        gdalDtype = gdal.GDT_Int32
    elif inDtype == np.uint16:
        gdalDtype = gdal.GDT_UInt16
    elif inDtype == np.uint32:
        gdalDtype = gdal.GDT_UInt32
        
    return gdalDtype
    

def parseEnviProjCs(filePathToEnviProjCs,epsg):
    with open(filePathToEnviProjCs, 'r') as file:
        for line in file:
            # Use regular expression to find a number and the following string
            match = re.match(r'^\s*(\d+)\s+(.*)$', line)
            if match:
                number = int(match.group(1))
                if number == epsg:
                    return match.group(2).strip()

def writeEnviRaster(outEnviFile,raster,metadata,needsBandMetadata=False):

    if outEnviFile.endswith('.hdr'):
        outEnviFile = outEnviFile.replace('.hdr','')

    if len(raster.shape) == 2:
        raster = raster[:,:,None]
        numBands = 1
    else:
        numBands = raster.shape[2]

    driver = gdal.GetDriverByName("ENVI")
    outputDatasetEnvi = driver.Create(outEnviFile, int(metadata["width"]), int(metadata["height"]),
                          numBands, metadata["data_type"])

    outputDatasetEnvi.SetGeoTransform(metadata["geotransform"])
    outputDatasetEnvi.SetProjection(metadata["projection"])
    
    for band in range(0, numBands):
        outputBand = outputDatasetEnvi.GetRasterBand(band+1)
        outputBand.WriteArray(raster[:,:,band])
        outputBand.SetNoDataValue(metadata["data_ignore_value"])
        if "band_names" in metadata and not needsBandMetadata:
            outputBand.SetDescription(metadata["band_names"][band])
    bandMetadata={}
    if needsBandMetadata:
        
        bandMetadata = {'wavelength units': 'nanometers', 'wavelength': '{'+','.join(map(str, metadata['wavelengths']))+'}','fwhm': '{'+','.join(map(str, metadata['fwhm']))+'}'}
    
    if 'Classes' in metadata:
        bandMetadata['classes'] = metadata['Classes']
    if 'Class_Lookup' in metadata:
        bandMetadata['class lookup'] = '{'+','.join(map(str,metadata['Class_Lookup']))+'}'
    
    outputDatasetEnvi.SetMetadata(bandMetadata, 'ENVI')
    outputDatasetEnvi.FlushCache()
    outputDatasetEnvi = None

    
    if 'Class_Names' in metadata:
        decodedClassNames = [class_name.decode('utf-8') for class_name in metadata['Class_Names']]
    
        # Join the decoded strings into a single comma-delimited string
        decodedClassNamesString = '{'+', '.join(decodedClassNames)+'}'
    
        with open(os.path.splitext(outEnviFile)[0]+'.hdr', 'a') as file:
                file.write('class names = '+decodedClassNamesString)

def convertH5RasterToEnvi(h5File,rasterName,outEnviFile,filePathToEnviProjCs,spatialIndexesToRead = None,bandIndexesToRead = None):

    raster, metadata = h5refl2array(h5File, rasterName,spatialIndexesToRead = spatialIndexesToRead, bandIndexesToRead = bandIndexesToRead )
    
    writeRasterToEnvi(raster, rasterName, metadata,outEnviFile,filePathToEnviProjCs)

def writeRasterToEnvi(raster, rasterName,metadata,outEnviFile,filePathToEnviProjCs):

    if raster.ndim == 2:
        raster = raster[:,:,None]
        metadata['shape'] = raster.shape
        
    if isinstance(metadata["bandNames"],np.ndarray):
        metadata["bandNames"] = metadata["bandNames"].astype('U')[0]
    
    enviProjCs = parseEnviProjCs(filePathToEnviProjCs,metadata['EPSG'])
    
    if 'Sky_View_Factor' == rasterName or 'Cast_Shadow' == rasterName:
        raster = raster.astype(np.uint8)
    if 'Slope' == rasterName or 'Smooth_Surface_Elevation' == rasterName or 'Aspect' == rasterName:
        raster = raster.astype(np.float64)

    gdalDtype = getRasterGdalDtype(raster.dtype)
    
    enviMetadata = {
    "geotransform": (metadata['ext_dict']['xMin'], metadata['res']['pixelWidth'],-0.0,metadata['ext_dict']['yMax'],0.0,-1.0*metadata['res']['pixelHeight']),
    "projection": enviProjCs,
    "data_type": gdalDtype,
    "data_ignore_value": float(metadata['noDataVal']),
    "num_bands": int(metadata['shape'][2]),
    "width": int(metadata['shape'][1]),
    "height": int(metadata['shape'][0]),
    "band_names": metadata["bandNames"].split(','),
    "wavelengths": metadata["wavelengths"],
    "fwhm": metadata["fwhm"]
    # Add more metadata fields as needed
    }
    
    
    if 'Classes' in metadata:
        enviMetadata['Classes'] = metadata['Classes']
    if 'Class_Lookup' in metadata:
        enviMetadata['Class_Lookup'] = metadata['Class_Lookup']
    if 'Class_Names' in metadata:
        enviMetadata['Class_Names'] = metadata['Class_Names']
        

    needsBandMetadata = False
    if rasterName == 'Reflectance' or rasterName == 'Radiance':
        needsBandMetadata = True

    writeEnviRaster(outEnviFile,np.squeeze(raster),enviMetadata,needsBandMetadata=needsBandMetadata)

def h5refl2array(h5_filename, raster, onlyMetadata = False, spatialIndexesToRead = None, bandIndexesToRead = None):
    hdf5_file = h5py.File(h5_filename,'r')
    #print('h5refl2array')
    #Get the site name
    sitename = str(list(hdf5_file.items())).split("'")[1]
    productType = str(list(hdf5_file[sitename].items())).split("'")[1]

    if productType == 'Reflectance':
        productBaseLoc = hdf5_file[sitename]['Reflectance']
    elif productType == 'Radiance':
        productBaseLoc = hdf5_file[sitename]['Radiance']

    if raster == 'Reflectance':
        raster = 'Reflectance_Data'
        productLoc = productBaseLoc
    elif raster == 'Radiance':
        productLoc = productBaseLoc
    elif raster == 'to-sensor_Azimuth_Angle' or raster == 'to-sensor_Zenith_Angle':
        productLoc = productBaseLoc['Metadata']
    elif raster == 'GLT_Data' or raster == 'IGM_Data' or raster == 'OBS_Data':
        productLoc = productBaseLoc['Metadata']['Ancillary_Rasters']
    else:
        productLoc = productBaseLoc['Metadata']['Ancillary_Imagery']

    if 'DP3' in h5_filename and raster == 'to-sensor_Azimuth_Angle':
        raster = 'to-sensor_azimuth_angle'

    if 'DP3' in h5_filename and raster == 'to-sensor_Zenith_Angle':
        raster = 'to-sensor_zenith_angle'

    metadata = {}
    if raster == 'Radiance':
         rasterArray = productLoc['RadianceDecimalPart']
    else:
        rasterArray = productLoc[raster]
        
    if raster == 'Reflectance_Data':
        metadata['bandNames'] = 'Reflectance'
    elif raster == 'Radiance':
        metadata['bandNames'] = 'Radiance'
    elif raster == 'BDE':
        metadata['bandNames'] = 'BadDetectorElements'
    else:
        if 'Band_Names' in rasterArray.attrs:
            metadata['bandNames'] = rasterArray.attrs['Band_Names']
    
    
    if 'Scale_Factor' in rasterArray.attrs:
        metadata['scaleFactor'] = float(rasterArray.attrs['Scale_Factor'])
    elif 'Scale' in rasterArray.attrs:
        metadata['scaleFactor'] = float(rasterArray.attrs['Scale'])
    else:
        metadata['scaleFactor'] = 1.0

    rasterShape = rasterArray.shape
    metadata['wavelengths'] = productBaseLoc['Metadata']['Spectral_Data']['Wavelength'][:]
    metadata['fwhm'] = productBaseLoc['Metadata']['Spectral_Data']['FWHM'][:]
    
    #Create dictionary containing relevant metadata information    #Create dictionary containing relevant metadata information
    
    metadata['shape'] = rasterShape
    metadata['mapInfo'] = productBaseLoc['Metadata']['Coordinate_System']['Map_Info'][()]
    #Extract no data value & set no data value to NaN\n",

    
    if raster == 'Reflectance_Data':

        metadata['bad_band_window1'] = (productLoc.attrs['Band_Window_1_Nanometers'])
        metadata['bad_band_window2'] = (productLoc.attrs['Band_Window_2_Nanometers'])

    metadata['projection'] = productBaseLoc['Metadata']['Coordinate_System']['Proj4'][()]
    metadata['EPSG'] = int(productBaseLoc['Metadata']['Coordinate_System']['EPSG Code'][()])
    mapInfo = productBaseLoc['Metadata']['Coordinate_System']['Map_Info'][()]
    mapInfo_string = str(mapInfo); #print('Map Info:',mapInfo_string)\n",
    mapInfo_split = mapInfo_string.split(",")
    #Extract the resolution & convert to floating decimal number
    metadata['res'] = {}
    metadata['res']['pixelWidth'] = float(mapInfo_split[5])
    metadata['res']['pixelHeight'] = float(mapInfo_split[6])
    #Extract the upper left-hand corner coordinates from mapInfo\n",
    xMin = float(mapInfo_split[3]) #convert from string to floating point number\n",
    yMax = float(mapInfo_split[4])
    #Calculate the xMax and yMin values from the dimensions\n",
    xMax = xMin + (rasterShape[1]*float(metadata['res']['pixelWidth'])) #xMax = left edge + (# of columns * resolution)\n",
    yMin = yMax - (rasterShape[0]*float(metadata['res']['pixelHeight'])) #yMin = top edge - (# of rows * resolution)\n",
    metadata['extent'] = (xMin,xMax,yMin,yMax)
    metadata['ext_dict'] = {}
    metadata['ext_dict']['xMin'] = xMin
    metadata['ext_dict']['xMax'] = xMax
    metadata['ext_dict']['yMin'] = yMin
    metadata['ext_dict']['yMax'] = yMax

    if 'Classes' in rasterArray.attrs:
        metadata['Classes'] = float(rasterArray.attrs['Classes'])
    if 'Class_Lookup' in rasterArray.attrs:
        metadata['Class_Lookup'] = rasterArray.attrs['Class_Lookup'].astype(np.float32)
    if 'Class_Names' in rasterArray.attrs:
        metadata['Class_Names'] = rasterArray.attrs['Class_Names']
    if spatialIndexesToRead is None or spatialIndexesToRead == 'all':
        
        indexesRow = (int(0),int(rasterShape[0]))
        indexesCol = (int(0),int(rasterShape[1]))
        spatialIndexesToRead = [indexesRow,indexesCol]
    
    if 'Data_Ignore_Value' in rasterArray.attrs:
        metadata['noDataVal'] = float(rasterArray.attrs['Data_Ignore_Value'])                                               
    if onlyMetadata:
        hdf5_file.close()
        rasterArray = []
    elif raster == 'Radiance' or raster == 'Reflectance_Data':  
        
        if bandIndexesToRead is None:
            bandIndexesToRead = (int(0),int(rasterShape[2]))
            
        if raster == 'Reflectance_Data':
            rasterArray = rasterArray[spatialIndexesToRead[0][0]:spatialIndexesToRead[0][1],spatialIndexesToRead[1][0]:spatialIndexesToRead[1][1],bandIndexesToRead[0]:bandIndexesToRead[1]]
        elif raster == 'Radiance': 
        
            rasterArray = productLoc['RadianceIntegerPart'][spatialIndexesToRead[0][0]:spatialIndexesToRead[0][1],spatialIndexesToRead[1][0]:spatialIndexesToRead[1][1],bandIndexesToRead[0]:bandIndexesToRead[1]] + productLoc['RadianceDecimalPart'][spatialIndexesToRead[0][0]:spatialIndexesToRead[0][1],spatialIndexesToRead[1][0]:spatialIndexesToRead[1][1],bandIndexesToRead[0]:bandIndexesToRead[1]]/metadata['scaleFactor']
            rasterArray[rasterArray==productLoc['RadianceIntegerPart'].attrs['Data_Ignore_Value']+productLoc['RadianceDecimalPart'].attrs['Data_Ignore_Value']/metadata['scaleFactor']]=-9999
            metadata['noDataVal'] = -9999
    else:
        
        rasterArray = rasterArray[spatialIndexesToRead[0][0]:spatialIndexesToRead[0][1],spatialIndexesToRead[1][0]:spatialIndexesToRead[1][1]] 
        if 'noDataVal' not in metadata.keys():

            if rasterArray.dtype == np.uint8:
                metadata['noDataVal'] = 0
            else:
                metadata['noDataVal'] = -9999
        
        hdf5_file.close()

    return rasterArray, metadata


# outDir = os.path.join(r'D:\RadianceH5Out')

# h5_dir = os.path.join(r'D:\RadianceH5\2025053113')

# h5_files = [os.path.join(h5_dir,file) for file in os.listdir(h5_dir) if file.endswith('.h5')]

# rasterNames = ['Radiance','IGM_Data','OBS_Data','GLT_Data']

# for h5_filename in h5_files:
    
    # for rasterName in rasterNames:
    #     print('Working on: '+rasterName + ' for '+os.path.basename(h5_filename))
    #     t1 = time.time()
    #     outFile = os.path.join(outDir,os.path.basename(h5_filename).replace('radiance.h5',rasterName))
    
    #     #if outputFormat == 'gtif':
    #         #outFile = outFile+'.tif'
    #         #convertH5RasterToGtif(h5_filename,rasterName,outFile)
    #     outFile = outFile+'.bsq'
    #     convertH5RasterToEnvi(h5_filename,rasterName,outFile,filePathToEnviProjCs)
