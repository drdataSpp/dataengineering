# Python ELT script to load CSV file into MS SQL Server Table

This script is designed to load data from a CSV file into an MS SQL Server database table. It performs various checks, including header row count, business date comparison, and target table existence, to ensure data integrity and reliability.

## Developer

- Name: Soorya Prakash Parthiban
- GitHub: drdataSpp

## Date

27 May, 2023

## Script Parameter

This Python script requires a parameter file to be passed when calling it. The parameter file should be in JSON format and contain necessary configuration values for the script to run.

## Change History

- **V1** (2023-05-27): Pushed draft files with Python libraries.
- **V2** (2023-05-27): Added Python code to check the existence of the source CSV data file and parameter files & folders.
- **V3** (2023-05-28): Added a LOGS folder to create .txt logs on failure. Implemented row count checks and business date checks.
- **V4** (2023-05-28): Added code to create a processed data frame and establish an SQL Server connection using pyodbc.
- **V4.1** (2023-05-28): Added SQL Truncate and Load Queries.
- **V4.2** (2023-05-28): Added ROLLBACK & COMMIT if the correct data is inserted into the Target Table.
- **V4.3** (2023-05-28): Added an archive feature when the table is successfully loaded.
- **V5** (2023-05-30): Removed .txt Parameter Sets and added JSON Parameter sets.
- **V5.1** (2023-05-30): Added an IF TABLE EXISTS clause before loading data.
- **V5.2** (2023-05-30): Removed hardcoded values - now picking values from the JSON Parameter file.
- **V6** (2023-06-02): Updated folder and file names.
- **V6.1** (2023-06-02): Added a feature to pass a parameter file when calling the Python script.
- **V6.2** (2023-06-02): Generating success message logs if data is loaded correctly.

## Installation

To run this script, follow these steps:

1. Install the required Python libraries. You can use the following command to install them:

   ```shell
   pip install numpy pandas pyodbc
   ```

2. Prepare a JSON parameter file with the required values. The parameter file should contain the following fields:

```json
{
  "PROJECT_PARENT_PATH": "<parent_folder_path>",
  "FOLDER_NAME": "<source_folder_name>",
  "FILE_NAME": "<source_file_name>",
  "SQL_SERVER_NAME": "<sql_server_name>",
  "SQL_DATABASE_NAME": "<database_name>",
  "SQL_TARGET_TABLE": "<table_name>"
}
```

3. Execute the script by running the following command:

   ```shell
   Python Terminal command: python script_name.py parameter_file.json
   GIT BASH command       : ./run_pelt_script.sh parameter_file.json
   ```

## Logical Flowchart

<img src="https://github.com/drdataSpp/dataengineering/blob/master/Python_ELT_script/Images/PELT_Logical_Img.png">

## Usage

Before running the script, ensure that you have the following:

- The source CSV data file exists in the specified folder.
- The parameter file is present in the correct location and follows the JSON format.

The script will perform checks and load the data into the specified SQL Server target table if all conditions are met.

## Script execution examples

### Success Message example
<img src="https://github.com/drdataSpp/dataengineering/blob/master/Python_ELT_script/Images/success_message.png">

### SQL Server Target Table
<img src="https://github.com/drdataSpp/dataengineering/blob/master/Python_ELT_script/Images/success_sql.png">

### Failure Message example
<img src="https://github.com/drdataSpp/dataengineering/blob/master/Python_ELT_script/Images/error_message.png">

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please feel free to submit a pull request or open an issue.

## Credits

Credits to ChatGPT for generating this README file 😉 and to all informative youtubers 🧑🏽‍💻.
