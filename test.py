import streamlit as st
from dbconnection import *

# Create Streamlit app
st.title('Magnetic Measurements Dashboard')

# Display the data in a Streamlit table
st.write("Magnetic Measurements Data")
st.table(df)

st.title("Average Flux")
# Display the pivoted data
st.write(average_data)

st.title("Stddev Flux")
# Display the pivoted data
st.write(stddev_data)

# # Check if there is data in the DataFrame
# if not df.empty:
#     st.title("Measurement Information")
    
#     # Access the basic information for the first row (iloc[0])
#     basic_info = df.iloc[0]

#     # Display the basic information
#     st.subheader("Basic Measurement Info")
#     st.write(f"Date Measured: {basic_info['MEASUREMENT_DATE']}")
#     st.write(f"Measured Magnet: {basic_info['MAGNET_MEASURED']}")
#     st.write(f"Reference Magnet: {basic_info['MAGNET_REFERENCE']}")
#     st.write(f"Fluxmeter in Measured Magnet: {basic_info['FLUXMETER_MEASURED']}")
#     st.write(f"Fluxmeter in Reference Magnet: {basic_info['FLUXMETER_REFERENCE']}")
# else:
#     st.warning("No measurement information found in the DataFrame.")