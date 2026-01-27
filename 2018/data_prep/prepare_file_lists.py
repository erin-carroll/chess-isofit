import os
from glob import glob

# # all fids for line-level apply_oe
# fol = '/store/carroll/col/data/2018/raw/L1/'
# fp_out = '/store/carroll/repos/chess-isofit/2018/2_deploy/crbu_2018_fids_new.txt'
# fids = glob(os.path.join(fol, '*', f'*rdn_ort'))
# fids = [os.path.basename(x).removesuffix('_rdn_ort') for x in fids]
# with open(fp_out, 'w') as f:
#     for fid in fids:
#         f.write(fid + '\n')

# mosaicking lists
fp = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_obs.txt'
with open(fp) as f:
    fids = f.readlines()
fids = [os.path.basename(x.strip()).removesuffix('_rdn_obs_ort') for x in fids]
print(len(fids))
print(fids[0])

# rfl
fp_out = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_refl.txt'
working_dir = '/store/carroll/col/data/2018/deploy_6c_20260120'
with open(fp_out, 'w') as f:
    for fid in fids:
        f.write(f'{working_dir}/{fid}/output/{fid}_rfl' + '\n')

# unc
fp_out = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_unc.txt'
working_dir = '/store/carroll/col/data/2018/deploy_6c_20260120'
with open(fp_out, 'w') as f:
    for fid in fids:
        f.write(f'{working_dir}/{fid}/output/{fid}_uncert' + '\n')

# shade
fp_out = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_shade.txt'
working_dir = '/store/carroll/col/data/2018/shade'
with open(fp_out, 'w') as f:
    for fid in fids:
        f.write(f'{working_dir}/{fid}_shade.tif' + '\n')

# ewt
fp_out = '/store/carroll/col/data/2018/mosaic/file_lists/top_priority_isofit_ewt.txt'
working_dir = '/store/carroll/col/data/2018/deploy_6c_20260120'
with open(fp_out, 'w') as f:
    for fid in fids:
        f.write(f'{working_dir}/{fid}/output/{fid}_ewt' + '\n')
