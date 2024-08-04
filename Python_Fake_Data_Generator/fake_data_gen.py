##---------------------------------------------------------------------------------------------------------------------------
## SCRIPT NAME      :     PYTHON - FAKE DATA GENERATOR USING SQL TABLE DDL
## PURPOSE          :     TO GENERATE MOCK OR FAKE DATA USING SQL TABLE DDL AND DATATYPES
## DEVELOPER NAME   :     SOORYA PRAKASH PARTHIBAN
## DATE             :     2023-11-25
##---------------------------------------------------------------------------------------------------------------------------

##---------------------------------------------------------------------------------------------------------------------------
## IMPORTING REQUIRED PYTHON LIBRARY

import numpy as np
import pandas as pd
import random
import string
import re
from datetime import datetime, timedelta
##---------------------------------------------------------------------------------------------------------------------------

##---------------------------------------------------------------------------------------------------------------------------
## Defining functions to extract SQL DDL from .txt file

def read_ddl_from_file(file_path):
    with open(file_path, 'r') as file:
        ddl = file.read()
    return ddl

def extract_columns_from_ddl(ddl):
    # Remove unnecessary SQL keywords
    ddl = re.sub(r'\b(?:CHARACTER SET|NOT CASESPECIFIC|UNICODE|NOT NULL|LATIN|FORMAT|YYYY-MM-DD)\b', '', ddl)

    # Extract column names and data types using regular expressions
    ##columns_info = re.findall(r'(\w+)\s+(\w+(?:\(\d+\))?)', ddl) 
    
    pattern = re.compile(r'(\w+)\s+(\w+(?:\(\d+(?:,\d+)?\))?(?:\s+FORMAT\s+\'[^\']*\'|)?)')

    columns_info = pattern.findall(ddl)

    # Create a DataFrame with the extracted information
    df = pd.DataFrame(columns_info, columns=['ColumnName', 'ColumnDataType'])
    
    return df

## Generating mockdata for widely used SQL Datatypes 
 
def generate_bigint():
    return random.randint(0, 922337203685477580)

def generate_integer():
    return random.randint(0, 2147483647)

def generate_smallInt():
    return random.randint(0, 32767)

def generate_byteInt():
    return random.randint(0, 127)

def generate_decimal(total_digits, decimal_points):
    return round(random.uniform(0, 10**total_digits), decimal_points)

def generate_character(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def generate_date():
    start_date = datetime(1970, 1, 1)
    end_date = datetime(2100, 12, 31)
    random_date = start_date + timedelta(days=random.randint(1, 365))
    return random_date.strftime('%Y-%m-%d')

def generate_timestamp():
    start_timestamp = datetime(1970, 1, 1)
    end_timestamp = datetime(2100, 12, 31, 23, 59, 59, 999999)
    random_timestamp = start_timestamp + timedelta(
        microseconds=random.randint(0, (end_timestamp - start_timestamp).microseconds)
    )
    return random_timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')#[:-3]


def generate_mock_data(row, num_rows):
    data = []

    for i in range(1, num_rows + 1):
        row_data = []
        for col_name, col_type in zip(row['ColumnName'], row['ColumnDataType']):
            if 'name' in col_name.lower():
                row_data.append(f'TEST_NAME_{i}')
            elif 'email' in col_name.lower():
                row_data.append(f'TEST_EMAIL_{i}@email.com')
            elif 'address' in col_name.lower():
                row_data.append(f'TEST_ADDR_{i}')
            elif 'VARCHAR' in col_type:
                length = int(col_type[col_type.index('(') + 1:col_type.index(')')])
                row_data.append(generate_character(length))
            elif 'CHAR' in col_type:
                length = int(col_type[col_type.index('(') + 1:col_type.index(')')])
                row_data.append(generate_character(length))
            elif 'INTEGER' in col_type:
                row_data.append(generate_integer())
            elif 'BIGINT' in col_type:
                row_data.append(generate_bigint())
            elif 'DATE' in col_type:
                row_data.append(generate_date())
            elif 'TIMESTAMP' in col_type:
                row_data.append(generate_timestamp())
            # elif 'DECIMAL' in col_type or 'NUMBER' in col_type:
            #     # Extract total digits and decimal points from the type
            #     match = re.match(r'\D*(\d+)(?:\D*(\d+))?\D*', col_type)
            #     total_digits = int(match.group(1))
            #     decimal_points = int(match.group(2)) if match.group(2) else 0
            #     row_data.append(generate_decimal(total_digits, decimal_points))
            elif 'DECIMAL' in col_type or 'NUMBER' in col_type:
                # Extract total digits and decimal points from the type
                match = re.match(r'\D*(\d+)(?:\D*(\d+))?\D*', col_type)
                total_digits = int(match.group(1))
                decimal_points = int(match.group(2)) if match.group(2) else 0

                if total_digits <= 3:
                    row_data.append(generate_byteInt())
                elif total_digits <= 5:
                    row_data.append(generate_smallInt())
                elif total_digits <= 10:
                    row_data.append(generate_integer())
                elif total_digits <= 19:
                    row_data.append(generate_bigint())
                else:
                    row_data.append(generate_bigint())

                # Round the generated value to the specified decimal points
                if decimal_points > 0:
                    row_data[-1] = round(row_data[-1], decimal_points)
            else:
                raise ValueError(f"Unsupported data type: {col_type}")

        data.append(row_data)

    return data
##---------------------------------------------------------------------------------------------------------------------------

## MAIN PROGRAM

def main():
    
    ddl_file_path = 'ddl.txt'

    ddl = read_ddl_from_file(ddl_file_path)

    result_df = extract_columns_from_ddl(ddl)
    
    print(result_df)
    
    num_rows = int(input("Enter the number of rows to generate: "))

    # Generate mock data
    mock_data = generate_mock_data(result_df, num_rows)
    
    # Create a new DataFrame with mock data
    mock_df = pd.DataFrame(mock_data, columns=result_df['ColumnName'])

    # Print the generated mock data
    print(mock_df)
    
    mock_df.to_csv('mock_cust_data.csv')
    
if __name__ == "__main__":
    main()
    
## EOP    
##---------------------------------------------------------------------------------------------------------------------------