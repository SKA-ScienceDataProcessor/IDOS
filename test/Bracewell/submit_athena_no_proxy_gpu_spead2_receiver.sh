#!/bin/bash

#SBATCH --nodes=5
#SBATCH --time=02:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:4
#SBATCH --mem=128g
#SBATCH --job-name=Receiver

export MODULEPATH=$MODULEPATH:/flush1/tob020/modulefiles
module load oskar

module load openmpi boost

APP_ROOT="/home/wu082/proj/IDOS/test/Bracewell"
#SID=$(date +"spead2_receiver_N"$1_"%Y-%m-%dT%H-%M-%S")
SID=$SLURM_JOB_ID"_Receiver"
LOG_DIR=$APP_ROOT"/logs/"$SID
mkdir -p $LOG_DIR # to remove potential directory creation conflicts later
GRAPH_DIR="/home/wu082/proj/IDOS/logical_graphs/Bracewell/spead2_receiver.json"
CLUSTER="Bracewell"
source /flush1/tob020/venvs/jacal/bin/activate
mpirun -np 5  python -m dlg.deploy.pawsey.start_dfms_cluster -l $LOG_DIR -L $GRAPH_DIR -d -c $CLUSTER -v 3 

#-R "receiver"
