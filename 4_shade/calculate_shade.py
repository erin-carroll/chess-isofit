# adapted from https://github.com/emit-sds/emit-sds-masks/blob/develop/cloud_shade.py and https://github.com/pgbrodrick/shade-ray-trace/blob/master/calculate_shade.py

import numpy as np
from osgeo import gdal
import bresenham_line
from tqdm import tqdm
import argparse
from glob import glob
import os
import sys

# set up parser so flight id submitted from batch script
parser = argparse.ArgumentParser()
parser.add_argument("--fid", required=True)
parser.add_argument("--solar_azimuth_band", type=int, required=True)
parser.add_argument("--solar_zenith_band", type=int, required=True)
parser.add_argument("--output_folder", required=True)
args = parser.parse_args()
fid = args.fid
solar_azimuth_band = args.solar_azimuth_band
solar_zenith_band = args.solar_zenith_band
output_folder = args.output_folder

def cwn_to_math(angle_cw_from_north):
    return (90 - angle_cw_from_north) % 360

def edge_coords_from_target(target_px_x: np.array, target_px_y: np.array, angle: np.array, bounds):
    """ Get the coordinates of the edge pixel in the direction of the given angle from a target pixel.

    Args:
        target_px_x (array, int): array of x-coordinate of the target pixel.
        target_px_y (array, int): array of y-coordinate of the target pixel.
        angle (array, float): angle in degrees, clockwise from North.
        bounds (tuple): bounds of the image in the format (min_x, min_y, max_x, max_y).
    """
    min_x, min_y, max_x, max_y = bounds

    # Compute direction vector (dx, dy) in image coordinates
    dy = -np.sin(np.deg2rad(angle)) # invert y
    dx = np.cos(np.deg2rad(angle))  

    # choose the boundary in the forward ray direction
    x_edge = np.where(dx >= 0, max_x, min_x)
    y_edge = np.where(dy >= 0, max_y, min_y)

    # parametric distance to vertical and horizontal boundaries
    tx = (x_edge - target_px_x) / dx
    ty = (y_edge - target_px_y) / dy

    # only forward intersections count
    tx = np.where(tx >= 0, tx, np.inf)
    ty = np.where(ty >= 0, ty, np.inf)

    # take the first boundary the ray hits
    use_x = tx < ty
    t = np.where(use_x, tx, ty)

    edge_px_x_out = target_px_x + t * dx
    edge_px_y_out = target_px_y + t * dy

    # round and clip to valid pixel indices
    edge_px_x_out = np.clip(np.rint(edge_px_x_out).astype(int), min_x, max_x)
    edge_px_y_out = np.clip(np.rint(edge_px_y_out).astype(int), min_y, max_y)

    return edge_px_x_out, edge_px_y_out

# define inputs
if '2018' in fid:
    obs_file = glob(f'/store/carroll/col/data/2018/raw/L1/*/{fid}_rdn_obs_ort')[0]
    dsm_file = glob(f'/store/carroll/col/data/2018/raw/L1/*/{fid}_rdn_ort_igm_ort')[0]
elif '2025' in fid:
    fid = '_'.join(fid.split('_')[:3])
    obs_file = glob(f'/store/carroll/col/data/2025/raw/L1/radianceENVI/{fid}_OBS_Data')[0]
    dsm_file = glob(f'/store/carroll/col/data/2025/raw/L1/radianceENVI/{fid}_IGM_Data')[0]
output_file = os.path.join(output_folder, f'{fid}_shade.tif')

# if os.path.exists(output_file):
#     print(f'{fid} already exists, exiting')
#     sys.exit(0)

obs_set = gdal.Open(obs_file, gdal.GA_ReadOnly)
solar_azimuth = obs_set.GetRasterBand(solar_azimuth_band).ReadAsArray()
solar_zenith = obs_set.GetRasterBand(solar_zenith_band).ReadAsArray()
dsm = gdal.Open(dsm_file, gdal.GA_ReadOnly).ReadAsArray()[2,...]

bounds = (0, 0, solar_azimuth.shape[1] - 1, solar_azimuth.shape[0] - 1)

# identify coordinates of all valid target pixels
valid = dsm>=0
valid_loc = np.where(valid)

# identify the coordinates of the solar edge pixel for each target pixel
solar_edge_px_x, solar_edge_px_y = edge_coords_from_target(valid_loc[1], valid_loc[0], cwn_to_math(solar_azimuth[valid]), bounds)

# set up output shade mask
shade_mask = np.ones_like(solar_azimuth)
shade_mask[:] = -9999

# for each target pixel, 
for _l in tqdm(range(len(valid_loc[0]))):
    # identify target, edge px coordinates
    target_px = np.array([valid_loc[1][_l], valid_loc[0][_l]]).reshape(1,-1)
    edge_px = np.array([solar_edge_px_x[_l], solar_edge_px_y[_l]]).reshape(1,-1)

    # caluclate bresenham line - identify the coordinates of all px in a straight line from the the target to edge px
    linepx = bresenham_line.bresenhamline(target_px, edge_px, max_iter=-1)

    # subset to valid px in line
    valid = linepx[:,0] < bounds[2]
    valid[linepx[:,1] >= bounds[3]] = False
    linepx = linepx[valid,:]

    # calculate [horizontal] distance from target px for each point on the bresenham line
    px_dist = np.sqrt((linepx[:,0] - target_px[0,0])**2 + (linepx[:,1] - target_px[0,1])**2)

    # get the dsm value at each point on the bresenham line
    surface_line = dsm[linepx[:, 1], linepx[:, 0]]
    surface_line[np.isfinite(surface_line) == False] = -9999
    
    # calculate the height of the solar ray at each point on the line
    solar_height = dsm[target_px[0,1], target_px[0,0]] + px_dist * np.tan(np.pi / 180 * (90-solar_zenith[target_px[0,1], target_px[0,0]]))
    
    # the pixel is sunlit if the solar height is always higher than the surface (IE, no ray intersection)
    sunlit = np.all(solar_height > surface_line)
    shade_mask[target_px[0,1], target_px[0,0]] = sunlit

driver = gdal.GetDriverByName('GTiff')
outDataset = driver.Create(output_file, obs_set.RasterXSize, obs_set.RasterYSize, 1, gdal.GDT_Float32, ['COMPRESS=LZW'])
outDataset.SetGeoTransform(obs_set.GetGeoTransform())
outDataset.SetProjection(obs_set.GetProjection())
outDataset.GetRasterBand(1).WriteArray(shade_mask, 0, 0)