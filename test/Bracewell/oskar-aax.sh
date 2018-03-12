#!/bin/bash
# Markus Dolensky, ICRAR, 2018-03-09

#SBATCH --job-name=OskarAAx
#SBATCH --time=1-12:00:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:4
#SBATCH --mem=30g
#SBATCH --mail-type=END
#SBATCH --mail-user=markus.dolensky@uwa.edu.au
#SBATCH --output=/flush1/dol040/oskar/log/oskar-job%A.log
#SBATCH --error=/flush1/dol040/oskar/log/oskar-job%A.err

# make sure to set scenario
SCENARIO="aa1-64k"
#SCENARIO="aa1-6h"

echo "SLURM_JOB_NODELIST: " $SLURM_JOB_NODELIST
echo "SLURM_JOBID: " $SLURM_JOBID
echo "SCENARIO: " $SCENARIO

# not sure all modules are needed by oskar; most of it are casacore dependencies
module load cfitsio cuda fftw hdf5 qt wcslib

# directory setup
APP_ROOT="/home/dol040/proj/IDOS"
WRK_ROOT="/flush1/dol040/oskar"
LOG_DIR=${WRK_ROOT}/log
IMG_DIR=${WRK_ROOT}/img
VIS_DIR=${WRK_ROOT}/vis
mkdir -p $LOG_DIR $IMG_DIR $VIS_DIR

# file names
VISNAME=${VIS_DIR}/${SCENARIO}-${SLURM_JOBID}.vis
FITSROOT=${IMG_DIR}/${SCENARIO}-${SLURM_JOBID}
INTER_INI=conf/Bracewell/${SCENARIO}-oskar_sim_interferometer.ini
IMAGER_INI=conf/Bracewell/${SCENARIO}-oskar_imager.ini

case "$SCENARIO" in
  aa1-6h)  
	  # AA1 6 h workload paras
	  START_TIME_UTC="01-01-2000 20:00:00"
	  OBS_LENGTH="06:00:00"
	  NUM_TIME_STEPS=24000
	  START_FREQUENCY_HZ=114428000
	  NUM_CHANNELS=364
	  FREQUENCY_INC_HZ=4578
	  # set MAX_SOURCES_PER_CHUNK to evenly distribute 24000 sky model sources onto 4 GPUs
	  MAX_SOURCES_PER_CHUNK=6000
	  IMG_SIZE=1024
	  ;;
  aa1-64k)
	  # AA1 64k channel workload paras
	  START_TIME_UTC="01-01-2000 23:00:00"
	  OBS_LENGTH="00:02:00"
	  NUM_TIME_STEPS=133
	  START_FREQUENCY_HZ=50000000
	  NUM_CHANNELS=65536
	  FREQUENCY_INC_HZ=4578
	  # set MAX_SOURCES_PER_CHUNK to evenly distribute 24000 sky model sources onto 4 GPUs
	  MAX_SOURCES_PER_CHUNK=6000
	  IMG_SIZE=1024
	  ;;
  *)
	  echo "unkown scenario - aborting"
	  exit 1
	  ;;
esac

# patch OSKAR settings to tune workload
cd $APP_ROOT
oskar_sim_interferometer --set $INTER_INI simulator/use_gpus true
oskar_sim_interferometer --set $INTER_INI simulator/max_sources_per_chunk $MAX_SOURCES_PER_CHUNK

oskar_sim_interferometer --set $INTER_INI observation/start_time_utc "$START_TIME_UTC"
oskar_sim_interferometer --set $INTER_INI observation/length $OBS_LENGTH
oskar_sim_interferometer --set $INTER_INI observation/num_time_steps $NUM_TIME_STEPS

oskar_sim_interferometer --set $INTER_INI observation/start_frequency_hz $START_FREQUENCY_HZ
oskar_sim_interferometer --set $INTER_INI observation/num_channels $NUM_CHANNELS
oskar_sim_interferometer --set $INTER_INI observation/frequency_inc_hz $FREQUENCY_INC_HZ

oskar_sim_interferometer --set $INTER_INI interferometer/oskar_vis_filename $VISNAME

# execute simulation
oskar_sim_interferometer $INTER_INI

# generate FITS image for visual inspection with e.g. ds9
oskar_imager --set $IMAGER_INI image/use_gpus true
oskar_imager --set $IMAGER_INI image/input_vis_data $VISNAME
oskar_imager --set $IMAGER_INI image/root_path $FITSROOT
oskar_imager --set $IMAGER_INI image/size $IMG_SIZE
oskar_imager $IMAGER_INI


