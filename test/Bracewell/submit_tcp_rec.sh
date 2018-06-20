#!/bin/bash

#SBATCH --nodes=3
#SBATCH --time=01:00:00
#SBATCH --ntasks-per-node=1
#SBATCH --mem=64g
#SBATCH --job-name=Receiver

export MODULEPATH=$MODULEPATH:/flush1/tob020/modulefiles
export DLG_DISABLE_CHECKSUM=1
module load oskar

module load openmpi boost

APP_ROOT="/home/wu082/proj/IDOS/test/Bracewell"
SID=$(date +"spead2_receiver_N"$1_"%Y-%m-%dT%H-%M-%S")
LOG_DIR=$APP_ROOT"/logs/"$SID
mkdir -p $LOG_DIR # to remove potential directory creation conflicts later
#GRAPH_DIR="/home/wu082/proj/IDOS/logical_graphs/Bracewell/spead2_receiver.json"
#GRAPH_DIR="/home/wu082/proj/IDOS/logical_graphs/Bracewell/spead2_receiver_tcp.json"
GRAPH_DIR="/home/wu082/proj/IDOS/logical_graphs/Bracewell/spead2_receiver_tcp_nocrc.json"
#GRAPH_DIR="/home/wu082/proj/IDOS/logical_graphs/Bracewell/spead2_receiver_tcp_nocrc_nobufsize.json"
#GRAPH_DIR="/home/wu082/proj/IDOS/logical_graphs/Bracewell/spead2_receiver_tcp_memdrop.json"
CLUSTER="Bracewell"
source /flush1/tob020/venvs/jacal/bin/activate
#source /flush1/tob020/venvs/jacal3/bin/activate
DLG_MON_HOST="sdp-dfms.ddns.net"
DLG_MON_PORT="8081"
export PYTHONPATH=/home/wu082/proj/jacal/apps/python
mpirun -np 3  python -m dlg.deploy.pawsey.start_dfms_cluster -l $LOG_DIR -L $GRAPH_DIR -c $CLUSTER -v 3 -m $DLG_MON_HOST -o $DLG_MON_PORT
#mpirun -np 3  python -m dlg.deploy.pawsey.start_dfms_cluster -l $LOG_DIR -L $GRAPH_DIR -c $CLUSTER -v 3 -m $DLG_MON_HOST -o $DLG_MON_PORT --part-algo mysarkar
#mpirun -np 6  python -m dlg.deploy.pawsey.start_dfms_cluster -l $LOG_DIR -L $GRAPH_DIR -c $CLUSTER -v 3 --part-algo mysarkar

#-R "receiver"
