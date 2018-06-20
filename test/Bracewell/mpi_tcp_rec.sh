#!/bin/bash

#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --ntasks-per-node=2
#SBATCH --mem=64g
#SBATCH --job-name=Sender

export MODULEPATH=$MODULEPATH:/flush1/tob020/modulefiles
module load openmpi

source /flush1/tob020/venvs/jacal/bin/activate
mpirun -np 2 python /home/wu082/proj/IDOS/spead/receiver/iperf_recv.py

