#!/bin/bash

yhrun -N 1 -n 1 -p gpu python /BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR2.7/simulate_data_rate.py --skymodel ./sky_model/sky_Cen_A_si.osm --inifile  ./conf/sim_cenA_data_rate.ini --telemode ./telescope/aa1.tm 
