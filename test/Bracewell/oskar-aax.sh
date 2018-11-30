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
#SBATCH --time=10:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:4
#SBATCH --mem=30g
#SBATCH --mail-type=ALL
#SBATCH --mail-user=markus.dolensky@uwa.edu.au
#SBATCH --output=/flush1/dol040/oskar/log/oskar-job%A.log
#SBATCH --error=/flush1/dol040/oskar/log/oskar-job%A.err

# enable OSKAR; Rodrigo's /modulefiles activates casacore among others 
export MODULEPATH=$MODULEPATH:/flush1/tob020/modulefiles
# module load oskar     
# scenario 'partition' requires bugfixed local installation of OSKAR
module swap intel-cc/16.0.4.258 intel-mkl/2017.2.174
module load cuda casacore/2.0.3


# make sure to set the scenario to one of the following options:
# epa-64k | aa1-64k | aa2-64k | aa3-64k | aa4-64k | epa-6h | aa1-6h | aa2-6h | aa3-6h | aa4-6h | aa4-1c | partition
SCENARIO=${1:-"epa-6h"}

# set to true to run or generate bits
RUN_INTER="true"
GENERATE_FITS="true"
GENERATE_MS="false"

# constants across scenarios
FOV_DEG=5
# 
USE_GPUS="true"
# keep GPU_COUNT in sync with slurm parameter --gres=gpu:N
GPU_COUNT=4
let "UPPERIDX = $GPU_COUNT - 1"

# push some info to stdout showing that the job has started
echo "SLURM_JOB_NODELIST: <${SLURM_JOB_NODELIST}>"
echo "SLURM_JOBID: <${SLURM_JOBID}>"
echo "SCENARIO: <${SCENARIO}>"
echo "CUDA_VISIBLE_DEVICES: <${CUDA_VISIBLE_DEVICES}>"

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


case "$SCENARIO" in
  epa-64k | aa1-64k | aa2-64k | aa3-64k | aa4-64k)
	  # 64k channel workload paras
	  DOUBLE_PRECISION="false"	  
	  START_TIME_UTC="01-01-2000 23:00:00"
	  OBS_LENGTH="00:02:00"
	  NUM_TIME_STEPS=133
	  START_FREQUENCY_HZ=50000000
	  NUM_CHANNELS=65536
	  FREQUENCY_INC_HZ=4578
	  SM_NAME="sky_Cen_A_si"
	  POL_MODE="Full"
	  IMG_SIZE=1024
	  ;;
  epa-6h | aa1-6h | aa2-6h | aa3-6h | aa4-6h)
	  # 6 h workload paras
	  DOUBLE_PRECISION="false"
	  START_TIME_UTC="01-01-2000 20:00:00"
	  OBS_LENGTH="06:00:00"
	  NUM_TIME_STEPS=24000
	  START_FREQUENCY_HZ=114428000
	  NUM_CHANNELS=364
	  FREQUENCY_INC_HZ=4578
	  SM_NAME="sky_Cen_A_si"
	  POL_MODE="Full"
	  IMG_SIZE=1024
	  ;;
  aa4-1c)
	  # single channel workload paras
	  DOUBLE_PRECISION="false"
	  START_TIME_UTC="01-01-2015 18:00:00"
	  OBS_LENGTH="00:01:00"
	  NUM_TIME_STEPS=60
	  START_FREQUENCY_HZ=100000000
	  NUM_CHANNELS=1
	  FREQUENCY_INC_HZ=4687500
	  SM_NAME="sky_Cen_A_si1000"
	  POL_MODE="Scalar"
	  IMG_SIZE=1024
	  ;;
  partition)
	  # EoR sky model partitioning test case; it's a logical expansion of the single channel setup aa4-1c
	  DOUBLE_PRECISION="false"
	  START_TIME_UTC="01-01-2015 18:00:00"
	  OBS_LENGTH="00:01:00"
	  NUM_TIME_STEPS=60
	  START_FREQUENCY_HZ=(209991850 210244750 210497950 210751700)
	  NUM_CHANNELS=1
	  FREQUENCY_INC_HZ=(252900 253200 253750 254000)
	  SM_NAME=$SCENARIO
	  POL_MODE="Scalar"
	  IMG_SIZE=1024
	  FOV_DEG=6
	  ;;
  *)
	  echo "unkown scenario - aborting"
	  exit 1
	  ;;
esac

