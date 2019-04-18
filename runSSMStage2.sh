#!/bin/bash -x
# this script is going to be slightly "opinionated", by which I mean it's going to conform to a 
# predefined directory structure.  This is going to (hopefully) simplify our lives.
# let's grab the needed arguments

# This needs to be replaced with a "systemy" anaconda
source /home/anaconda/anaconda2/bin/activate r
echo $PATH

PROJECT_NAME=$1
SORTED_SOURCE_DIR=$2

if [ "$#" -ne 2 ]; then
   echo "\
   This script processes the sorted responsibilities files. To do this it requires 2 
   arguments: the first argument is the name of the project (ex: Mississippi). This 
   must match the first argument to the runSSM.sh script and the second argument is 
   a directory path containing the sorted responsibilites files to process. You don't 
   have to specify an output directory: on success the script will zip the result files 
   and tell you where they are."
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

# The project home must exist, since it carries over from runSSM.sh
if [ ! -d "$PROJECT_HOME" ]; then
  echo "Project ${PROJECT_NAME} must exist" >&2
  exit 1
fi 

# create the project sorted resposibilies dir if it's not here.
SORTED_DIR=${PROJECT_HOME}/4-sorted-responsibilities
[ -d "$SORTED_DIR" ] || mkdir $SORTED_DIR

# Now grab the Sorted files and put them into our directory
/bin/cp ${SORTED_SOURCE_DIR}/*.txt ${SORTED_DIR}
if [ $? -eq 0 ]
then
  echo "Successfully copied source SSM files to ${SORTED_DIR}"
else
  echo "Could not find source SSM files in directory ${SORTED_DIR}" >&2
  exit 1
fi

# Cat the files into 1 file.  It seems to need a blank line at the end, so we do that also
CONCAT_FILE=${SORTED_DIR}/concatentatedFiles.txt
JSON_FILE=${SORTED_DIR}/concatentatedFiles.json

# delete the concatenated and json files if they already exist
[ -e ${CONCAT_FILE} ] && /usr/bin/rm ${CONCAT_FILE}
[ -e ${JSON_FILE} ] && /usr/bin/rm ${JSON_FILE}

# let's get rid of duplicate entries
for i in ${SORTED_DIR}/*.txt 
   do j=$(basename ${SORTED_DIR}/$i .txt)  
      echo $j
      FILE=${SORTED_DIR}/${j}-uniq.txt
      [ -e ${FILE} ] && /usr/bin/rm ${FILE}
      cat $i | /usr/bin/uniq > ${SORTED_DIR}/${j}-uniq.txt 
   done
/usr/bin/cat ${SORTED_DIR}/*-uniq.txt >> ${CONCAT_FILE}
/usr/bin/echo "" >> ${CONCAT_FILE}

# next we run text2json
TEXT_TO_JSON_EXECUTABLE=${SSM_BIN_HOME}/ssm_processing/text2JSON.py
${TEXT_TO_JSON_EXECUTABLE} ${CONCAT_FILE}
if [ $? -eq 0 ]
then
  echo "Successfully created ${CONCAT_FILE}"
else
  echo "Could not create ${CONCAT_FILE}" >&2
  exit 1
fi

# Next is AddCodesToBLM.R
BLM_DIR=${PROJECT_HOME}/3-binary-link-matrix
RCODED_DIR=${PROJECT_HOME}/5-rcoded-ssm
[ -d "$RCODED_DIR" ] || mkdir $CODEDD_DIR
RCODE_EXECUTABLE=${SSM_BIN_HOME}/AddCodesToBLM/AddCodesToBLM.R
RSCRIPT_EXECUTABLE=Rscript
${RSCRIPT_EXECUTABLE} ${RCODE_EXECUTABLE} ${JSON_FILE} ${BLM_DIR} ${RCODED_DIR}
if [ $? -eq 0 ]
then
  echo "Successfully ran ${RCODE_EXECUTABLE}"
else
  echo "Could not run ${RCODE_EXECUTABLE}" >&2
  exit 1
fi
