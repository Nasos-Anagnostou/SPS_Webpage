import cx_Oracle
import pandas as pd

def initialize_oracle_client(lib_dir):
    cx_Oracle.init_oracle_client(lib_dir)

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
        print(df)
        return df
    finally:
        cursor.close()


lib_dir = r"C:\Oracle\instantclient_12_2"
#initialize_oracle_client(lib_dir)


# Initialize the database connection
db_connection = connect_to_oracle()
df = execute_query(db_connection)

# cursor = db_connection.cursor()
# sql_query = "SELECT * FROM SPS_SEP_COIL_ACQ"
# cursor.execute(sql_query)

# Data processing and analysis here
# Average Flux of the coils for different current applied
avg_data = df.pivot_table(index='CURRENT_APPLIED', values=['R5', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9'], aggfunc='mean')
average_data = avg_data.style.format("{:.6f}")

# Stddev Flux of the coils for different current applied
grouped_data = df.groupby('CURRENT_APPLIED')[['R5', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9']].std()
pivoted_data = grouped_data.reset_index().pivot_table(index='CURRENT_APPLIED')
stddev_data = pivoted_data.style.format("{:.6f}")


# Close the connection
db_connection.close()        


print("\n###############################     EXECUTED     ###############################\n")
