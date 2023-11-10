import cx_Oracle
import pandas as pd
from custom_funct import modify_string
from datetime import datetime


def connect_to_oracle():
    oracle_username = '***REMOVED***'
    oracle_password = '***REMOVED***'    
    oracle_host = '***REMOVED***'
    oracle_port = '***REMOVED***'
    oracle_service_name = '***REMOVED***'

    try:
        connection = cx_Oracle.connect(
            f"{oracle_username}/{oracle_password}@{oracle_host}:{oracle_port}/{oracle_service_name}")
        return connection
    except cx_Oracle.Error as error:
        print(f"Error: {error}")
        return None


def execute_query(connection):
    cursor = connection.cursor()

    try:
        # comment only for the dev of the app
        cursor.execute("ALTER TABLE SPS_SEP_COIL_ACQ NOCACHE")
        cursor.execute("SELECT * FROM SPS_SEP_COIL_ACQ")
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=column_names)

        # convert workorder to int
        df['WORKORDER_N'] = df['WORKORDER_N'].fillna(0).astype(int)
        # Convert the 'MEASUREMENT_DATE' column to datetime format
        df['MEASUREMENT_DATE'] = pd.to_datetime(df['MEASUREMENT_DATE'], format='%Y%m%d_%H%M%S', errors='coerce')
        # Convert the second date format
        df['MEASUREMENT_DATE'] = df['MEASUREMENT_DATE'].combine_first(pd.to_datetime(df['MEASUREMENT_DATE'], format='%Y-%m-%d', errors='coerce'))
        # Format the 'MEASUREMENT_DATE' column as required
        df['MEASUREMENT_DATE'] = df['MEASUREMENT_DATE'].dt.strftime("%H:%M   %d/%m/%Y")

        df['MAGNET_MEASURED'] = df['MAGNET_MEASURED'].apply(modify_string)
        df['MAGNET_REFERENCE'] = df['MAGNET_REFERENCE'].apply(modify_string)
        df['FLUXMETER_MEASURED'] = df['FLUXMETER_MEASURED'].apply(modify_string,)
        df['FLUXMETER_REFERENCE'] = df['FLUXMETER_REFERENCE'].apply(modify_string)

        return df
    finally:
        cursor.close()

# initialise the connection
try:
    cx_Oracle.init_oracle_client("C:\Oracle\instantclient_12_2")
except:
    print("It is already initialised")

# Initialize the database connection
db_connection = connect_to_oracle()
df = execute_query(db_connection)

# Close the connection
db_connection.close()        


print("\n###############################     EXECUTED     ###############################\n")
