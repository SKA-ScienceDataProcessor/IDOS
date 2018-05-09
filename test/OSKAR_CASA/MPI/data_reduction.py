"""Make images using CASA."""

import os
import argparse
from os.path import isdir
import drivecasa
#import threading
from threading import Thread
import numpy
import math
import shutil
import time


#Define a function for the thread
def casa_imaging(ms_file, Nfacet, NID):
    casa = drivecasa.Casapy(working_dir=os.path.curdir,
                         casa_logfile=False,
                         timeout = 1200,
                         echo_to_stdout=False)
    casa.run_script(["ms_file='{}'".format(ms_file)])

    casa.run_script(["Nfacet={}".format(Nfacet)])
    casa.run_script(["NID={}".format(NID)])

    casa.run_script_from_file('/BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/MPI/image.py',timeout = 6000000)


if __name__ == "__main__":
 
    parser = argparse.ArgumentParser(description='Simulation script.',
                                     epilog='')

    parser.add_argument('--msfile', dest='ms_file', type=str , default='./config/1_0.ms', help='Measurement Set file.')

    args = parser.parse_args()   
    
    
    Nfacet = 4 
  
    ms_file = args.ms_file

    t0=Thread(target=casa_imaging(ms_file, Nfacet, 0))
    t1=Thread(target=casa_imaging(ms_file, Nfacet, 1))
    t2=Thread(target=casa_imaging(ms_file, Nfacet, 2))
    t3=Thread(target=casa_imaging(ms_file, Nfacet, 3))

    t0.start()
    t1.start()
    t2.start()
    t3.start() 
   
