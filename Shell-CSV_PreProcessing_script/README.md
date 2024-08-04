# Shell Script: Pre-processing of CSV file into detail and control file
*This shell script is designed for pre-processing a source CSV file by creating detail and control files. It performs various validations and checks to ensure the integrity of the data.* 

## What's the purpose of this project?
In the context of ETL (Extract, Transform, Load) processes, the detail and control files play important roles in managing data movement and ensuring data integrity. Here's an explanation of each file:

1. Detail File:
   - Purpose: The detail file contains the actual data extracted from the source system, transformed (if required), and ready for loading into the target system or data warehouse.
   - Content: It typically consists of the extracted rows from the source file, after applying any necessary transformations or cleansing operations.
   - Format: The format of the detail file may vary depending on the specific requirements of the target system or data warehouse. It can be a CSV file, a delimited text file, or any other structured format.

2. Control File:
   - Purpose: The control file provides metadata and control information about the data being processed in the ETL pipeline. It helps ensure the accuracy, completeness, and consistency of the data.
   - Content: The control file includes details such as the business date, source file name, row count, data validation results, and other relevant information for auditing and monitoring purposes.
   - Format: The control file is typically a structured text file, often in a key-value pair or tabular format. It may use a specific syntax or follow a predefined schema.

The detail file and control file work together to facilitate the ETL process. After the source data is pre-processed and transformed, the detail file is created and stored in a staging area. Simultaneously, the control file is generated to capture essential metadata about the data and its processing. This allows for traceability and error handling during the subsequent loading phase.

The control file provides information like the business date and row count, which can be used for reconciling data, validating completeness, and ensuring consistency between the source and target systems. It helps monitor data quality and track any issues or discrepancies that may occur during the ETL process.

Both the detail file and control file are crucial components in ETL workflows, as they enable data integration and data integrity checks, and provide an audit trail for data processing activities.

## Developer

Soorya Parthiban

## Date

2023-07-08

## Required Parameters

1. Business Date (YYYY-MM-DD)
2. Parameter File (in .txt format)

## Description

The script performs the following steps:

1. Validates the provided parameters to ensure the correct format.
2. Retrieves the necessary parameter values from the parameter file.
3. Searches for the source file matching the business date and validates the header and trailer values.
4. Compares the row count of the source file with the trailer value.
5. If the validation is successful, removes the header and trailer values from the source file and creates a detail file in the staging folder.
6. Creates a control file with the filename, business date, and row count information in the staging folder.
7. Moves the matched source file to the archive folder and compresses it.
8. Displays success or error messages based on the execution.

## Usage

```bash
./preprocess.sh <business_date> <parameter_file.txt>
```

Note: Replace `<business_date>` with the actual business date in YYYY-MM-DD format and `<parameter_file.txt>` with the parameter file in .txt format.

Example:

```bash
./preprocess.sh 2023-07-01 parameters.txt
```

Please ensure that the script has the necessary permissions to execute.

## File Structure

The script assumes the following file structure:

```
|-- preprocess.sh
|-- parameter
|   |-- parameters.txt
|-- source_data
|   |-- source_file1.csv
|   |-- source_file2.csv
|-- archive_data
|   |-- source_file.csv.gz
|-- stage_data
|   |-- detail_file.csv
|   |-- control_file.ctl
```

You can modify the `PARENT_DIR` variable in the script to match your file structure.

## Inspiration & Credits

This [AWS documentation](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/orchestrate-an-etl-pipeline-with-validation-transformation-and-partitioning-using-aws-step-functions.html) was the inspiration behind this script. Thanks a ton to #ChatGPT for generating this README file 😉.

## End notes
Thanks for your time and please feel free to provide any feedback or suggestions 🙌.
