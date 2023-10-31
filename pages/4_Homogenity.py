import streamlit as st

from streamlit_extras.switch_page_button import switch_page
from custom_funct import *
import pandas as pd


# Initialization of the st.session variables
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
    st.session_state['kMeasCoil'] = []


######################################## THE LAYOUT OF THE PAGE ###########################################
#config of the page
st.set_page_config(page_title="Magnetic Measurements SPS Database 🧲📏", page_icon="🧲", layout="wide",
                   initial_sidebar_state="expanded", menu_items=None)

# add background
add_bg_from_url(title)
######################################## THE LAYOUT OF THE PAGE ###########################################

# get the session state variables
current_applied = st.session_state.current_applied
kRefCoil = st.session_state.kRefCoil
kMeasCoil = st.session_state.kMeasCoil
afcorrlist = st.session_state.afcorrlist
result_df = st.session_state.dtframe
coils_used = st.session_state.coils_used

st.write(afcorrlist)

subtraction_result = {}
for current in current_applied:
    
    st.write(current)
    sub_result = {}
    # Extract 'After Correction' value where 'Coil' is 'M5'
    m5_aftercorr = [entry["After Correction"] for entry in afcorrlist if (entry["Coil"] == "M5" and entry["Current"] == current)]
    m5_aftercorr = m5_aftercorr[0] if m5_aftercorr else None      
    
    for coil in coils_used:

        if coil == "R5" or coil == 'M5':
            continue
        elif coil != 'M5':
            mi = [entry["After Correction"] for entry in afcorrlist if (entry["Coil"] == coil and entry["Current"] == current)]
            mi = mi[0] if mi else None
            sub_result[f"{coil} - M5"] = mi-m5_aftercorr if m5_aftercorr is not None else None

    subtraction_result[current] = sub_result
    st.write(sub_result)


    # # Display the subtraction results
    # for mi, subtraction in sub_result.items():

    #     st.write(f"{mi} - M5: {subtraction}")
    #         # Creating a DataFrame
    #     data = {
    #         'Current': current,
    #         'R5': r5_aftcorr,
    #         'M5': m5_aftercorr,
    #         'M5-R5': dVcorr,
    #         '(Vmeas-Vref)/Vref   (E-3)': dv_vref,
    #         'dV/Vref corrected   (E-3)': dvcorr_vref
    #    }