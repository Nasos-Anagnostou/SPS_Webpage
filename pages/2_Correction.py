import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from custom_funct import *
from dbconnection import *
import pandas as pd


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
    data_list = []
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
            data_list.append(row_data)

    # Create a DataFrame from the data_list
    result_df = pd.DataFrame(data_list)
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

# Check if there is data in the DataFrame
if not df.empty:   
    # Access the basic information for the first row (iloc[0])
    basic_info = df.iloc[0]
    df = df.iloc[:, 7:]
    
    if "MBA" in basic_info['MAGNET_MEASURED']:

        if "B4" in basic_info['FLUXMETER_REFERENCE']:
            KRefCoil = 0.004460  # R5
            coilRefResistance = 6384.0  # ohm
        elif "Other" in basic_info['FLUXMETER_REFERENCE']:
            KRefCoil = 0.0  # R5
            coilRefResistance = 6400.0 # ohm

        if "A7" in basic_info['FLUXMETER_MEASURED']:
            KMeasCoil = [0.0, 0.002990, 0.0, 0.002670, 0.002680, 0.003990, 0.0, 0.003970, 0.0] # M1, M2, M3, M4, M5, M6, M7, M8, M9
            coilMeasResistance = {
                "R5": coilRefResistance,
                "M1": 6358.0,
                "M2": 6344.0,
                "M3": 6348.0,
                "M4": 6387.0,
                "M5": 6342.0,
                "M6": 6404.0,
                "M7": 6347.0,
                "M8": 6357.0,
                "M9": 6355.0
            }
        elif "Other" in basic_info['FLUXMETER_MEASURED']:
            KMeasCoil = [0.0] * 9  # M1, M2, M3, M4, M5, M6, M7, M8, M9
            coilMeasResistance = {f"M{i}": 6400.0 for i in range(1, 10)}
            coilMeasResistance["R5"] = coilRefResistance

        current_applied = (250, 1000, 2500, 4000, 4900)
        coils_used = ("R5", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9")
        impedance_img = "images/Impedance_dipole.png"
    

    elif "MBB" in basic_info['MAGNET_MEASURED']:
        
        if "B4" in basic_info['FLUXMETER_REFERENCE']:
            KRefCoil = 0.004460  # R5
            coilRefResistance = 6384.0  # ohm
        elif "Other" in basic_info['FLUXMETER_REFERENCE']:
            KRefCoil = 0.0  # R5
            coilRefResistance = 6500.0 # ohm

        if "B5" in basic_info['FLUXMETER_MEASURED']:
            KMeasCoil = [0.0, 0.004708, 0.0, 0.003518, 0.003898, 0.004478, 0.0, 0.004538, 0.0] # M1, M2, M3, M4, M5, M6, M7, M8, M9
            coilMeasResistance = {
                "R5": coilRefResistance,
                "M1": 6409.0,
                "M2": 6361.0,
                "M3": 6397.0,
                "M4": 6399.0,
                "M5": 6366.0,
                "M6": 6357.0,
                "M7": 6364.0,
                "M8": 6368.0,
                "M9": 6363.0
            }
        elif "Other" in basic_info['FLUXMETER_MEASURED']:
            KMeasCoil = [0.0] * 9  # M1, M2, M3, M4, M5, M6, M7, M8, M9
            coilMeasResistance = {f"M{i}": 6400.0 for i in range(1, 10)}
            coilMeasResistance["R5"] = coilRefResistance

        current_applied = (250, 1000, 2500, 4000, 4900)
        coils_used = ("R5", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9")
        impedance_img = "images/Impedance_dipole.png"

    elif "Quadrupole" in basic_info['MAGNET_MEASURED']:
        
        if "Q4" in basic_info['FLUXMETER_REFERENCE']:
            KRefCoil = -0.003890  # R5
            coilRefResistance = 39519.0  # ohm
        elif "Other" in basic_info['FLUXMETER_REFERENCE']:
            KRefCoil = 0.0  # R5
            coilRefResistance = 39000.0  # ohm

        if "Q2" in basic_info['FLUXMETER_MEASURED']:
            KMeasCoil = [0.0, 0.006720, 0.019860, 0.002840, -0.000290, 0.014550, 0.019280, 0.026890, 0.0]  # 0.0, M2, M3, M4, M5, M6, M7, M8, 0.0
            coilMeasResistance = {
                "R5": coilRefResistance,
                "M1": 0,
                "M2": 39651,
                "M3": 39655,
                "M4": 39658,
                "M5": 39547,
                "M6": 39556,
                "M7": 39623,
                "M8": 39734,
                "M9": 0
            }
        elif "Other" in basic_info['FLUXMETER_MEASURED']:
            KMeasCoil = [0.0] * 9  # M1, M2, M3, M4, M5, M6, M7, M8, M9
            coilMeasResistance = {f"M{i}": 3900.0 for i in range(1, 10)}
            coilMeasResistance["R5"] = coilRefResistance

        current_applied = (100, 400, 1000, 1540, 1938)
        coils_used = ("R5", "M2", "M3", "M4", "M5", "M6", "M7", "M8")
        impedance_img = "images/Impedance_quadrople.png"
    
    else:
        st.write("Error! Something went wrong with the magnet selection.")


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
       
else:
    st.write("No measurement information found in the DataFrame.")




