#!/bin/sh

rm -rf ./config/*

RUNLINE="yhrun -N $1 -n $1 -p gpu python /BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/MPI/oskar_casa_mpi.py"
echo $RUNLINE
$RUNLINE > $1_$2.log

rm -rf casapy*
