#!/bin/bash

#SBATCH --nodes=1
#SBATCH --time=01:00:00
#SBATCH --ntasks-per-node=2
#SBATCH --gres=gpu:4
#SBATCH --mem=64g
#SBATCH --job-name=Sender

export MODULEPATH=$MODULEPATH:/flush1/tob020/modulefiles
module load oskar
module load cuda openmpi boost


source /flush1/tob020/venvs/jacal/bin/activate
mpirun -np 2 python /home/wu082/proj/IDOS/spead/sender/spead_sender_tcp.py 

