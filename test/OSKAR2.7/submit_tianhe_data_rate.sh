#!/bin/bash

yhrun -N 1 -n 1 -p gpu python /BIGDATA/ac_shao_tan_1/OSKAR/IDOS-master/test/OSKAR2.7/simulate_data_rate.py --skymodel ./sky_model/sky_cen_A_si.mod --inifile  ./conf/sim_cenA_data_rate.ini --tele_mode ./telescope/aa1.tm 
