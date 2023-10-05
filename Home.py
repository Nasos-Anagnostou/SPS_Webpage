import streamlit as st

from streamlit_extras.switch_page_button import switch_page
from custom_funct import add_logo

from dbconnection import *


####################################################### INITIALIZATION ###############################################################
# init the styles of fonts
homepage = '<p style="font-family:Arial Black; color:black; font-size: 200%;"><strong>Homepage 🏠</strong></p>'
comp = '<p style="font-family:Arial Black; color:#262730; font-size: 150%;"><strong>Chose competition🏆</strong></p>'
title = '<p style="font-family:Arial Black; color:white; font-size: 300%; text-align: center;">Magnetic Measurements SPS Database 🧲📏</p>'


######################################## THE LAYOUT OF THE PAGE ###########################################
#config of the page
st.set_page_config(page_title="Magnetic Measurements SPS Database 🧲📏", page_icon="🧲", layout="wide",
                   initial_sidebar_state="expanded", menu_items=None)

# insert empty spaces
def empty_line(lines_number):
    for num in range(lines_number):
        st.write("\n")

# set background wallpaper and subtitle title & sidebar name
def add_bg_from_url():
    st.markdown(
        f"""
       <style>
       .stApp {{
       background-image: url("https://static.vecteezy.com/system/resources/previews/021/565/019/non_2x/minimalist-abstract-background-design-smooth-and-clean-subtle-background-vector.jpg");
       background-attachment: fixed;
       background-size: cover
       }}
       </style>
       """,
        unsafe_allow_html=True
    )
    add_logo("images//CERN-Logo.png")
    st.sidebar.markdown("# Magnetic Measurements  🧲 SPS Database 🖥️")
    # set the homepage style
    st.markdown(title, unsafe_allow_html=True)
    empty_line(4)

add_bg_from_url()




# Create Streamlit app
st.title('Magnetic Measurements Dashboard')

# Display the data in a Streamlit table
st.write("Magnetic Measurements Data")
st.write(df)

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