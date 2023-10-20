import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from custom_funct import *
from dbconnection import df,average_data,stddev_data
import pandas as pd


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

    # # Display the basic information
    # st.subheader("Basic Measurement Info")
    # st.write(f"Workorder number: {basic_info['WORKORDER_N']}")
    # st.write(f"Date Measured: {basic_info['MEASUREMENT_DATE']}")
    # st.write(f"{basic_info['MAGNET_MEASURED']}")
    # st.write(f"{basic_info['MAGNET_REFERENCE']}")
    # st.write(f"{basic_info['FLUXMETER_MEASURED']}")
    # st.write(f"{basic_info['FLUXMETER_REFERENCE']}")
    # Display the basic information in a horizontal layout
    # Display the basic information in a table
    st.subheader("Basic Measurement Info")

    # Create a table to display the information
    basic_info_table = pd.DataFrame(
        {
            'Workorder number': [basic_info['WORKORDER_N']],
            'Date Measured': [basic_info['MEASUREMENT_DATE']],
            'Magnet Measured': [basic_info['MAGNET_MEASURED']],
            'Magnet Reference': [basic_info['MAGNET_REFERENCE']],
            'Fluxmeter Measured': [basic_info['FLUXMETER_MEASURED']],
            'Fluxmeter Reference': [basic_info['FLUXMETER_REFERENCE']]
        }
    )
    st.table(basic_info_table)

else:
    st.warning("No measurement information found in the DataFrame.")


 # Display the data in a Streamlit table
st.title("Magnetic Measurements Data")
df = df.iloc[:, 7:]
st.dataframe(df, width=1200)

# Create two columns for arranging items side by side
left_column, right_column = st.columns(2)


with left_column:
    # for a specific workorder,date, etc 
    st.title("Average Flux")
    # Display the pivoted data
    st.dataframe(average_data)      


with right_column:
    st.title("Stddev Flux")
    # Display the pivoted data
    st.dataframe(stddev_data)