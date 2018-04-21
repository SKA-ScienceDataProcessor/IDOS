"""Simulate a Measurement Set."""

import subprocess
import argparse
import ConfigParser

class EqualsSpaceRemover:
    output_file = None
    def __init__( self, new_output_file ):
        self.output_file = new_output_file

    def write( self, what ):
        self.output_file.write( what.replace( " = ", "=", 1 ) )



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Simulation script.',
                                     epilog='')
    parser.add_argument('--inifile', dest='ini_file', type=str , default='./config/1_0', help='INI config file.')

    parser.add_argument('--outputmsfile', dest='output_msfile', type=str , default='./config/1_0.ms', help='output Measuremnet Set file.')
    

    args = parser.parse_args()
   
    ini_file = args.ini_file

    output_msfile = args.output_msfile
   
    config = ConfigParser.RawConfigParser()

    config.read(ini_file)

    if output_msfile == None :
       raise NameError
    else:
       config.set('interferometer', 'ms_filename', output_msfile)
       with open(ini_file, 'w+') as configfile:
            config.write(EqualsSpaceRemover(configfile)) 
       subprocess.call(["/BIGDATA/ac_shao_tan_1/OSKAR/OSKAR-2.7/bin/oskar_sim_interferometer", ini_file])
    
