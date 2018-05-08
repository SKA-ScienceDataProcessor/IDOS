"""Make images using CASA."""

import os
import argparse
from os.path import isdir
import drivecasa
from threading import Thread
import numpy
import math
import shutil
import time
import json


#Define a function for the thread
def casa_imaging(ms_file, Nfacet, NID):
    casa = drivecasa.Casapy(working_dir=os.path.curdir,
                         casa_logfile=False,
                         timeout = 3600,
                         echo_to_stdout=False)
    casa.run_script(["ms_file='{}'".format(ms_file)])

    casa.run_script(["Nfacet={}".format(Nfacet)])
    casa.run_script(["NID={}".format(NID)])

    casa.run_script_from_file('/BIGDATA1/ac_shao_tan_1/OSKAR//IDOS/test/OSKAR_CASA/daliuge/image.py',timeout = 6000000)


if __name__ == "__main__":
 
    parser = argparse.ArgumentParser(description='Simulation script.',
                                     epilog='')

    parser.add_argument('--msfile', dest='ms_file', type=str , default='./config/1_0.ms', help='Measurement Set file.')
    parser.add_argument('--dropuid', dest='drop_uid', type=str, default='2_0_1/0',  help='drop uid.')

    args = parser.parse_args()  

    scatter_uid = args.drop_uid.split('/')
    scatter_id = scatter_uid[len(scatter_uid)-1] 

    lg = json.load(open('/BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/daliuge/lg/oskar_casa_img.json'))
    for jd in lg['nodeDataArray']:
        if (jd['text'] == 'Scatter by Facet'):
           for kw in ['num_of_copies', 'num_of_splits']:
               if kw in jd:
                  num_copy = int(jd[kw])
                  #print(num_copy)    
    
    Nfacet = num_copy 
  
    ms_file = args.ms_file

    casa_imaging(ms_file, Nfacet, scatter_id)

   
