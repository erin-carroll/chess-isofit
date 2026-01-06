from glob import glob
import os

for domain in ['ALMO', 'UPTA', 'CRBU']:

    fp_obs_list = f'/store/carroll/col/data/2025/mosaic/file_lists/top_priority_obs_{domain}.txt'
    obs_files = [x.strip() for x in open(fp_obs_list, 'r').readlines()]
    fids = ['_'.join(x.split('/')[-1].split('_')[0:4]) for x in obs_files]
    
    fp_out = f'/store/carroll/col/data/2025/mosaic/file_lists/top_priority_shade_{domain}.txt'
    shade_files = ['/store/carroll/col/data/2025/shade/' + x + '_shade.tif' for x in fids]
    with open(fp_out, 'w') as f:
        for s in shade_files:
            f.write(f'{s}\n')