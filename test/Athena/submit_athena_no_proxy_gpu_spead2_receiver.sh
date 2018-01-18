#!/bin/bash

#SBATCH --nodes=2
#SBATCH --partition=gpuq
#SBATCH --gres=gpu:1
#SBATCH --time=10:00:00
#SBATCH --account=pawsey0245 

source /home/blao/OSKAR/bashrc

APP_ROOT="/home/blao/OSKAR/IDOS/test/Athena"
SID=$(date +"spead2_receiver_N"$1_"%Y-%m-%dT%H-%M-%S")
LOG_DIR=$APP_ROOT"/logs/"$SID
mkdir -p $LOG_DIR # to remove potential directory creation conflicts later
GRAPH_DIR="/home/blao/OSKAR/IDOS/logical_graphs/Athena/spead2_receiver.json"
CLUSTER="Tianhe2"
srun -N 2 -n 2 -p gpuq -A pawsey0245 /group/pawsey0245/blao/pyml/bin/python -m dlg.deploy.pawsey.start_dfms_cluster -l $LOG_DIR -L $GRAPH_DIR -d -c $CLUSTER -v 3 

#-R "receiver"
