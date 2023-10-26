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

aftrcorr_m5 = 10 
aftrcorr_r5 = 20 
diffm5r5 = aftrcorr_m5 - aftrcorr_r5
dvvref = 1000 * (diffm5r5/aftrcorr_r5)
dvcorrected = dvvref - (1000* (1-kRefCoil) )
dvcorrlist = {}


for current in current_applied:

    for  row in afcorrlist:

        if row['Current'] == current:

            st.write(current)
            print(aftrcorr_m5,aftrcorr_r5)
            print(diffm5r5)
            print (dvvref)
            print(dvcorrected)


for current, dvcorr in dvcorrlist:
    
    #table
    print(current, aftrcorr_m5, dvcorr)
