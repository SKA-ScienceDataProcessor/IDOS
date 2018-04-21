# -*- coding: utf-8 -*-
"""Simulate a Measurement Set."""

import subprocess
import argparse
import numpy
import ConfigParser


class EqualsSpaceRemover:
    output_file = None
    def __init__( self, new_output_file ):
        self.output_file = new_output_file

    def write( self, what ):
        self.output_file.write( what.replace( " = ", "=", 1 ) )



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Create OSKAR 2.7.0 ini file')
 
    parser.add_argument('--outputini', dest='output_ini', type=str, default='./config/1_0', help='output ini file name')

    args = parser.parse_args()

    ini_file = args.output_ini
    ms_file = "%s.ms" % ini_file

    sky_model = './sky_Cen_A_si.osm'
    tele_input_dir = './ska1_low.tm'

    freq_start = 100000000.0
    freq_stop = 400000000.0
    freq_c = numpy.linspace(freq_start, freq_stop, 64)
    id_f = ini_file.split('_')
    freq_id = int(id_f[len(id_f)-1])
    freq = freq_c[freq_id]

    config = ConfigParser.RawConfigParser()
    #General
    config.add_section('General')
    config.set('General', 'app', 'oskar_sim_interferometer')
    config.set('General', 'version', '2.7.0')
    #interferometer
    config.add_section('interferometer')
    config.set('interferometer', 'channel_bandwidth_hz', '1.0')
    config.set('interferometer', 'ms_filename', ms_file)
    config.set('interferometer', 'time_average_sec', '0.0')
    #observation
    config.add_section('observation')    
    config.set('observation', 'length', '1.0')
    config.set('observation', 'num_channels', '1')
    config.set('observation', 'num_time_steps', '10')
    config.set('observation', 'phase_centre_dec_deg', '-43.02')
    config.set('observation', 'phase_centre_ra_deg', '201.36')
    config.set('observation', 'start_frequency_hz', str(freq))
    config.set('observation', 'start_time_utc', '01-01-2015 18:00:00.0')
    #simulator
    config.add_section('simulator')
    config.set('simulator', 'double_precision', 'false')
    config.set('simulator', 'keep_log_file', 'false')
    #sky
    config.add_section('sky')  
    config.set('sky', 'oskar_sky_model\\file', sky_model)
    #telescope
    config.add_section('telescope')    
    config.set('telescope', 'input_directory', tele_input_dir)
    config.set('telescope', 'pol_mode', 'Scalar')

    with open(ini_file, 'w+') as configfile:
         config.write(EqualsSpaceRemover(configfile))


