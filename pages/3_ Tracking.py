import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from custom_funct import *

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


st.write(afcorrlist)
aftrcorr_m5 = 10 
aftrcorr_r5 = 20 
diffm5r5 = aftrcorr_m5 - aftrcorr_r5
dvvref = 1000 * (diffm5r5/aftrcorr_r5)
dvcorrected = dvvref - (1000* (1-kRefCoil) )
dvcorrlist = {}


for current in current_applied:

    filtered_df = result_df[(result_df['Current'] == current) & (result_df["Coil"] == 'R5')]
    
    try:
        value = filtered_df['After Correction']
        st.write(value)
    except:
        st.write("nope")

    for  index, dict in enumerate(afcorrlist):
        if dict['Coil'] == 'R5':
            continue

        # if dict['Current'] == current:
            
        #     # Display the selected table
        #     st.write(f" Current {current}:")
        #     st.dataframe(filtered_df, hide_index=1, width=600)
            
            
