"""Simulate a Measurement Set."""
import os
import subprocess
import argparse
import numpy
import time
import ConfigParser

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Simulate a Measurement Set')
    
    parser.add_argument('--skymodel', dest='sky_model', help='a sky model file',
                        default='./sky_model/sky_cen_A_1k.mod', type=str)

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    #sky model 
    sky_model = args.skymodel
    #number of time steps 
    num_time_steps = [1, 6, 60, 600, 1200]

    ini_file = './conf/sim_cenA.ini' 

    config = ConfigParser.RawConfigParser()
    config.read(ini_file)    
    start_freq = config.getfloat('observation', 'start_frequency_hz')

    for n in num_time_steps:
       #create a new conf file
       ms_file = './data/n%s.ms' %s n 
       config.set('interferometer', 'ms_filename', ms_file)
       config.set('observation', 'num_time_steps', str(n)) 
       config.set('sky', 'oskar_sky_model\file', sky_model)
       with open(ini_file 'w+') as configfile:
            config.write(configfile)
       clock_start = time.time()
       subprocess.call(["oskar_sim_interferometer", ini_file])
       clock_end = time.time()
       #record oskar run time
       log_string = '%i %09i %.1f' % \
                   (num_time_steps, start_freq, (clock_end - clock_start))

       sky_split = sky_model.split("_")[-1]
       log_file = "./results/data_log_%s" % sky_split 
       with open(log_file, "a") as f:
           f.write(log_string + '\n')



