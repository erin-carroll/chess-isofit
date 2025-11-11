import os
import numpy as np
import matplotlib.pyplot as plt
from spectral.io import envi
from spectral.io.envi import read_envi_header, write_envi_header
from scipy import ndimage
from glob import glob

from isofit.core.fileio import IO
from isofit.core.forward import ForwardModel
from isofit.inversion.inverse import Inversion
from isofit.inversion.inverse_simple import invert_algebraic
from isofit.configs import configs
from isofit.core.geometry import Geometry

import rasterio
from rasterio.warp import reproject, Resampling

def add_byte_order(fp_hdr, byte_order=0):
    """
    Adds 'byte order' to an ENVI .hdr file if it's missing
    """
    hdr = read_envi_header(fp_hdr)
    if 'byte order' not in hdr:
        hdr['byte order'] = byte_order
        write_envi_header(fp_hdr, hdr)

def subset_region(fp_rdn, fp_obs, fp_igm, output_dir, x, y, buf, brighten_factor=1):
    """
    subset a larger flightline, visualize subset rdn, obs, loc (where everything is the same shape, ort or raw)
    """

    # translate x, y to raw space coordinates
    igm = envi.open(fp_igm).open_memmap(interleave='bip').copy()
    rows, cols = igm[...,0].shape
    flat_x = igm[...,0].flatten()
    flat_y = igm[...,1].flatten()
    diffs = np.abs(flat_x - x) + np.abs(flat_y - y)
    idx = np.argmin(diffs)
    row, col = np.unravel_index(idx, (rows, cols))

    flight_id = fp_igm.split('/')[-1].split('_rdn')[0]

    # rdn
    fp_out = os.path.join(output_dir, f'{flight_id}_rdn.hdr')
    meta = envi.open(fp_rdn).metadata
    meta['lines'] = buf*2
    meta['samples'] = buf*2
    out_ds = envi.create_image(fp_out, meta, ext='', force=True)
    out_ds.open_memmap(writable=True)[:,:,:] = envi.open(fp_rdn).open_memmap(interleave='bip')[row-buf:row+buf, col-buf:col+buf, :].copy()
    rdn = envi.open(fp_out).open_memmap(interleave='bip')[:,:,np.array([60,40,30])].copy()
    del out_ds

    # obs
    fp_out = os.path.join(output_dir, f'{flight_id}_obs.hdr')
    meta = envi.open(fp_obs).metadata
    meta['lines'] = buf*2
    meta['samples'] = buf*2
    out_ds = envi.create_image(fp_out, meta, ext='', force=True)
    out_ds.open_memmap(writable=True)[:,:,:] = envi.open(fp_obs).open_memmap(interleave='bip')[row-buf:row+buf, col-buf:col+buf, :].copy()
    obs = envi.open(fp_out).open_memmap(interleave='bip')[:,:,6].copy() # slope
    del out_ds

    # igm
    fp_out = os.path.join(output_dir, f'{flight_id}_igm.hdr')
    meta = envi.open(fp_igm).metadata
    meta['lines'] = buf*2
    meta['samples'] = buf*2
    out_ds = envi.create_image(fp_out, meta, ext='', force=True)
    out_ds.open_memmap(writable=True)[:,:,:] = envi.open(fp_igm).open_memmap(interleave='bip')[row-buf:row+buf, col-buf:col+buf, :].copy()
    loc = envi.open(fp_out).open_memmap(interleave='bip')[:,:,2].copy() # elev
    del out_ds

    # visualize
    fig, axs = plt.subplots(ncols=3, figsize=(15,5))
    axs[0].imshow(rdn/np.max(rdn)*brighten_factor)
    p1 = axs[1].imshow(obs)
    p2 = axs[2].imshow(loc)
    fig.colorbar(p1)
    fig.colorbar(p2)
    axs[0].set_title('rdn')
    axs[1].set_title('obs (slope)')
    axs[2].set_title('loc (elev)')
    plt.show()

def single_px_retrieval(config, rdn, obs, loc, n_states=2, plot=True):
    """
    run a single pixel retrieval, option to visualize surface, atm solution at each step
    """
    
    # set up forward model, io, inversion according to config
    fm = ForwardModel(config) # loads pre-built LUT
    io = IO(config, fm)
    inv = Inversion(config, fm)
    
    # load the isofit geometry representation of the single pixel
    geom = Geometry(obs=obs, loc=loc)
    
    # run the iterative inversions, each adjusting the state vector at each step to minimize the loss function comparing predicted and observed rdn
    states=inv.invert(rdn, geom)
    
    # get solutions converged upon at the final step
    x_surface, x_RT, x_instrument = fm.unpack(states[-1,:])
    
    # do a final inversion with the above solutions to get rfl
    x_alg, coeffs = invert_algebraic(fm.surface, fm.RT, fm.instrument, 
                                         x_surface, x_RT, x_instrument,
                                         rdn, geom)

    # get surface prior mean
    x0 = states[0,...][fm.idx_surface]
    x = x0.copy()
    xa_full = fm.xa(x, geom)
    xa_surface = xa_full[fm.idx_surface]
    
    # surface
    if plot==True:
        def closest_wl(mv):
            return np.argmin(np.abs(io.meas_wl-mv))
        wl = io.meas_wl.copy()
        wl[closest_wl(1360):closest_wl(1410)] = np.nan
        wl[closest_wl(1800):closest_wl(1970)] = np.nan
        fig = plt.figure(figsize=(15,5))
        for n in range(0, states.shape[0]):
            lab = f'step {n}'
            plt.plot(wl, states[n, :n_states*-1], label=lab)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()
    
        # rt
        labs = config.forward_model.radiative_transfer.radiative_transfer_engines[0].statevector_names
        states_rt = states[:, -2:]
        fig, axs = plt.subplots(ncols=2, figsize=(15,5))
        for i in [0,1]:
            axs[i].plot(range(states_rt.shape[0]), states_rt[:,i])
            axs[i].set_title(labs[i])
            axs[i].set_xlabel('step')
        plt.show()

    return x_RT, x_alg, coeffs, xa_surface, wl

