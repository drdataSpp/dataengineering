#######################################################################################

## PROJECT NAME     : Python ELT script to load CSV file (Flat file source) into MS SQL Server Database
## Developer        : Soorya Prakash Parthiban
## GitHub           : drdataSpp
## Date             : 27 May, 2023
## Description      : This PELT script checks the header row count of the CSV file, compares with the system date and file's business date, if both matches then the data is loaded into the SQL Server target table.
## Script Parameter : This python script needs a Parameter file to be passed when calling ONLY in JSON Format 


## Change history

## V1   - 2023-05-27 - Pushed draft files with python libraries
## V2   - 2023-05-27 - Added python code to check if the source csv data file exists and parameter files & folders 
## V3   - 2023-05-28 - Added LOGS folder to create .txt logs on failure. Added row count checks and business date checks
## V4   - 2023-05-28 - Added code to create processed data frame & established SQL Server connection using pyodbc
## V4.1 - 2023-05-28 - Added SQL Truncate and Load Queries
## V4.2 - 2023-05-28 - Added ROLLBACK & COMMIT if correct data is inserted into the Target Table 
## V4.3 - 2023-05-28 - Added archive feature when the table is successfully loaded
## V5   - 2023-05-30 - Removed .txt Parameter Sets and added JSON Paramater sets
## V5.1 - 2023-05-30 - Added IF TABLE EXISTS Clause before loading data
## V5.2 - 2023-05-30 - Added Removed hardcoded values - Picks from JSON Parameter file
## V6   - 2023-06-02 - Updated folder and file names
## V6.1 - 2023-06-02 - Added feature to pass in a parameter file when calling the python script
## V6.2 - 2023-06-02 - Generating success message logs, if data is loaded is correctly
 
#######################################################################################

## Importing python libraries
import sys
import datetime
from datetime import date
import os.path
import json
import numpy as np
import pandas as pd
import pyodbc as pySQLConn

##PARAMETER FILE PATH

## Using JSON files to get parameter values
    ### With the help of a paramater file, we can make changes easily without editing the actual source code)
PARAM_FILE_NAME = sys.argv[1] ##Getting Parameter file value from Bash script
PARAM_FILE = "D:/001_Data/data_projects/data_projects/Python ELT/Job Parameters/" + PARAM_FILE_NAME

isParamFIleExists = os.path.exists(PARAM_FILE)

