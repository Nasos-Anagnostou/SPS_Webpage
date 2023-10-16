import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from custom_funct import *
from dbconnection import *


######################################## THE LAYOUT OF THE PAGE ###########################################
#config of the page
st.set_page_config(page_title="Magnetic Measurements SPS Database 🧲📏", page_icon="🧲", layout="wide",
                   initial_sidebar_state="expanded", menu_items=None)

# add background
add_bg_from_url(title)
######################################## THE LAYOUT OF THE PAGE ###########################################

# Check if there is data in the DataFrame
if not df.empty:
    st.title("Measurement Information")
    
    # Access the basic information for the first row (iloc[0])
    basic_info = df.iloc[0]

    # Display the basic information
    st.subheader("Basic Measurement Info")
    st.write(f"Date Measured: {basic_info['MEASUREMENT_DATE']}")
    st.write(f"Measured Magnet: {basic_info['MAGNET_MEASURED']}")
    st.write(f"Reference Magnet: {basic_info['MAGNET_REFERENCE']}")
    st.write(f"Fluxmeter in Measured Magnet: {basic_info['FLUXMETER_MEASURED']}")
    st.write(f"Fluxmeter in Reference Magnet: {basic_info['FLUXMETER_REFERENCE']}")
else:
    st.warning("No measurement information found in the DataFrame.")


    # for a specific workorder,date, etc
# Display the data in a Streamlit table
st.write("Magnetic Measurements Data")
st.write(df)

st.title("Average Flux")
# Display the pivoted data
st.write(average_data)

st.title("Stddev Flux")
# Display the pivoted data
st.write(stddev_data)
