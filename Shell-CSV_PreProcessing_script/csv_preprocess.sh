#!/bin/bash

########################################################################################################
#	Program Description	: Shell script to pre-process a source CSV file & create detail and control file
#	Developer			: Soorya Parthiban
#	Date				: 2023-07-08	
########################################################################################################

## Required parameters
# 1. Business Date YYYY-MM-DD
# 2. Parameter File in .txt format

########################################################################################################

##Defining PATHS

PARENT_DIR=/d/001_Data/data_projects/data_projects/Shell-CSV_PreProcessing
PARAMETER_DIR=parameter
LOGS_DIR=logs
SOURCE_DATA_DIR=source_data
ARCHIVE_DATA_DIR=archive_data
STAGE_DATA_DIR=stage_data
ERROR_DATA_DIR=error_data

##Checking for correct parameters are passed when calling the script

if [ $# -eq 2 ]
  then
    if [[ $1 == [0-9][0-9][0-9][0-9]-[0-3][0-9]-[0-1][0-9] ]]	&& [[ $2 == *.txt ]]
		then
			echo "SUCCESS: Business Date and Parameter file validated."
			
			BUSINESS_DATE_ARG=$1
			PARAM_FILE_ARG=$2
			
			cd $PARENT_DIR/$PARAMETER_DIR
			
			##Getting parameter values from parameter file
			FILENAME=$(awk 'NR==1' $PARAM_FILE_ARG | awk -F "=" '{print $2}')
			FILEDELIMITER=$(awk 'NR==2' $PARAM_FILE_ARG | awk -F "=" '{print $2}')
			HEADERVAL=$(awk 'NR==3' $PARAM_FILE_ARG | awk -F "=" '{print $2}')
			TRAILERVAL=$(awk 'NR==5' $PARAM_FILE_ARG | awk -F "=" '{print $2}')
			BUSINESS_DATE_POS=$(awk 'NR==4' $PARAM_FILE_ARG | awk -F "=" '{print $2}')
			TRAILERVAL_POS=$(awk 'NR==6' $PARAM_FILE_ARG | awk -F "=" '{print $2}')
			TARGETFILEFORMAT=$(awk 'NR==7' $PARAM_FILE_ARG | awk -F "=" '{print $2}')
			
			cd $PARENT_DIR/$SOURCE_DATA_DIR
			
			for file in $(find . -name "*$FILENAME*")
			do	
				if [ $BUSINESS_DATE_ARG == $(awk 'NR==1' $file | awk -F "$FILEDELIMITER" '{print $2}') ] && [ $HEADERVAL == $(awk 'NR==1' $file | awk -F "$FILEDELIMITER" '{print $1}') ] && [ $TRAILERVAL == $(tail -1 $file | awk -F "$FILEDELIMITER" '{print $1}') ]
					then matched_file=$file
					
				elif [ $BUSINESS_DATE_ARG == $(awk 'NR==1' $file | awk -F "$FILEDELIMITER" '{print $2}') ] && [ $HEADERVAL != $(awk 'NR==1' $file | awk -F "$FILEDELIMITER" '{print $1}') ] && [ $TRAILERVAL == $(tail -1 $file | awk -F "$FILEDELIMITER" '{print $1}') ]
					then 
						echo "Error in source file header value. Please check the source file or parameter value."
						
				elif [ $BUSINESS_DATE_ARG == $(awk 'NR==1' $file | awk -F "$FILEDELIMITER" '{print $2}') ] && [ $HEADERVAL == $(awk 'NR==1' $file | awk -F "$FILEDELIMITER" '{print $1}') ] && [ $TRAILERVAL != $(tail -1 $file | awk -F "$FILEDELIMITER" '{print $1}') ]
					then
						echo "Error in source file trailer value. Please check the source file or parameter value."
						
				elif [ $BUSINESS_DATE_ARG != $(awk 'NR==1' $file | awk -F "$FILEDELIMITER" '{print $2}') ] && [ $HEADERVAL == $(awk 'NR==1' $file | awk -F "$FILEDELIMITER" '{print $1}') ] && [ $TRAILERVAL == $(tail -1 $file | awk -F "$FILEDELIMITER" '{print $1}') ]
					then
						echo "No source file was found for the given business date."
				fi
			done
			
			##Comparing source file's row count and trailer value
			MATCHEDFILEROWCNT=$(sed '1d;2d;$d' $matched_file | wc -l)
			ROWCNTVAL=$(tail -1 $file | awk -F "$FILEDELIMITER" '{print $2}')
			
			if [ $MATCHEDFILEROWCNT == $ROWCNTVAL ]
				then 
					echo "Row count and source trailer value matches."
					
					##Removing header and trailer values from source CSV file, if validation is successful and creating a detail file in the staging folder
					sed '1d;$d' $matched_file > $PARENT_DIR/$STAGE_DATA_DIR/$(basename $matched_file | cut -d. -f1)$TARGETFILEFORMAT
					
					echo $(basename $matched_file,$BUSINESS_DATE_ARG,$ROWCNTVAL) > $PARENT_DIR/$STAGE_DATA_DIR/$BUSINESS_DATE_ARG-$FILENAME.ctl
					
					echo "Preprocess SUCCESS: Detail and Control file placed in the staging folder."
					
					mv $PARENT_DIR/$SOURCE_DATA_DIR/$matched_file $PARENT_DIR/$ARCHIVE_DATA_DIR
					gzip $PARENT_DIR/$ARCHIVE_DATA_DIR/$matched_file
					
					echo "Archive SUCCESS: Source CSV file compressed in the archive folder."
					
			else
				echo "Row count and source trailer value does not match. Please check the source data."
				
			fi
			
	
	elif [[ $1 == [0-9][0-9][0-9][0-9]-[0-3][0-9]-[0-1][0-9] ]]	&& [[ $2 != *.txt ]]
		then 
			echo "FAILED: Parameter file passed in with wrong file format. Please provide a .txt file."
	
	elif [[ $1 != [0-9][0-9][0-9][0-9]-[0-3][0-9]-[0-1][0-9] ]]	&& [[ $2 == *.txt ]]
		then 
			echo "FAILED: Business Date provided in wrong format. Please provide the data in YYYY-MM-DD."
	fi
else
	echo "No arguments supplied - Please pass in business data DD-MM-YYYY format and parameter file in txt file format."
fi
