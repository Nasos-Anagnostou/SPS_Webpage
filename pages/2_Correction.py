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
    # Access the basic information for the first row (iloc[0])
    basic_info = df.iloc[0]
    
    if "Dipole" in basic_info['MAGNET_MEASURED']:
        print("This is a Dipole")

        coil_impedances = [
            ("R5", 6384),
            ("M1", 6409),
            ("M2", 6361),
            ("M3", 6397),
            ("M4", 6399),
            ("M5", 6366),
            ("M6", 6357),
            ("M7", 6364),
            ("M8", 6368),
            ("M9", 6363),
            ("FDI", 400010)
        ]
        

    elif "Quadrupole" in basic_info['MAGNET_MEASURED']:
        print("This is a Quadruple")
        
        coil_impedances = [
            ("R5", 39519),
            ("M2", 39651),
            ("M3", 39655),
            ("M4", 39658),
            ("M5", 39547),
            ("M6", 39556),
            ("M7", 39623),
            ("M8", 39734),
            ("FDI", 400010)
        ]
    
    if basic_info['CURRENT_APPLIED'] == 1000:
            st.write("MALAKAAAA")
            st.write(basic_info)
    


else:
    print("No measurement information found in the DataFrame.")