if isParamFIleExists == True:

    with open(PARAM_FILE, 'r') as j:
        CREDIT_SCORE_LOAD_PARAMS = json.loads(j.read())

    ## Defining Project Path
    PROJECT_PARENT_PATH = CREDIT_SCORE_LOAD_PARAMS['PROJECT_PARENT_PATH'] 

    ## Defining Business Date
    ## FORMAT: DD/MM/YYYY
    BUSINESS_DATE = datetime.date.today().strftime("%d") + "/" + datetime.date.today().strftime("%m") + "/" + datetime.date.today().strftime("%Y")

    ## Clearing old logs from the LOGS folder before running the script
    filelist = [ f for f in os.listdir(PROJECT_PARENT_PATH + "/logs") if f.endswith(".txt") ]
    for f in filelist:
        os.remove(os.path.join(PROJECT_PARENT_PATH + "/logs", f))
        
    ## Clearing pre-processed csv files from the processed data folder before running the script
    filelist = [ f for f in os.listdir(PROJECT_PARENT_PATH + "/processed data") if f.endswith(".csv") ]
    for f in filelist:
        os.remove(os.path.join(PROJECT_PARENT_PATH + "/processed data", f))

    ## Check if source data file exists
        
    ## Variables for file path & file name
    SOURCE_DATA_FOLDER_NAME = CREDIT_SCORE_LOAD_PARAMS['FOLDER_NAME']
    FILE_NAME               = CREDIT_SCORE_LOAD_PARAMS['FILE_NAME']
    
    isSourceDataExists = os.path.exists(PROJECT_PARENT_PATH + "/" + SOURCE_DATA_FOLDER_NAME + "/" + FILE_NAME)

    if isSourceDataExists == True:
        ## Importing Raw CSV file and Pre-Processing
        raw_df = pd.read_csv(PROJECT_PARENT_PATH + "/" + SOURCE_DATA_FOLDER_NAME + "/" + FILE_NAME, header=0)
        FILE_BUSINESS_DATE = raw_df.columns.tolist()[1]
        
        ## Business Date comparision
        
        if BUSINESS_DATE == FILE_BUSINESS_DATE:
            
            ## If program's business date matches with source file's business date then check for row count with header row count value 
            SOURCE_FILE_ROW_COUNT = int(raw_df.columns.tolist()[0])
            DF_ROW_COUNT          = int(raw_df.shape[0])
            
            if SOURCE_FILE_ROW_COUNT == DF_ROW_COUNT:
                
                ## If all three checkpoints are cleared, we will create a data frame without the header values and establish SQL Server Database connection
                
                ## Create data frame excluding the header count values for loading into the Database table
                processed_df = pd.read_csv(PROJECT_PARENT_PATH + "/" + SOURCE_DATA_FOLDER_NAME + "/" + FILE_NAME, header=1)
            
                processed_df.to_csv(PROJECT_PARENT_PATH + "/processed data/" + datetime.date.today().strftime("%d") + "-" + datetime.date.today().strftime("%m") + "-" + datetime.date.today().strftime("%Y") + "_" + FILE_NAME)
                
                
                ## SQL Server connection
                
                ## Getting SQL Connection values from PARAM file
                SQL_SERVER_NAME = CREDIT_SCORE_LOAD_PARAMS['SQL_SERVER_NAME']
                SQL_TGT_DB = CREDIT_SCORE_LOAD_PARAMS['SQL_DATABASE_NAME']
                SQL_TGT_TABLE = CREDIT_SCORE_LOAD_PARAMS['SQL_TARGET_TABLE']
                                                
                sqlConn = pySQLConn.connect("Driver={SQL Server};"
                        "Server=" + SQL_SERVER_NAME + ";"
                        "Database=" + SQL_TGT_DB + ";"
                        "Trusted_Connection=yes;")
                
                cursor = sqlConn.cursor()

                ##Check if Target Table exists in SQL Server

                isTableExistsSQL = """ IF EXISTS (SELECT 1 
                                FROM INFORMATION_SCHEMA.TABLES 
                                WHERE TABLE_CATALOG = ?
                                    AND TABLE_NAME=?) 
                        SELECT 1 AS RESULT ELSE SELECT 0 AS RESULT;"""
                    
                isTableExists = pd.read_sql_query(isTableExistsSQL, sqlConn, params=[SQL_TGT_DB, SQL_TGT_TABLE]) ##params are used to pass in the table and DB names to be checked
                isTableExists = int(isTableExists['RESULT']) ##Binary output: 1 if Target table exists, 0 if not
                
                if isTableExists == 1:
                    ## Truncate table before loading
                    cursor.execute("USE " + SQL_TGT_DB + ";")
                    cursor.execute("DELETE FROM " + SQL_TGT_TABLE + ";")

                    # Insert Dataframe into SQL Server:
                    for index, row in processed_df.iterrows():
                        cursor.execute("INSERT INTO " + SQL_TGT_TABLE + " (Age ,Gender ,Income ,Education ,MaritalStatus ,NumberOfChildren ,HomeOwnership ,CreditScore) values(?,?,?,?,?,?,?,?)", row.Age, row.Gender, row.Income, row.Education, row.MaritalStatus, row.NumberOfChildren, row.HomeOwnership, row.CreditScore)
                        
                    SQL_TABLE_COUNT = int(pd.read_sql("SELECT COUNT(*) FROM " + SQL_TGT_TABLE + ";", sqlConn).iloc[0])
                    SOURCE_DATA_COUNT = int(processed_df.count(axis=0)[1])

                    if SQL_TABLE_COUNT == SOURCE_DATA_COUNT:
                        sqlConn.commit()
                        processed_df.to_csv(PROJECT_PARENT_PATH + "/archive/" + datetime.date.today().strftime("%d") + "-" + datetime.date.today().strftime("%m") + "-" + datetime.date.today().strftime("%Y") + "_" + FILE_NAME + "_" + FILE_NAME + ".gz", compression='gzip')
                        
                        SUCCESS_MESSAGE = "Load process completed sucessfully. Loaded " + str(SOURCE_DATA_COUNT) + " rows into " + str(SQL_TGT_TABLE) + " SQL Server table."
                        SUCCESS_MESSAGE_FILENAME = "SuccessMessage_" + str(datetime.datetime.now().date()) + "_"+ datetime.datetime.now().strftime("%H") + "_"+ datetime.datetime.now().strftime("%M") + "_"+ datetime.datetime.now().strftime("%S") + ".txt"
                        
                        with open(PROJECT_PARENT_PATH + "/logs/" + SUCCESS_MESSAGE_FILENAME, 'w') as f:
                            f.write(SUCCESS_MESSAGE)

                    else:
                        sqlConn.rollback()
                            
                    sqlConn.close()
                    sys.exit()
                
                else:
                    MISSING_TABLE_ERROR = "FAILED in STEP 5: SQL Target Table is missing. Please check both Target Table and Database and retry." 
                    MISSING_TABLE_ERROR_FILENAME = "MissingTargetTableError_" + str(datetime.datetime.now().date()) + "_"+ datetime.datetime.now().strftime("%H") + "_"+ datetime.datetime.now().strftime("%M") + "_"+ datetime.datetime.now().strftime("%S") + ".txt"
                
                    with open(PROJECT_PARENT_PATH + "/logs/" + MISSING_TABLE_ERROR_FILENAME, 'w') as f:
                        f.write(MISSING_TABLE_ERROR)
                        
                    sys.exit()
    
            else:
                ROW_COUNT_ERROR = "FAILED in STEP 4: Source file Header Row Count " + str(SOURCE_FILE_ROW_COUNT) + " and Data Count "+ str(DF_ROW_COUNT) + " doesn't match" 
                ROW_COUNT_ERROR_FILENAME = "RowCountError_" + str(datetime.datetime.now().date()) + "_"+ datetime.datetime.now().strftime("%H") + "_"+ datetime.datetime.now().strftime("%M") + "_"+ datetime.datetime.now().strftime("%S") + ".txt"
                
                with open(PROJECT_PARENT_PATH + "/logs/" + ROW_COUNT_ERROR_FILENAME, 'w') as f:
                    f.write(ROW_COUNT_ERROR)
                    
                sys.exit()
            
        else:
            BUSINESS_DATE_ERROR = "FAILED in STEP 3: Source file Business Date and Program's Business Date doesn't match"
            BUSINESS_DATE_ERROR_FILENAME = "BusinessDateError_" + str(datetime.datetime.now().date()) + "_"+ datetime.datetime.now().strftime("%H") + "_"+ datetime.datetime.now().strftime("%M") + "_"+ datetime.datetime.now().strftime("%S") + ".txt"
            
            with open(PROJECT_PARENT_PATH + "/logs/" + BUSINESS_DATE_ERROR_FILENAME, 'w') as f:
                f.write(BUSINESS_DATE_ERROR)
                
            sys.exit()
            
    else:
        FILE_MISSING_ERROR = "FAILED in STEP 2: Source file doesn't exist in the raw_data folder"
        FILE_MISSING_ERROR_FILENAME = "SourceFileMissingError_" + str(datetime.datetime.now().date()) + "_"+ datetime.datetime.now().strftime("%H") + "_"+ datetime.datetime.now().strftime("%M") + "_"+ datetime.datetime.now().strftime("%S") + ".txt"
            
        with open(PROJECT_PARENT_PATH + "/logs/" + FILE_MISSING_ERROR_FILENAME, 'w') as f:
            f.write(FILE_MISSING_ERROR)
        
        sys.exit()
        
else:
    PARAM_FILE_MISSING_ERROR = "FAILED in STEP 1: Param file doesn't exist in the ../Job Parameters folder or wrong parameter file name/ file format was passed in while calling the script"
    PARAM_FILE_MISSING_ERROR_FILENAME = "ParamFileMissingError_" + str(datetime.datetime.now().date()) + "_"+ datetime.datetime.now().strftime("%H") + "_"+ datetime.datetime.now().strftime("%M") + "_"+ datetime.datetime.now().strftime("%S") + ".txt"
            
    with open("D:/001_Data/data_projects/data_projects/Python ELT/" + "/logs/" + PARAM_FILE_MISSING_ERROR_FILENAME, 'w') as f:
        f.write(PARAM_FILE_MISSING_ERROR)
        
    sys.exit()
