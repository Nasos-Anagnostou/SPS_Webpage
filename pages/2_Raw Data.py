import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.row import row 
from custom_funct import *
from Home_Page import *
import pandas as pd


# Initialization of the st.session variables
if "magnettype" not in st.session_state:
    st.session_state['magnettype'] = ""

if "coilMeasResistance" not in st.session_state:
    st.session_state['coilMeasResistance'] = {}

if "afcorrlist" not in st.session_state:
    st.session_state['afcorrlist'] = []

if "current_applied" not in st.session_state:
    st.session_state['current_applied'] = []

if "coils_used" not in st.session_state:
    st.session_state['coils_used'] = []

if "kRefCoil" not in st.session_state:
    st.session_state['kRefCoil'] = 0

if "kMeasCoil" not in st.session_state:
    st.session_state['kMeasCoil'] = None

if "avg_data" not in st.session_state:
    st.session_state['avg_data'] = None

if "impedance_img" not in st.session_state:
    st.session_state['impedance_img'] = ""

if "flag" not in st.session_state:
    st.session_state['flag'] = False

######################################## THE LAYOUT OF THE PAGE ###########################################
#config of the page
st.set_page_config(page_title="Magnetic Measurements SPS Database 🧲📏", page_icon="🧲", layout="wide",
                   initial_sidebar_state="expanded", menu_items=None)
# add background
add_bg_from_url(title)
######################################## THE LAYOUT OF THE PAGE ###########################################

# Check if there is data in the DataFrame
if st.session_state.flag:   
    # get the session state variables
    current_applied = st.session_state.current_applied
    coils_used = st.session_state.coils_used
    impedance_img = st.session_state.impedance_img
    kRefCoil = st.session_state.kRefCoil
    kMeasCoil = st.session_state.kMeasCoil
    avg_data = st.session_state.avg_data
    coilMeasResistance = st.session_state.coilMeasResistance


    # Define a radio button to select input method
    input_method = st.radio("Select Input Method", ["Default Values", "Custom Input"], horizontal= True)
    # Create two columns for arranging items side by side
    left_column, right_column = st.columns(2)
    
    # If the user selects "Custom Input," collect user inputs
    if input_method == "Custom Input":
        with left_column:
            with st.expander("Custom Coil Resistances"):
                for coil_name in coilMeasResistance:
                    coilMeasResistance[coil_name] = st.number_input(f"{coil_name} Resistance", 0.0)
            
        with right_column:
            st.session_state.afcorrlist = show_results(current_applied, avg_data, coilMeasResistance, coils_used)
            #     # Create a "Show Results" button
            #     if st.button("Show Results"):
            #         # Display the selected values
                    
    else:
        with left_column:
            st.session_state.afcorrlist = show_results(current_applied, avg_data, coilMeasResistance, coils_used)

        with right_column:
            st.header("Impedance of every coil")
            st.image(impedance_img)
            st.image("images/Correction_image.png")
else:
    empty_line(3)
    row1 = row([0.7, 0.6], vertical_align="bottom")
    row1.subheader("Please choose first the date or the workorder of the measurement.")
    if row1.button("Back to Home Page 🏠"):
        switch_page("Raw_data")




