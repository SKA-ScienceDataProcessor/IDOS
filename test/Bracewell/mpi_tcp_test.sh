#!/bin/bash

#SBATCH --nodes=1
#SBATCH --time=00:01:00
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=SenderTest

export MODULEPATH=$MODULEPATH:/flush1/tob020/modulefiles
module load oskar
module load cuda openmpi boost


source /flush1/tob020/venvs/jacal/bin/activate
mpirun -np 1 python test_ib.py
#mpirun -np 2 python /home/wu082/proj/IDOS/spead/sender/spead_sender_tcp.py 

