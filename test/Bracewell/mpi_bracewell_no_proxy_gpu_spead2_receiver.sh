#!/bin/bash

#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:4
#SBATCH --mem=64g
#SBATCH --job-name=Receiver

export MODULEPATH=$MODULEPATH:/flush1/tob020/modulefiles
module load oskar

module load openmpi boost

APP_ROOT="/home/wu082/proj/IDOS/test/Bracewell"
SID=$(date +"spead2_receiver_N"$1_"%Y-%m-%dT%H-%M-%S")
LOG_DIR=$APP_ROOT"/logs/"$SID
mkdir -p $LOG_DIR # to remove potential directory creation conflicts later
GRAPH_DIR="/home/wu082/proj/IDOS/logical_graphs/Bracewell/spead2_receiver.json"
CLUSTER="Bracewell"
source /flush1/tob020/venvs/jacal/bin/activate
#mpirun -np 6  python -m dlg.deploy.pawsey.start_dfms_cluster -l $LOG_DIR -L $GRAPH_DIR -d -c $CLUSTER -v 3 
#mpirun -np 2 python /home/wu082/proj/IDOS/spead/receiver/spead_recv.py 41000 /flush1/wu082/jacal_data/mpi_data mpi
mpirun -np 1 python /home/wu082/proj/IDOS/spead/receiver/spead_recv_binary.py 41000 /flush1/wu082/jacal_data/mpi_data mpi
#-R "receiver"
