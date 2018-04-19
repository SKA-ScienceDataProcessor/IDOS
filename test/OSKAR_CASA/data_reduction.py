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

    casa.run_script_from_file('/BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge_new/image.py',timeout = 6000000)


#class myThread (threading.Thread):
#   def __init__(self, threadID, ms_file, Nfacet):
#      threading.Thread.__init__(self)
#      self.threadID = threadID
#      self.ms_file = ms_file
#      self.Nfacet = Nfacet
#   def run(self):
#      print "Starting " + self.ms_file
#      # Get lock to synchronize threads
#      #threadLock.acquire()
#      casa_imaging(self.ms_file, self.Nfacet, self.threadID)
#      # Free lock to release next thread
#      #threadLock.release()
#

if __name__ == "__main__":
 
    parser = argparse.ArgumentParser(description='Simulation script.',
                                     epilog='')

    parser.add_argument('--msfile', dest='ms_file', type=str , default='./config/1_0.ms', help='Measurement Set file.')

    args = parser.parse_args()   
    
    
    Nfacet = 4 
  
    ms_file = args.ms_file

    t1=Thread(target=casa_imaging(ms_file, Nfacet, 1))
    t2=Thread(target=casa_imaging(ms_file, Nfacet, 2))
    t3=Thread(target=casa_imaging(ms_file, Nfacet, 3))
    t4=Thread(target=casa_imaging(ms_file, Nfacet, 4))

    t1.start()
    t2.start()
    t3.start()
    t4.start() 
   
    #threadLock = threading.Lock()

    # Create new threads and start
#    for t in range(4): 
#       thr = myThread(t+1, ms_file, Nfacet)
#       thr.start()
       # Wait for all threads to complete
#       thr.join()
#    print "Exiting Main Thread" 
