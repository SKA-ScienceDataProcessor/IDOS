#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import time
import numpy
import oskar

if __name__ == '__main__':
    # Global options.
    precision = 'single'
    phase_centre_ra_deg = 0.0
    phase_centre_dec_deg = 60.0
    output_root = 'test_via_files'
    start_frequency_hz=100000000.0 # 100MHz
    num_channels=1
    frequency_inc_hz=20000000.0   # 20MHz
    #start_time_utc=01-01-2000 12:00:00.0
    #length=00:00:05.0
    num_time_steps=1200

    # Set up the sky model.
    oskar_sky_model='/group/pawsey0245/rdodson/IDOS/spead/sender/sky_Cen_A.osm'
    phase_centre_ra_deg=199.6
    phase_centre_dec_deg=-45.0
    num_channels=1
    start_frequency_hz=100000000
    frequency_inc_hz=20000000
    oskar_sky_model='/group/pawsey0245/rdodson/IDOS/oskarpy/examples/gleam_mod.si.mod'
    #oskar_sky_model='/group/pawsey0245/rdodson/IDOS/spead/sender/sky.osm'
    #phase_centre_ra_deg=20.0
    #phase_centre_dec_deg=-30.0
    #num_channels=3
    #start_frequency_hz=100000000
    #frequency_inc_hz=20000000
    #phase_centre_ra_deg=20
    #phase_centre_dec_deg=-30
    num_time_steps=24
    start_time_utc='01-01-2000 00:00:00.000'
    length='10:00:00.000'

    #sky = oskar.Sky.generate_grid(phase_centre_ra_deg, phase_centre_dec_deg,
    #                              16, 1.5, precision=precision)
    sky = oskar.Sky.load(oskar_sky_model, precision=precision)
    #sky.append_sources(phase_centre_ra_deg, phase_centre_dec_deg, 1.0)

    # Set up the telescope model.
    tel = oskar.Telescope(precision)
    tel.set_channel_bandwidth(frequency_inc_hz)
    tel.set_time_average(5.0)
    tel.set_pol_mode('Scalar')
    tm_path='/group/pawsey0245/rdodson/IDOS/spead/sender/mwa2.tm'
    tm_path='/group/pawsey0245/rdodson/IDOS/spead/sender/ska1_low.tm'
    tm_path='/group/pawsey0245/rdodson/IDOS/spead/sender/epa+mwa.tm'
    tm_path='/group/pawsey0245/rdodson/IDOS/spead/sender/aa4.tm'
    tm_path='/group/pawsey0245/rdodson/IDOS/spead/sender/telescope.tm'
    tm_path='/group/pawsey0245/rdodson/IDOS/spead/sender/aa1.tm'
    tel.load(tm_path)
    print('No of Stations: '+str(tel.num_stations)+' No of Baselines '+str(tel.num_baselines))
    # Set station properties after stations have been defined.
    tel.set_phase_centre(phase_centre_ra_deg, phase_centre_dec_deg)
    tel.set_station_type('Gaussian beam')
    tel.set_gaussian_station_beam_width(5.0, start_frequency_hz)

    # Set up two imagers for natural and uniform weighting.
    imagers = []
    for i in range(2):
        imagers.append(oskar.Imager(precision))
        imagers[i].set(fov_deg=2.0, image_size=2048, algorithm='W-projection',
                       input_file=output_root+'.ms')
    imagers[0].set(weighting='Natural', output_root=output_root+'_Natural')
    imagers[1].set(weighting='Uniform', output_root=output_root+'_Uniform')

    # Set up the basic interferometer simulator.
    simulator = oskar.Interferometer(precision)
    simulator.set_settings_path(os.path.abspath(__file__))
    simulator.set_max_sources_per_chunk(500)
    simulator.set_sky_model(sky)
    simulator.set_telescope_model(tel)
    simulator.set_observation_frequency(100.0e6)
    simulator.set_observation_time(
        start_time_mjd_utc=51545.5, length_sec=43200.0, num_time_steps=num_time_steps)
    # 01-01-2000 12UT
    simulator.set_output_measurement_set(output_root+'.ms')

    # Simulate and image visibilities.
    start = time.time()
    print('Running interferometer simulator...')
    simulator.run()
    print('Completed Simulations after %.3f seconds.' % (time.time() - start))
    for i, imager in enumerate(imagers):
        print('Running imager %d...' % i)
        imager.run()
    print('Completed after %.3f seconds.' % (time.time() - start))
