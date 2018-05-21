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
import multiprocessing


#Define a function for the thread
def casa_imaging(ms_file, Nfacet, NID):
    casa = drivecasa.Casapy(working_dir=os.path.curdir,
                         casa_logfile=False,
                         timeout = 1200,
                         echo_to_stdout=False)
    casa.run_script(["ms_file='{}'".format(ms_file)])

    casa.run_script(["Nfacet={}".format(Nfacet)])
    casa.run_script(["NID={}".format(NID)])

    casa.run_script_from_file('/BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/MPI/image.py',timeout = 60000000)


if __name__ == "__main__":
 
    parser = argparse.ArgumentParser(description='Simulation script.',
                                     epilog='')

    parser.add_argument('--msfile', dest='ms_file', type=str , default='./config/1_0.ms', help='Measurement Set file.')

    args = parser.parse_args()   
    
    
    Nfacet = 4 
  
    ms_file = args.ms_file

    jobs = []
    for i in range(0, Nfacet):
        process = multiprocessing.Process(target=casa_imaging,args=(ms_file, Nfacet, i))
	jobs.append(process) 
 
    # Start the processes  
    for j in jobs:
	j.start()

    # Ensure all of the processes have finished
    for j in jobs:
	j.join() 
