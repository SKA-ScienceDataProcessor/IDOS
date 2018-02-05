#!/bin/bash

#SBATCH --nodes=6
#SBATCH --time=01:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:4
#SBATCH --mem=64g
#SBATCH --job-name=Sender

export MODULEPATH=$MODULEPATH:/flush1/tob020/modulefiles
module load oskar
module load cuda openmpi boost


APP_ROOT="/home/wu082/proj/IDOS/test/Bracewell"
SID=$(date +"spead2_sender_N"$1_"%Y-%m-%dT%H-%M-%S")
LOG_DIR=$APP_ROOT"/logs/"$SID
mkdir -p $LOG_DIR # to remove potential directory creation conflicts later
GRAPH_DIR="/home/wu082/proj/IDOS/logical_graphs/Bracewell/spead2_sender.json"
CLUSTER="Bracewell"
source /flush1/tob020/venvs/jacal/bin/activate
mpirun -np 6  python -m dlg.deploy.pawsey.start_dfms_cluster -l $LOG_DIR -L $GRAPH_DIR -d -c $CLUSTER -v 3

