import numpy as np
import os
from glob import glob
import pickle

from isofit.core.fileio import IO
from isofit.core.forward import ForwardModel
from isofit.inversion.inverse import Inversion
from isofit.inversion.inverse_simple import invert_algebraic, invert_simple, invert_analytical
from isofit.configs import configs
from isofit.core.geometry import Geometry
import logging

# Enable the ISOFIT logger
logging.getLogger().setLevel(logging.INFO)

os.chdir('/store/carroll/col/data/')

# prepare representative single pxs
fp = '2018/rccs/single_pxs_cal_tarp.pkl'
with open(fp, 'rb') as f:
    single_px = pickle.load(f)
fids = [x for x in single_px['rdn'].keys() if '20180611' in x]

modeled_rdns = {k: {} for k in fids}
rccs = {k: {} for k in fids}

targets = ['white_tarp', 'black_tarp']

# derive factors for each flight, target
for fid in fids:   
    # load config file
    fp_config = glob(os.path.join('2018/rccs', f'{fid}_6c_', 'config', '*_isofit.json'))[0]
    config = configs.create_new_config(fp_config)

    # set up forward model, io, inv according to config
    fm = ForwardModel(config) # loads pre-built LUT
    io = IO(config, fm)
    inv = Inversion(config, fm)

    for target in targets:
        print(fid, target)
        try:
            # load the single pixel representation
            rdn_ = single_px['rdn'][fid][target]
            obs_ = single_px['obs'][fid][target]
            loc_ = single_px['loc'][fid][target]
            geom = Geometry(obs=obs_, loc=loc_)         
    
            # run isofit per px
            states=inv.invert(rdn_, geom)
            x_surface, x_RT, x_instrument = fm.unpack(states[-1,:])
            x_alg, coeffs = invert_algebraic(fm.surface, fm.RT, fm.instrument, x_surface, x_RT, x_instrument, rdn_, geom)
    
            # get single px rcc
            fp_rfl = f'2018/insitu/cal_{target}_neon.txt'
            insitu_rfl = np.loadtxt(fp_rfl)[:,1]
            modeled_rdn = fm.calc_meas(np.concatenate([x_alg, x_RT, x_instrument]), geom, insitu_rfl)
            rcc_ = modeled_rdn/rdn_
           
            rccs[fid][target] = rcc_
            modeled_rdns[fid][target] = modeled_rdn
            
        except Exception as e:
            print(f"Error for flight {fid}, key {target}: {e}")

# export
fp_out = '2018/rccs/insitu_rccs_6c_20260107.pkl'
with open(fp_out, 'wb') as f:
    pickle.dump(rccs, f)
