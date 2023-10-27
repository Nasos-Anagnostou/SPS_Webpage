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



current_applied = st.session_state.current_applied
kRefCoil = st.session_state.kRefCoil
kMeasCoil = st.session_state.kMeasCoil
afcorrlist = st.session_state.afcorrlist
result_df = st.session_state.dtframe

for current in current_applied:
    filtered_df = result_df[result_df['Current'] == current].iloc[:, 1:]
    # Display the selected table
    st.write(f" Current {current}:")
    st.dataframe(filtered_df, hide_index=1, width=600) 

# for current in current_applied:
#     st.write(current)

#     for  index, dict in enumerate(afcorrlist):
#         if dict['Coil'] == 'R5':
#             continue

#         if dict['Current'] == current:
            
            
#             st.write(dict['Coil'])
#             st.write("after correction",dict['After Correction'])
            
#             print(aftrcorr_m5,aftrcorr_r5)
#             print(diffm5r5)
#             print (dvvref)
#             print(dvcorrected)