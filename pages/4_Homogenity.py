import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.row import row 
from custom_funct import *
import pandas as pd
import plotly.express as px



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

# get the session state variables
current_applied = st.session_state.current_applied
kRefCoil = st.session_state.kRefCoil
kMeasCoil = st.session_state.kMeasCoil
afcorrlist = st.session_state.afcorrlist
coils_used = st.session_state.coils_used
magnettype = st.session_state.magnettype


subtraction_result = {}
subtraction_result_dv = {}
subtraction_result_dvcorr = {}

# Check if there is data in the DataFrame
if st.session_state.flag:   
    for current in current_applied:
        
        sub_result = {}
        sub_result_dv = {}
        sub_result_dvcorr = {}    
        # Extract 'After Correction' value where 'Coil' is 'M5'
        m5_aftercorr = [entry["After Correction"] for entry in afcorrlist if (entry["Coil"] == "M5" and entry["Current"] == current)]
        m5_aftercorr = m5_aftercorr[0] if m5_aftercorr else None      
        
        for coil in coils_used:
            if coil == "R5":
                continue
            
            mi = [entry["After Correction"] for entry in afcorrlist if (entry["Coil"] == coil and entry["Current"] == current)]
            mi = mi[0] if mi else None

            value1 = mi-m5_aftercorr if m5_aftercorr is not None else None
            value2 = 1000* (value1) / m5_aftercorr  if m5_aftercorr is not None else None
            value3 = value2 - (1000*(kMeasCoil[coil] - kMeasCoil["M5"]))
            sub_result[f"{coil} - M5"] = value1, value2, value3
            
        subtraction_result[current] = {key: value[0] for key, value in sub_result.items()}
        subtraction_result_dv[current] = {key: value[1] for key, value in sub_result.items()}
        subtraction_result_dvcorr[current] = {key: value[2] for key, value in sub_result.items()}


    # Create a DataFrame
    df = pd.DataFrame(subtraction_result)
    df.index.name = 'Coil'
        
    # Create a DataFrame
    df_dv = pd.DataFrame(subtraction_result_dv)
    df_dv.index.name = 'Coil'

    # Create a DataFrame
    df_dvcorr = pd.DataFrame(subtraction_result_dvcorr)
    df_dvcorr.index.name = 'Coil'

    if magnettype == "Quadrupole":
        df_dvcorr.insert(0, 'Position', [40, 55, 35, 0, -35, -55, -40] )#M2...M8

    elif magnettype == "Dipole":
        df_dvcorr.insert(0, 'Position', [11, 44, -11, 25, 0, -25, 11, -44, -11]) #M1...M9

    # get rid of the irelevant data
    df_filtered = df_dvcorr[~df_dvcorr.index.isin(["M8 - M5", "M2 - M5"])]
    # Get column names and store in a list
    column_names = df_filtered.columns[1:].tolist()  # Exclude the 'Position' column


    left_column, right_column = st.columns(2)

    with left_column:
        #selected_table = st.selectbox("Select a Table", ("Mi-M5","Vmeas-Vref /Vref (E-3)", "Vmeas-Vref /Vref (E-3) corrected" ))
        st.header("Mi-M5")
        st.dataframe(df,use_container_width= True)
        
        
        
        st.header("Vmeas-Vref /Vref (E-3) corrected")
        st.dataframe(df_dvcorr,use_container_width= True)

    with right_column:
        st.header("Vmeas-Vref /Vref (E-3)")
        st.dataframe(df_dv,use_container_width= True)

        st.header("Homogeneity shown only for x-axis coils")
        # Create Plotly figure
        fig = px.line(df_filtered, x='Position', title='Homogeneity', markers=True,
                    labels={'Position': 'Position of the coil with respect to the central coil (mm)', 'value':'dG/Gref (E-3)'})
        # Add lines for each column in column_names
        for col in column_names:
            fig.add_scatter(x=df_filtered['Position'], y=df_filtered[col], name=col)

        fig.update_layout(title_x = 0.35, title_font =dict(size=30))
        fig.update_layout(yaxis=dict(title=dict(text="dG/Gref (E-3)", font=dict(size=25))))

        fig.update_yaxes(showticklabels=False)
        st.plotly_chart(fig)

else:
    empty_line(3)
    row1 = row([0.7, 0.6], vertical_align="center")
    row1.subheader("Please choose first the date or the workorder of the measurement.")
    if row1.button("Back to Home Page 🏠"):
        switch_page("Raw_data")