def get_raw_obs(fp_obs, fp_glt, fp_rdn):
    """
    Derive raw-space obs data from orthorectified obs data and GLT
    """
    # load data
    obs_ort = envi.open(fp_obs).open_memmap(interleave='bip')
    glt_ort = envi.open(fp_glt).open_memmap(interleave='bip').copy().astype(float)
    rdn_raw = envi.open(fp_rdn).open_memmap(interleave='bip')

    # generate empty array with raw_space shape
    obs_raw = np.full((rdn_raw.shape[0], rdn_raw.shape[1], obs_ort.shape[2]), np.nan, dtype=obs_ort.dtype)
    
    # mask glt_ort
    glt_ort[glt_ort<=0] = np.nan

    # raw positions from GLT
    col_raw = glt_ort[..., 0]
    row_raw = glt_ort[..., 1]
    
    # create valid mask
    valid = np.isfinite(col_raw) & np.isfinite(row_raw)
    
    # convert to int (assuming 1-based indexing in GLT)
    row_idx = row_raw[valid].astype(int) - 1
    col_idx = col_raw[valid].astype(int) - 1
    
    # flip row, col idx to match raw-space coordinate system
    row_idx_flipped = (obs_raw.shape[0] - 1) - row_idx
    col_idx_flipped = (obs_raw.shape[1] - 1) - col_idx
    
    # grab all valid ortho values
    vals = obs_ort[valid, :]   # shape: (n_valid_pixels, bands)
    
    # assign to raw array
    obs_raw[row_idx_flipped, col_idx_flipped, :] = vals
    
    # fill blank values
    rows, cols, bands = obs_raw.shape
    
    # Copy array for output
    obs_filled = obs_raw.copy()
    
    # interpolate, fill by band
    for b in range(bands):
        band = obs_raw[..., b]
        mask = np.isnan(band)
        # Get indices of nearest non-NaN pixels
        idx = ndimage.distance_transform_edt(mask, return_distances=False, return_indices=True)
        obs_filled[..., b] = band[tuple(idx)]

    return obs_filled

def viz_rfl_subset(row1, col1, size, flight, working_dir, n_sample, wl, plt_widget=True):
    fp = glob(os.path.join(working_dir, 'output', '*_rfl.hdr'))[0]
    
    row2 = row1+size; col2 = col1+size
    rfl = envi.open(fp).open_memmap()[row1:row2,col1:col2,:].copy()
    rgb = rfl[...,(60,40,30)]

    rows = np.random.randint(0, rfl.shape[0], size=n_sample)
    cols = np.random.randint(0, rfl.shape[1], size=n_sample)
    
    fig, axs = plt.subplots(ncols=2, figsize=(15,5))
    if plt_widget==False:
        fig.subplots_adjust(right=0.82) 
    
    axs[0].imshow(rgb / np.nanmax(rgb, axis=(0, 1)))
    for i in range(n_sample):
        axs[1].plot(wl, rfl[rows[i], cols[i], :], label=f'row {rows[i]} col {cols[i]}')
        axs[0].scatter(cols[i], rows[i], label=f'row {rows[i]} col {cols[i]}')

    if plt_widget==False:
        fig.legend(
            loc='center left',
            bbox_to_anchor=(1, 0.5))  # x > 1 moves it outside the figure
    else:
        axs[0].legend(loc='upper left', bbox_to_anchor=(1.02, 1))
        axs[1].legend(loc='upper left', bbox_to_anchor=(1.02, 1))
    
    fig.suptitle(flight)
    
    plt.tight_layout() 
    
    plt.show()

def clip_skyview_per_flightline(fp_skyview, fp_ref, fp_out):
    """
    Resample a campaign-wide skyview factor to the geoemtry of individual flightlines
    """
    with rasterio.open(fp_ref) as ref, rasterio.open(fp_skyview) as skyview:    
        dst = np.full((1, ref.height, ref.width),
                      ref.nodata if ref.nodata is not None else np.nan,
                      dtype=np.float32)
    
        reproject(
            source=rasterio.band(skyview, 1),
            destination=dst[0],
            src_transform=skyview.transform,
            src_crs=skyview.crs,
            src_nodata=skyview.nodata,
            dst_transform=ref.transform,
            dst_crs=ref.crs,
            dst_nodata=skyview.nodata if skyview.nodata is not None else -9999,
            resampling=Resampling.bilinear,
        )
    
        profile_out = ref.profile
        profile_out.update(
            dtype=dst.dtype,
            count=1,
            nodata=skyview.nodata if skyview.nodata is not None else -9999,
            interleave='bil'
        )
        with rasterio.open(fp_out, 'w', **profile_out) as dst_ds:
            dst_ds.write(dst)    