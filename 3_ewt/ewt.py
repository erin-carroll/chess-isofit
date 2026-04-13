from glob import glob
import os
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--fp_rfl", required=True)
args = parser.parse_args()
fp_rfl = args.fp_rfl

fp_ewt_out = fp_rfl.replace('rfl', 'ewt')
if os.path.exists(fp_ewt_out)==False:
    fid = fp_rfl.split('/')[-1].removesuffix('_rfl')
    lf = f'/home/carroll/logs/ewt_{fid}.log'
    cmd_str = f'isofit ewt {fp_rfl} {fp_ewt_out} --logfile {lf} --n_cores 64 --ewt_limit 0.6'
    print(cmd_str)
    subprocess.run(cmd_str, shell=True)