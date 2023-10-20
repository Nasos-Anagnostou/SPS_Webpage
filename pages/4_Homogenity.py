import streamlit as st

from streamlit_extras.switch_page_button import switch_page
from custom_funct import *



######################################## THE LAYOUT OF THE PAGE ###########################################
#config of the page
st.set_page_config(page_title="Magnetic Measurements SPS Database 🧲📏", page_icon="🧲", layout="wide",
                   initial_sidebar_state="expanded", menu_items=None)

# add background
add_bg_from_url(title)
######################################## THE LAYOUT OF THE PAGE ###########################################



# Create a collapsible section for coil resistances
with st.expander("Coil Resistances"):
    coilMeasResistance = {
        "M1": 0.0, "M2": 0.0, "M3": 0.0, "M4": 0.0,
        "M5": 0.0, "M6": 0.0, "M7": 0.0, "M8": 0.0, "M9": 0.0
    }

    # Collect user inputs for coil resistances
    for coil_name in coilMeasResistance:
        coilMeasResistance[coil_name] = st.number_input(f"{coil_name} Resistance", 0.0)

# Display the collected values
st.write("Collected Coil Resistances:", coilMeasResistance)