# sky model
case "$SM_NAME" in
  sky_Cen_A | sky_Cen_A_si | sky_Cen_A_si1000 )
	  PHASE_CENTRE_RA_DEG="201.36"
	  PHASE_CENTRE_DEC_DEG="-43.02"
	  # increase MAX_SOURCES_PER_CHUNK to fit on a single GPU
	  MAX_SOURCES_PER_CHUNK=50000
	  SM_FILE=${SKY_DIR}/${SM_NAME}.osm
	  ;;
  partition )
	  PHASE_CENTRE_RA_DEG="201"
	  PHASE_CENTRE_DEC_DEG="-44"
	  MAX_SOURCES_PER_CHUNK=50000
	  SM_NAME=("sky_eor_model_f210.12" "sky_eor_model_f210.37" "sky_eor_model_f210.62" "sky_eor_model_f210.88")
	  SM_FILE=(${SKY_DIR}/${SM_NAME[0]}.osm ${SKY_DIR}/${SM_NAME[1]}.osm ${SKY_DIR}/${SM_NAME[2]}.osm ${SKY_DIR}/${SM_NAME[3]}.osm)
	  ;;
  *)
	  PHASE_CENTRE_RA_DEG="20"
	  PHASE_CENTRE_DEC_DEG="-30"
      # the model's 3 components do not provide much data/work to partition across GPUs (degraded case)
	  MAX_SOURCES_PER_CHUNK=1	  
	  SM_FILE=${SKY_DIR}/${SM_NAME}.osm
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

  oskar_sim_interferometer --set $INTER_INI telescope/pol_mode $POL_MODE

  oskar_sim_interferometer --set $INTER_INI sky/oskar_sky_model/file $SM_FILE
  oskar_sim_interferometer --set $INTER_INI interferometer/oskar_vis_filename $VISNAME
  oskar_sim_interferometer --set $INTER_INI interferometer/ms_filename $MS_FILENAME

  # further tailoring in case of running parallel instances
  if [ "${SCENARIO}" = "partition" ]
  then
	  for idx in $(seq 0 $UPPERIDX)
	  do
		  echo "device index: <${idx}>"
		  
		  # segregate input/output files etc. of each parallel OSKAR instance to be launched
		  cp $INTER_INI "${INTER_INI}.${idx}"
		  # let "DEVICE_ID = $idx - 1"
		  oskar_sim_interferometer --set "${INTER_INI}.${idx}" simulator/cuda_device_ids $idx
		  oskar_sim_interferometer --set "${INTER_INI}.${idx}" observation/start_frequency_hz ${START_FREQUENCY_HZ[$idx]}
		  oskar_sim_interferometer --set "${INTER_INI}.${idx}" observation/frequency_inc_hz ${FREQUENCY_INC_HZ[$idx]}
		  oskar_sim_interferometer --set "${INTER_INI}.${idx}" sky/oskar_sky_model/file ${SM_FILE[$idx]}
		  if [ -n "$VISNAME" ]; then
			  oskar_sim_interferometer --set "${INTER_INI}.${idx}" interferometer/oskar_vis_filename "${VISNAME}.${idx}"
		  fi
		  if [ -n "$MS_FILENAME" ]; then
			  oskar_sim_interferometer --set "${INTER_INI}.${idx}" interferometer/ms_filename "${MS_FILENAME}.${idx}"
		  fi
		  
		  # parallel execution of simulation, each on a single GPU of the same node
		  oskar_sim_interferometer "${INTER_INI}.${idx}" &
		  
		  # TODO: cleanup of (temporary) settings files "${INTER_INI}.[0-3]"
      done	  
  else
	  # execute simulation
	  oskar_sim_interferometer $INTER_INI
  fi
fi

if [ "${GENERATE_FITS}" = "true" ]
then
  # generate FITS image for visual inspection with e.g. ds9
  oskar_imager --set $IMAGER_INI image/double_precision $DOUBLE_PRECISION
  oskar_imager --set $IMAGER_INI image/use_gpus $USE_GPUS
  oskar_imager --set $IMAGER_INI image/fov_deg $FOV_DEG
  oskar_imager --set $IMAGER_INI image/size $IMG_SIZE
  
  if [ "${SCENARIO}" = "partition" ]
  then
	  # TODO: proper sync with background simulation task; imager fails due to incomplete .vis if sleep is too short!
	  sleep 60
	  
	  for idx in $(seq 0 $UPPERIDX)
	  do
		  oskar_imager --set $IMAGER_INI image/input_vis_data "${VISNAME}.${idx}"
		  oskar_imager --set $IMAGER_INI image/root_path "$FITSROOT.${idx}"
		  
		  # run
		  oskar_imager $IMAGER_INI
	  done
  else
	  oskar_imager --set $IMAGER_INI image/input_vis_data $VISNAME
	  oskar_imager --set $IMAGER_INI image/root_path $FITSROOT

	  # run
	  oskar_imager $IMAGER_INI
  fi
  
fi

