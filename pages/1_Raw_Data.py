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
    st.write(f"Workorder number: {basic_info['WORKORDER_N']}")
    st.write(f"Date Measured: {basic_info['MEASUREMENT_DATE']}")
    st.write(f"{basic_info['MAGNET_MEASURED']}")
    st.write(f"{basic_info['MAGNET_REFERENCE']}")
    st.write(f"{basic_info['FLUXMETER_MEASURED']}")
    st.write(f"{basic_info['FLUXMETER_REFERENCE']}")
else:
    st.warning("No measurement information found in the DataFrame.")


# for a specific workorder,date, etc
# Display the data in a Streamlit table
st.write("Magnetic Measurements Data")
df = df.iloc[:, 7:]
st.dataframe(df, width=1200)

st.title("Average Flux")
# Display the pivoted data
st.write(average_data)

st.title("Stddev Flux")
# Display the pivoted data
st.write(stddev_data)
