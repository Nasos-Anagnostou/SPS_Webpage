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


# Check if there is data in the DataFrame
if not df.empty:   
    # Access the basic information for the first row (iloc[0])
    basic_info = df.iloc[0]
    df = df.iloc[:, 7:]
    
    if "Dipole" in basic_info['MAGNET_MEASURED']:
        print("This is a Dipole")
        coil_impedances = {
            "R5": 6384,
            "M1": 6409,
            "M2": 6361,
            "M3": 6397,
            "M4": 6399,
            "M5": 6366,
            "M6": 6357,
            "M7": 6364,
            "M8": 6368,
            "M9": 6363,
            "FDI": 400010
        }
        current_applied = (250, 1000, 2500, 4000, 4900)
        coils_used = ('R5', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9')

    elif "Quadrupole" in basic_info['MAGNET_MEASURED']:
        print("This is a Quadruple")
        coil_impedances = {
            "R5": 39519,
            "M2": 39651,
            "M3": 39655,
            "M4": 39658,
            "M5": 39547,
            "M6": 39556,
            "M7": 39623,
            "M8": 39734,
            "FDI": 400010
        }
        current_applied = (100, 400, 1000, 1540, 1938)
        coils_used = ('R5','M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8')
    
    # for every current create a table with the correction for each coil
    # correction form
    #corr_data = ((coil_impedances["FDI"] + coil_impedances[coils_used])/ coil_impedances["FDI"]) * average_data
    
    for current in current_applied:
         st.write(current)
         current_avg = avg_data.loc[avg_data.index == current]
         st.write(current_avg)

         filtered_df = df[df['CURRENT_APPLIED'] == current]
         st.write(filtered_df)
         
         for coil in coils_used:
            st.write(coil)
            curr_avg = current_avg[coil]
            st.write(curr_avg)
            #corr_data = ((coil_impedances["FDI"] + coil_impedances[coil])/ coil_impedances["FDI"]) * curr_avg
            #st.write(corr_data)
         
    


else:
    print("No measurement information found in the DataFrame.")
