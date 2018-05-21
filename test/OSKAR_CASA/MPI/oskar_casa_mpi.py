#!/usr/bin/python

import os
import time
from mpi4py import MPI

if __name__ == '__main__':
    time_start = time.time()
    rank = MPI.COMM_WORLD.Get_rank()
    num_process = MPI.COMM_WORLD.Get_size()
    rank_str = str(rank)
    rank_size_str = str(num_process)

    os.system('python /BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/MPI/create_settings.py --outputini /BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/MPI//config/1_%s  --ranksize %s' % (rank_str, rank_size_str))
    os.system('python /BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/MPI/run_interferometer.py --inifile  /BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/MPI/config/1_%s --outputmsfile  /BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/MPI/config/1_%s.ms ' % (rank_str,rank_str))
    os.system('python /BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/MPI/data_reduction.py --msfile /BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/MPI/config/1_%s.ms' % rank_str) 
    time_stop = time.time()
    use_time = time_stop-time_start
    MPI.COMM_WORLD.barrier()
    print "use time: %.3f" % use_time
