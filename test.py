import streamlit as st
import cx_Oracle
import pandas as pd

# # This is the path to the ORACLE client files
# lib_dir = r"C:\Oracle\instantclient_12_2"
# cx_Oracle.init_oracle_client(lib_dir)

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

# Define the SQL query to fetch all columns from the table
sql_query = "SELECT * FROM SPS_SEP_COIL_ACQ"

# Create a cursor
cursor = connection.cursor()

try:
    # Execute the query
    cursor.execute(sql_query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Get column names
    column_names = [desc[0] for desc in cursor.description]

    # Create a Pandas DataFrame
    df = pd.DataFrame(rows, columns=column_names)

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()


# Create Streamlit app
st.title('Magnetic Measurements Dashboard')

# Display the data in a Streamlit table
st.write("Magnetic Measurements Data")
st.table(df)
