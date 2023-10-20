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

# Create Streamlit app
st.title('Magnetic Measurements Dashboard')


# choose data based on workorder and date and move to raw data page
st.write("Choose wich workorder you want to see")

#input
