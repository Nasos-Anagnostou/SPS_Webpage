import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from custom_funct import *
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Initialization of the st.session variables
if "afcorrlist" not in st.session_state:
    st.session_state['afcorrlist'] = []

if "current_applied" not in st.session_state:
    st.session_state['current_applied'] = []

if "kRefCoil" not in st.session_state:
    st.session_state['kRefCoil'] = 0

if "kMeasCoil" not in st.session_state:
    st.session_state['kMeasCoil'] = []

####################################################### INITIALIZATION ###############################################################
# init the styles of fonts
homepage = '<p style="font-family:Arial Black; color:black; font-size: 200%;"><strong>Homepage 🏠</strong></p>'
comp = '<p style="font-family:Arial Black; color:#262730; font-size: 150%;"><strong>Chose competition🏆</strong></p>'
title = '<p style="font-family:Arial Black; color:white; font-size: 300%; text-align: center;">Magnetic Measurements SPS Database 🧲📏</p>'

######################################## THE LAYOUT OF THE PAGE ###########################################
#config of the page
st.set_page_config(page_title="Magnetic Measurements SPS Database 🧲📏", page_icon="🧲", layout="wide",
                   initial_sidebar_state="expanded", menu_items=None)

# add background
add_bg_from_url(title)
######################################## THE LAYOUT OF THE PAGE ###########################################

current_applied = st.session_state.current_applied
kRefCoil = st.session_state.kRefCoil
kMeasCoil = st.session_state.kMeasCoil
afcorrlist = st.session_state.afcorrlist
result_df = st.session_state.dtframe


tracking_list = []

for current in current_applied:

    # Extract 'After Correction' values where 'Coil' is 'R5' and 'M5'
    r5_aftcorr = [entry["After Correction"] for entry in afcorrlist if (entry["Coil"] == "R5" and entry["Current"] == current)]
    r5_aftcorr = r5_aftcorr[0]
    
    # Extract 'After Correction' value where 'Coil' is 'R5'
    m5_aftercorr = [entry["After Correction"] for entry in afcorrlist if (entry["Coil"] == "M5" and entry["Current"] == current)]
    m5_aftercorr = m5_aftercorr[0]

    dVcorr = m5_aftercorr - r5_aftcorr
    dv_vref = 1000 * ( dVcorr / r5_aftcorr)
    dvcorr_vref = dv_vref - (1000* kMeasCoil[4] - kRefCoil)

    # Creating a DataFrame
    data = {
        'Current': current,
        'R5': r5_aftcorr,
        'M5': m5_aftercorr,
        'M5-R5': dVcorr,
        '(Vmeas-Vref)/Vref': dv_vref,
        'dV/Vref corrected': dvcorr_vref
    }
    tracking_list.append(data)

empty_line(3)
st.header("Tracking Results")
df_tracking = pd.DataFrame(tracking_list)
st.dataframe(df_tracking, hide_index=1, use_container_width=True)

st.header("Line Charts for Magnetization Curve and Tracking")
# Create two columns for arranging items side by side
left_column, right_column = st.columns(2)

with left_column:
    # Create a line chart using Plotly Express
    fig = px.line(df_tracking, x='Current', y='M5', title='Magnetization curve', markers= True, 
                labels={'Current': 'Current in A', 'M5': 'Flux (V.s)'})
    fig.update_layout(title_x = 0.4)
    fig.update_traces(marker=dict(color='white', size=8))

    st.plotly_chart(fig)

with right_column:
    # Create a line chart using Plotly Express
    fig = px.line(df_tracking, x='Current', y='dV/Vref corrected', title='Tracking', markers= True, 
                labels={'Current': 'Current in A', 'M5': 'dG/G (E-3)'})
    fig.update_layout(title_x = 0.4)
    fig.update_traces(marker=dict(color='white', size=8))

    st.plotly_chart(fig)


            
            
