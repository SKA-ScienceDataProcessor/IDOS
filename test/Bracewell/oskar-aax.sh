#!/bin/bash
# 
# OSKAR2 job submission script
#
# Usage: oskar-aax.sh [scenario]
#
# Markus Dolensky, ICRAR, 2018-03-09
#

# SLURMify
#SBATCH --job-name=OskarAAx
##SBATCH --time=1-12:00:00
#SBATCH --time=10:00:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:4
#SBATCH --mem=30g
#SBATCH --mail-type=ALL
#SBATCH --mail-user=markus.dolensky@uwa.edu.au
#SBATCH --output=/flush1/dol040/oskar/log/oskar-job%A.log
#SBATCH --error=/flush1/dol040/oskar/log/oskar-job%A.err

# enable OSKAR; Rodrigo's /modulefiles activates casacore among others 
export MODULEPATH=$MODULEPATH:/flush1/tob020/modulefiles
module load oskar

# make sure to set the scenario to one of the following options:
# epa-64k | aa1-64k | aa2-64k | aa3-64k | aa4-64k | epa-6h | aa1-6h | aa2-6h | aa3-6h | aa4-6h
SCENARIO=${1:-"epa-6h"}

# set to true to run or generate bits
RUN_INTER="true"
GENERATE_FITS="true"
GENERATE_MS="false"

# push some info to stdout showing that the job has started
echo "SLURM_JOB_NODELIST: <${SLURM_JOB_NODELIST}>"
echo "SLURM_JOBID: <${SLURM_JOBID}>"
echo "SCENARIO: <${SCENARIO}>"

#
# scenario and job specific OSKAR settings
#

# directory setup
APP_ROOT="${HOME}/proj/IDOS"
SKY_DIR=${APP_ROOT}/spead/sender
WRK_ROOT="/flush1/dol040/oskar"
LOG_DIR=${WRK_ROOT}/log
IMG_DIR=${WRK_ROOT}/img
VIS_DIR=${WRK_ROOT}/vis
mkdir -p $LOG_DIR $IMG_DIR $VIS_DIR

# file names
VISNAME=${VIS_DIR}/${SCENARIO}-${SLURM_JOBID}.vis
if [ "${GENERATE_MS}" = "true" ]
then
  MS_FILENAME=${VIS_DIR}/${SCENARIO}-${SLURM_JOBID}.ms
else
  MS_FILENAME=""
fi
FITSROOT=${IMG_DIR}/${SCENARIO}-${SLURM_JOBID}
INTER_INI=conf/Bracewell/${SCENARIO}-oskar_sim_interferometer.ini
IMAGER_INI=conf/Bracewell/${SCENARIO}-oskar_imager.ini

# sky model
SM_NAME="sky"
SM_FILE=${SKY_DIR}/${SM_NAME}.osm
case "$SM_NAME" in
  sky_Cen_A | sky_Cen_A_si )
	  PHASE_CENTRE_RA_DEG="201.4"
	  PHASE_CENTRE_DEC_DEG="-43"
	  # increase MAX_SOURCES_PER_CHUNK to fit on a single GPU
	  MAX_SOURCES_PER_CHUNK=50000
	  ;;
  *)
	  PHASE_CENTRE_RA_DEG="20"
	  PHASE_CENTRE_DEC_DEG="-30"
      # the model's 3 components do not provide much data/work to partition across GPUs (degraded case)
	  MAX_SOURCES_PER_CHUNK=1	  
	  ;;
esac

case "$SCENARIO" in
  epa-64k | aa1-64k | aa2-64k | aa3-64k | aa4-64k)
	  # 64k channel workload paras
	  DOUBLE_PRECISION="false"
	  USE_GPUS="true"
	  START_TIME_UTC="01-01-2000 23:00:00"
	  OBS_LENGTH="00:02:00"
	  NUM_TIME_STEPS=133
	  START_FREQUENCY_HZ=50000000
	  NUM_CHANNELS=65536
	  FREQUENCY_INC_HZ=4578
	  IMG_SIZE=1024
	  ;;
  epa-6h | aa1-6h | aa2-6h | aa3-6h | aa4-6h)
	  # 6 h workload paras
	  DOUBLE_PRECISION="false"
	  USE_GPUS="true"
	  START_TIME_UTC="01-01-2000 20:00:00"
	  OBS_LENGTH="06:00:00"
	  NUM_TIME_STEPS=24000
	  START_FREQUENCY_HZ=114428000
	  NUM_CHANNELS=364
	  FREQUENCY_INC_HZ=4578
	  IMG_SIZE=1024
	  ;;
  *)
	  echo "unkown scenario - aborting"
	  exit 1
	  ;;
esac

if [ "${RUN_INTER}" = "true" ]
then
  cd $APP_ROOT

# patch OSKAR settings to tune workload
  oskar_sim_interferometer --set $INTER_INI simulator/double_precision $DOUBLE_PRECISION
  oskar_sim_interferometer --set $INTER_INI simulator/use_gpus $USE_GPUS
  oskar_sim_interferometer --set $INTER_INI simulator/max_sources_per_chunk $MAX_SOURCES_PER_CHUNK

  oskar_sim_interferometer --set $INTER_INI observation/phase_centre_ra_deg $PHASE_CENTRE_RA_DEG
  oskar_sim_interferometer --set $INTER_INI observation/phase_centre_dec_deg $PHASE_CENTRE_DEC_DEG

  oskar_sim_interferometer --set $INTER_INI observation/start_frequency_hz $START_FREQUENCY_HZ
  oskar_sim_interferometer --set $INTER_INI observation/num_channels $NUM_CHANNELS
  oskar_sim_interferometer --set $INTER_INI observation/frequency_inc_hz $FREQUENCY_INC_HZ

  oskar_sim_interferometer --set $INTER_INI observation/start_time_utc "$START_TIME_UTC"
  oskar_sim_interferometer --set $INTER_INI observation/length $OBS_LENGTH
  oskar_sim_interferometer --set $INTER_INI observation/num_time_steps $NUM_TIME_STEPS

  oskar_sim_interferometer --set $INTER_INI sky/oskar_sky_model/file $SM_FILE
  oskar_sim_interferometer --set $INTER_INI interferometer/oskar_vis_filename $VISNAME
  oskar_sim_interferometer --set $INTER_INI interferometer/ms_filename $MS_FILENAME

  # execute simulation
  oskar_sim_interferometer $INTER_INI
fi

if [ "${GENERATE_FITS}" = "true" ]
then
  # generate FITS image for visual inspection with e.g. ds9
  oskar_imager --set $IMAGER_INI image/double_precision $DOUBLE_PRECISION
  oskar_imager --set $IMAGER_INI image/use_gpus $USE_GPUS
  oskar_imager --set $IMAGER_INI image/fov_deg 4
  oskar_imager --set $IMAGER_INI image/input_vis_data $VISNAME
  oskar_imager --set $IMAGER_INI image/root_path $FITSROOT
  oskar_imager --set $IMAGER_INI image/size $IMG_SIZE
  
  # go execute
  oskar_imager $IMAGER_INI
fi

