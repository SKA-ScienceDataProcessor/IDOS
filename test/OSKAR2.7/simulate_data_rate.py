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
                        default='./sky_model/sky_cen_A_si.mod', type=str)

    parser.add_argument('--inifile', dest='ini_file', help='config ini file',
                        default='./conf/sim_cenA.ini', type=str)

    parser.add_argument('--telemodel', dest='tele_mode', help='telescope mode',
                        default='./telescope/aa1.tm', type=str)


    args = parser.parse_args()

    return args

class EqualsSpaceRemover:
    output_file = None
    def __init__( self, new_output_file ):
        self.output_file = new_output_file

    def write( self, what ):
        self.output_file.write( what.replace( " = ", "=", 1 ) )

if __name__ == "__main__":
    args = parse_args()
    #sky model 
    sky_model = args.sky_model
    #number of time steps 
    num_time_steps = [120] # 2 minutes 

    ini_file = args.ini_file

    config = ConfigParser.RawConfigParser()
    config.read(ini_file)    
    start_freq = config.getfloat('observation', 'start_frequency_hz')

    for n in num_time_steps:
       #create a new conf file
       tele_name = args.tele_mode.split('/')[-1]
       ms_file = "./data/%sn%s.ms" % (tele_name,n) 
       vis_file = "./data/%sn%s.vis" % (tele_name,n)
       config.set('interferometer', 'ms_filename', ms_file)
       config.set('interferometer', 'oskar_vis_filename', vis_file)
       config.set('observation', 'num_time_steps', str(n)) 
       integration_time = 0.9 #unit:seconds
       obs_length = float(n/integration_time)
       config.set('observation', 'length', str(obs_length))
       config.set('sky', 'oskar_sky_model\\file', sky_model)
       config.set('telescope', 'input_directory', args.tele_mode)
       with open(ini_file, 'w+') as configfile:
            config.write(EqualsSpaceRemover(configfile))
       
       clock_start = time.time()
       subprocess.call(["oskar_sim_interferometer", ini_file])
       clock_end = time.time()
       #record oskar run time
       log_string = '%i %09i %.1f' % \
                   (n, start_freq, (clock_end - clock_start))

       sky_split = sky_model.split("_")[-1]
       log_file = "./results/data_log_%s.txt" % sky_split 
       with open(log_file, "a") as f:
           f.write(log_string + '\n')



