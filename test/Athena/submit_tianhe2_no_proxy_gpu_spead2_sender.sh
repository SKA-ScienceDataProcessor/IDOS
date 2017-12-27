#!/bin/bash

source /home/blao/OSKAR/bashrc

APP_ROOT="/home/blao/OSKAR/IDOS/test/Athena"
SID=$(date +"spead2_sender_N"$1_"%Y-%m-%dT%H-%M-%S")
LOG_DIR=$APP_ROOT"/logs/"$SID
mkdir -p $LOG_DIR # to remove potential directory creation conflicts later
GRAPH_DIR="/home/blao/OSKAR/IDOS/logical_graphs/Athena/spead2_sender.json"
CLUSTER="Tianhe2"

srun -n 2 -N 2 -p gpuq -A pawsey0245 /group/pawsey0245/blao/pyml/bin/python $APP_ROOT"/start_dfms_cluster.py" -l $LOG_DIR -L $GRAPH_DIR -d -c $CLUSTER -v 3
