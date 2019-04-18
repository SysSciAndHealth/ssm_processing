#!/bin/bash
# this script is going to be slightly "opinionated", by which I mean it's going to conform to a 
# predefined directory structure.  This is going to (hopefully) simplify our lives.
# let's grab the needed arguments

# This needs to be replaced with a "systemy" anaconda
source /home/anaconda/anaconda2/bin/activate r
echo $PATH

PROJECT_NAME=$1
SSM_SOURCE_DIR=$2

if [ "$#" -ne 2 ]; then
   echo "\
   This script runs three steps of the SSM workflow: the monodirectionalize, rlabeling, and
   blm steps.  To do this it requires 2 arguments: the first argument is
   the name of the project (ex: Mississippi) and the second argument is a directory
   containing the SSM json files you want processed.  You don't have to specify an
   output directory: on success the script will zip the result files and tell you
   where they are."
   exit
fi
SSM_ROOT=/projects/systemsscience/SSMS
# You can overwrite the home by setting the SSM_HOME_DIR environment var
# For example: export SSM_HOME_DIR=new_home_dir
if [[ -z "${SSM_HOME_DIR}" ]]; then
  SSM_HOME="${SSM_ROOT}/processData/${USER}"
else
  SSM_HOME="${SSM_HOME_DIR}"
fi

# should clean this up with a common bin dir.  This should work until then
if [[ -z "${SSM_BIN_HOME_DIR}" ]]; then
  SSM_BIN_HOME="${SSM_ROOT}/bin"
else
  SSM_BIN_HOME="${SSM_BIN_HOME_DIR}"
fi

PROJECT_HOME=${SSM_HOME}/${PROJECT_NAME}
echo "setting project home to $PROJECT_HOME"

# create the project home if it's not there
[ -d "$PROJECT_HOME" ] || mkdir -p $PROJECT_HOME

# create the project sim dir if it's not here, Could have used mkdir -p, but 
# this seems cleaner.
SSM_DIR=${PROJECT_HOME}/0-ssm
[ -d "$SSM_DIR" ] || mkdir $SSM_DIR

# Now grab the SSM files and put them into our SSM directory
/bin/cp ${SSM_SOURCE_DIR}/*.json ${SSM_DIR}
if [ $? -eq 0 ]
then
  echo "Successfully copied source SSM files to ${SSM_DIR}"
else
  echo "Could not find source SSM files in directory ${SSM_SOURCE_DIR}" >&2
  exit 1
fi

# Now we want to run the mono-directionalize code.
MONO_DIRECTIONALIZED_DIR=${PROJECT_HOME}/1-ssm-monodir
[ -d "$MONO_DIRECTIONALIZED_DIR" ] || mkdir $MONO_DIRECTIONALIZED_DIR

MONO_EXECUTABLE=${SSM_BIN_HOME}/ssm_processing/monodirectionalize_SSM_edges.py
${MONO_EXECUTABLE} $SSM_DIR $MONO_DIRECTIONALIZED_DIR
if [ $? -eq 0 ]
then
  echo "Successfully monodirectionalized SSM files"
else
  echo "Could not monodirectionalize SSM files" >&2
  exit 1
fi

# Next is add_rlabels_to_SSMs.py
RLABELED_DIR=${PROJECT_HOME}/2-ssm-monodir-rlabeled
[ -d "$RLABELED_DIR" ] || mkdir $RLABELED_DIR
RLABEL_EXECUTABLE=${SSM_BIN_HOME}/ssm_processing/add_rlabels_to_SSMs.py
${RLABEL_EXECUTABLE} $MONO_DIRECTIONALIZED_DIR $RLABELED_DIR TRUE
if [ $? -eq 0 ]
then
  echo "Successfully rlabeled SSM files"
else
  echo "Could not rlabel SSM files" >&2
  exit 1
fi

# Next is blm.R
BLM_DIR=${PROJECT_HOME}/3-binary-link-matrix
[ -d "$BLM_DIR" ] || mkdir $BLM_DIR
BLM_EXECUTABLE=${SSM_BIN_HOME}/binary-link-matrix/blm.R
RSCRIPT_EXECUTABLE=Rscript
${RSCRIPT_EXECUTABLE} ${BLM_EXECUTABLE} $RLABELED_DIR ${BLM_DIR}
if [ $? -eq 0 ]
then
  echo "Successfully created BLM files"
else
  echo "Could not created BLM files" >&2
  exit 1
fi

ZIP_NAME=${PROJECT_HOME}/${PROJECT_NAME}-3-binary-link-matrix
/usr/bin/zip -r $ZIP_NAME $BLM_DIR
if [ $? -eq 0 ]
then
  echo "zip file binary link matrix results is ${ZIP_NAME}.zip"
else
  echo "Problem creating zip file $ZIP_NAME" >&2
  exit 1
fi
