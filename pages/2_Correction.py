import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from custom_funct import *
from dbconnection import *
import pandas as pd


# Initialization of the st.session variables
if "magnettype" not in st.session_state:
    st.session_state['magnettype'] = ""

if "afcorrlist" not in st.session_state:
    st.session_state['afcorrlist'] = []

if "dtframe" not in st.session_state:
    st.session_state['dtframe'] = None

if "current_applied" not in st.session_state:
    st.session_state['current_applied'] = []

if "coils_used" not in st.session_state:
    st.session_state['coils_used'] = []

if "kRefCoil" not in st.session_state:
    st.session_state['kRefCoil'] = 0

if "kMeasCoil" not in st.session_state:
    st.session_state['kMeasCoil'] = None

######################################## THE LAYOUT OF THE PAGE ###########################################
#config of the page
st.set_page_config(page_title="Magnetic Measurements SPS Database 🧲📏", page_icon="🧲", layout="wide",
                   initial_sidebar_state="expanded", menu_items=None)

# add background
add_bg_from_url(title)
######################################## THE LAYOUT OF THE PAGE ###########################################

fdiInputImpedance   = 400010
coilMeasResistance = {}

def show_results(current_applied,coils_used,impedance_img):
    # Initialize an empty dictionary to store DataFrames
    st.session_state.afcorrlist = []
    for current in current_applied:
        current_avg = avg_data.loc[avg_data.index == current]
                
        for coil in coils_used:
            bfr_corr = current_avg.loc[current,coil]
            aftr_corr = ((fdiInputImpedance + coilMeasResistance[coil])/ fdiInputImpedance) * bfr_corr
            
            # Create a dictionary for the current row of data
            row_data = {
                'Current':current,
                'Coil': coil,
                'Before Correction': bfr_corr,
                'After Correction': aftr_corr
            }
            # Append the row_data dictionary to the data_list
            st.session_state.afcorrlist.append(row_data)

    # Create a DataFrame from the data_list
    result_df = pd.DataFrame(st.session_state.afcorrlist)
    st.session_state.dtframe = result_df
    # Create two columns for arranging items side by side
    left_column, right_column = st.columns(2)

    # Add content to the left column
    with left_column:
        # Create a dropdown menu for selecting the "current" value
        selected_current = st.selectbox("Select a Current", current_applied)
        # Filter the DataFrame based on the selected "current"
        filtered_df = result_df[result_df['Current'] == selected_current].iloc[:, 1:]

        # Display the selected table
        st.write(f" Current {selected_current}:")
        st.dataframe(filtered_df, hide_index=1, width=600)        

    # Add content to the right column
    with right_column:
        empty_line(5)
        st.write("Impedance of every coil")
        st.image(impedance_img)
        st.image("images/Correction_image.png")


    # get the session state variables
    current_applied = st.session_state.current_applied
    coils_used = st.session_state.coils_used


    # Define a radio button to select input method
    input_method = st.radio("Select Input Method", ["Default Values", "Custom Input"])
    # Create two columns for arranging items side by side
    left_column, right_column = st.columns(2)
    
    # If the user selects "Custom Input," collect user inputs
    if input_method == "Custom Input":
        with left_column:
            with st.expander("Custom Coil Resistances"):
                for coil_name in coilMeasResistance:
                    coilMeasResistance[coil_name] = st.number_input(f"{coil_name} Resistance", 0.0)
            
        with right_column:
            show_results(current_applied,coils_used,impedance_img)
            #     # Create a "Show Results" button
            #     if st.button("Show Results"):
            #         # Display the selected values
                    
    else:
        show_results(current_applied,coils_used,impedance_img)
       





