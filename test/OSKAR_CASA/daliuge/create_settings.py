# -*- coding: utf-8 -*-
"""Simulate a Measurement Set."""

import subprocess
import argparse
import numpy
import ConfigParser
import json


class EqualsSpaceRemover:
    output_file = None
    def __init__( self, new_output_file ):
        self.output_file = new_output_file

    def write( self, what ):
        self.output_file.write( what.replace( " = ", "=", 1 ) )



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Create OSKAR 2.7.0 ini file')
 
    parser.add_argument('--outputini', dest='output_ini', type=str, default='./config/1_0', help='output ini file name')
    
    parser.add_argument('--dropuid', dest='drop_uid', type=str, default='2_0_1/0',  help='drop uid.')

    args = parser.parse_args()

    ini_file = args.output_ini
    ms_file = "%s.ms" % ini_file

    sky_model = '/BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/daliuge/sky_Cen_A_si.osm'
    tele_input_dir = '/BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/daliuge/aa4.tm'

    lg = json.load(open('/BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/daliuge/lg/oskar_casa_img.json'))
    
    for jd in lg['nodeDataArray']:
        if (jd['text'] == 'Scatter by Channel'):
           for kw in ['num_of_copies', 'num_of_splits']:
               if kw in jd:
                  num_chan = int(jd[kw])

    freq_start = 100000000.0
    freq_stop = 400000000.0
    freq_c = numpy.linspace(freq_start, freq_stop, num_chan)
    id_f = ini_file.split('_')
    freq_id = int(id_f[len(id_f)-1])
    freq = freq_c[freq_id]

    config = ConfigParser.RawConfigParser()
    #General
    config.add_section('General')
    config.set('General', 'app', '/BIGDATA1/ac_shao_tan_1/OSKAR/OSKAR-2.7/bin/oskar_sim_interferometer')
    config.set('General', 'version', '2.7.0')
    #interferometer
    config.add_section('interferometer')
    config.set('interferometer', 'channel_bandwidth_hz', '1.0')
    config.set('interferometer', 'ms_filename', ms_file)
    config.set('interferometer', 'time_average_sec', '0.0')
    #observation
    config.add_section('observation')    
    config.set('observation', 'length', '100.0')
    config.set('observation', 'num_channels', '1')
    config.set('observation', 'num_time_steps', '100')
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


