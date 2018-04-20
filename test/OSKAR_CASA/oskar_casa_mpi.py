#!/usr/bin/python

import os
import time
from mpi4py import MPI

if __name__ == '__main__':
    time_start = time.time()
    rank = MPI.COMM_WORLD.Get_rank()
    num_process = MPI.COMM_WORLD.Get_size()
    rank_str = str(rank)
    os.system('python /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge_new/create_settings.py --outputini /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge_new/config/1_%s ' % rank_str)
    os.system('python /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge_new/run_interferometer.py --inifile  /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge_new/config/1_%s --outputmsfile  /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge_new/config/1_%s.ms ' % (rank_str,rank_str))
    os.system('python /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge_new/data_reduction.py --msfile /BIGDATA/ac_shao_tan_1/OSKAR/OSKAR_CASA/no_daliuge_new/config/1_%s.ms' % rank_str) 
    time_stop = time.time()
    use_time = time_stop-time_start
    print "use time: %.3f" % use_time
