import cx_Oracle

# This is the path to the ORACLE client files
lib_dir = r"C:\Oracle\instantclient_12_2"
cx_Oracle.init_oracle_client(lib_dir)


# Define Oracle database connection parameters
oracle_username = '***REMOVED***'
oracle_password = '***REMOVED***'
oracle_host = '***REMOVED***'
oracle_port = '***REMOVED***'
oracle_service_name = '***REMOVED***'

# Establish a connection
connection = cx_Oracle.connect(
    f"{oracle_username}/{oracle_password}@{oracle_host}:{oracle_port}/{oracle_service_name}"
)


# Create a cursor for executing SQL queries
cursor = connection.cursor()

# Specify the table name
table_name = "SPS_SEP_COIL_ACQ"

# Fetch all column names from the table
query = f"SELECT column_name FROM all_tab_columns WHERE table_name = '{table_name}'"
cursor.execute(query)

# Retrieve the column names as a list
columns = [row[0] for row in cursor.fetchall()]

# Fetch the data
measurements_data = cursor.fetchall()


# Close the cursor and connection
cursor.close()
connection.close()

# Print the column names
for column in columns:
    print(column)

