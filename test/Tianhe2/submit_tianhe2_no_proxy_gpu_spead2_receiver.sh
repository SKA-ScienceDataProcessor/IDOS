#!/bin/bash 

DFMS_MON_HOST="sdp-dfms.ddns.net"
DFMS_MON_PORT="8098"
APP_ROOT="/BIGDATA/ac_shao_tan_1/OSKAR/daliuge-master/dfms/deploy/pawsey"
SID=$(date +"spead2_N"$1_"%Y-%m-%dT%H-%M-%S")
LOG_DIR=$APP_ROOT"/logs/"$SID
mkdir -p $LOG_DIR # to remove potential directory creation conflicts later
GRAPH_DIR="/BIGDATA/ac_shao_tan_1/OSKAR/IDOS/logical_graphs/spead2_receiver.json"
CLUSTER="Tianhe2"

yhrun -n 2 -N 2 -p gpu /BIGDATA/ac_shao_tan_1/OSKAR/python/bin/python $APP_ROOT"/start_dfms_cluster.py" -l $LOG_DIR -L $GRAPH_DIR -d -c $CLUSTER -v 3
