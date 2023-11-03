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
df = df.rename(columns={'CURRENT_APPLIED':'Current'})

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

# Data processing and analysis here
# Average Flux of the coils for different current applied
avg_data = df.pivot_table(index='Current', values=['R5', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9'], aggfunc='mean')

average_data = avg_data.style.format("{:.6f}")

# Stddev Flux of the coils for different current applied
grouped_data = df.groupby('Current')[['R5', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9']].std()
pivoted_data = grouped_data.reset_index().pivot_table(index='Current')
stddev_data = pivoted_data.style.format("{:.6f}")


# Close the connection
db_connection.close()        


print("\n###############################     EXECUTED     ###############################\n")
