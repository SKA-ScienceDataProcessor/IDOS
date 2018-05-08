#!/bin/bash 


APP_ROOT="/BIGDATA1/ac_shao_tan_1/OSKAR/daliuge-master/dfms/deploy/pawsey"
SID=$(date +"ska1_low_N"$1_"%Y-%m-%dT%H-%M-%S")
LOG_DIR=$APP_ROOT"/logs/"$SID
mkdir -p $LOG_DIR # to remove potential directory creation conflicts later
GRAPH_DIR="/BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/daliuge/lg/oskar_casa_img.json"
CLUSTER="Tianhe2"

rm -rf /BIGDATA1/ac_shao_tan_1/OSKAR/IDOS/test/OSKAR_CASA/daliuge/config/*

yhrun -n $1 -N $1 -p gpu /BIGDATA1/ac_shao_tan_1/OSKAR/python/bin/python $APP_ROOT"/start_dfms_cluster.py" -l $LOG_DIR -L $GRAPH_DIR -d -c $CLUSTER -v 3
