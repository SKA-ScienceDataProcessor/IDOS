#!/bin/bash

yhrun -N 1 -n 1 -p gpu python /BIGDATA/ac_shao_tan_1/OSKAR/IDOS-master/test/OSKAR2.7/simulate.py --skymodel ./sky_model/sky_cen_A_20k.mod --inifile  ./conf/sim_cenA_aa4.ini 
