#!/bin/bash

yhrun -N 1 -n 1 -p gpu python /BIGDATA/ac_shao_tan_1/OSKAR/oskar_reference_simulations/gleam_imaging_test_mpi/run.py sim_gleam.json
#echo $RUNLINE
#$RUNLINE >> /BIGDATA/ac_shao_tan_1/OSKAR/oskar_reference_simulations/gleam_imaging_test/log
