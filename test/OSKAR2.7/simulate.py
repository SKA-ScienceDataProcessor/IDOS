# -*- coding: utf-8 -*-
"""Simulate a Measurement Set."""

import os
from os.path import join
from collections import OrderedDict
import subprocess
import argparse
import json
from shutil import copyfile
import numpy
import math
import time
#from mpi4py import MPI


def create_sky_model(sky_file, ra, dec, stokes_i_flux):
    """Create a sky model file."""
    if not os.path.isdir(os.path.dirname(sky_file)):
        os.makedirs(os.path.dirname(sky_file))
    fh = open(sky_file, 'w')
    for ra_, dec_, I_ in zip(ra, dec, stokes_i_flux):
        fh.write('%.14f, %.14f, %.3f\n' % (ra_, dec_, I_))
    fh.close()


def dict_to_ini(settings_dict, ini):
    """Convert a dictionary of settings to and OSKAR settings ini file."""
    ini_dir = os.path.dirname(ini)
    if not ini_dir == "" and not os.path.isdir(ini_dir):
        os.makedirs(ini_dir)
    for group in sorted(settings_dict):
        for key in sorted(settings_dict[group]):
            key_ = group + key
            value_ = settings_dict[group][key]
            subprocess.call(["oskar_settings_set", "-q", ini,
                            key_, str(value_)])


def run_interferometer(ini, verbose=True):
    """Run the OSKAR interferometer simulator."""
    if verbose:
        subprocess.call(["oskar_sim_interferometer", ini])
    else:
        subprocess.call(["oskar_sim_interferometer", "-q", ini])


def create_settings(settings, sky_file, ms_path, freq_hz, num_times, smearing=True):
    """Create simulation settings file."""
    sim = settings['sim']
    obs = sim['observation']
    tel = sim['telescope']

    if not os.path.isdir(os.path.dirname(ms_path)):
        os.mkdir(os.path.dirname(ms_path))

    if smearing:
        dt_ave = obs['obs_length'] / num_times
    else:
        dt_ave = 0.0

    s = OrderedDict()
    s['simulator/'] = {
        'double_precision': 'false',
        'keep_log_file': 'false'
    }
    s['sky/'] = {
        'oskar_sky_model/file': sky_file
    }
    s['observation/'] = {
        'start_frequency_hz': freq_hz,
        'num_channels': 1,
        'start_time_utc': obs['start_time_utc'],
        'length': obs['obs_length'],
        'num_time_steps': num_times,
        'phase_centre_ra_deg': obs['ra_deg'],
        'phase_centre_dec_deg': obs['dec_deg']
    }
    s['telescope/'] = {
        'input_directory': tel['path'],
        'pol_mode': 'Scalar',
        'station_type': 'Isotropic beam'
    }
    s['interferometer/'] = {
        'time_average_sec': dt_ave,
        'channel_bandwidth_hz': obs['channel_bw_hz'],
        'ms_filename': ms_path
    }
    return s


def run(settings, verbose=True):
    """Run the OSKAR simulation."""
    sim_dir = settings['path']
    sim = settings['sim']
    obs = sim['observation']
    sky_file = join(sim_dir, 'sky_cen_A_20k.mod')
    if not os.path.isdir(os.path.dirname(sky_file)):
        os.makedirs(os.path.dirname(sky_file))
    os.system('cp sky_cen_A_20k.mod ./%s' % sim_dir)
    f = obs['freq_hz']
    for n in obs['num_times']:
        # ===== Without analytical smearing =====
        ini_file = join(sim_dir, 'n%04if%09i.ini' % (n, f))
        ms_out = join(sim_dir, 'n%04if%09i.ms' % (n, f))
        if not os.path.isdir(ms_out):
            s = create_settings(settings, sky_file, ms_out,
                freq_hz=f, num_times=n, smearing=False)
        dict_to_ini(s, ini_file)
        clock_start = time.time()
        run_interferometer(ini_file, verbose)
        clock_end = time.time()
        #record oskar run time
        log_string = '%i %09i %.1f' % \
            (n, f, (clock_end - clock_start))
        with open("data_log.txt", "a") as log_file:
            log_file.write(log_string + '\n')



