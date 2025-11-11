from glob import glob
import subprocess

rfls = [x for x in glob('/store/carroll/col/data/2018/deploy_1c_20251001/*/output/*rfl') if 'subs' not in x]

for fp_rfl in rfls:
    fp_ewt_out = fp_rfl.replace('rfl', 'ewt')
    fid = fp_rfl.split('/')[-1].removesuffix('_rfl')
    lf = f'/home/carroll/logs/ewt_{fid}.log'
    cmd_str = f'isofit ewt {fp_rfl} {fp_ewt_out} --logfile {lf} --n_cores 64'
    print(cmd_str)
    subprocess.run(cmd_str, shell=True)