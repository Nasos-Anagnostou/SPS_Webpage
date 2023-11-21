import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.row import row 
from custom_funct import *
from Home_Page import *
import pandas as pd


# Initialization of the st.session variables
if "magnettype" not in st.session_state:
    st.session_state['magnettype'] = ""

if "coilMeasResistance" not in st.session_state:
    st.session_state['coilMeasResistance'] = {}

if "afcorrlist" not in st.session_state:
    st.session_state['afcorrlist'] = []

if "current_applied" not in st.session_state:
    st.session_state['current_applied'] = []

if "coils_used" not in st.session_state:
    st.session_state['coils_used'] = []

if "kRefCoil" not in st.session_state:
    st.session_state['kRefCoil'] = 0

if "kMeasCoil" not in st.session_state:
    st.session_state['kMeasCoil'] = None

if "avg_data" not in st.session_state:
    st.session_state['avg_data'] = None

if "impedance_img" not in st.session_state:
    st.session_state['impedance_img'] = ""

if "flag" not in st.session_state:
    st.session_state['flag'] = False

if "mydf" not in st.session_state:
    st.session_state['mydf'] = None
######################################## THE LAYOUT OF THE PAGE ###########################################
#config of the page
st.set_page_config(page_title="Magnetic Measurements SPS Database 🧲📏", page_icon="🧲", layout="wide",
                   initial_sidebar_state="expanded", menu_items=None)
# add background
add_bg_from_url(title)
######################################## THE LAYOUT OF THE PAGE ###########################################

if st.session_state.flag:

    mydf = st.session_state.mydf
    all_coils = ['R5', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9']

    # Access the basic information for the first row (iloc[0])            
    basic_info = mydf.iloc[0]
    st.subheader("Basic Measurement Information")
    # Create a table to display the information
    basic_info_table = pd.DataFrame(
        {
            'Workorder number': str(basic_info['WORKORDER_N']),
            'Date Measured': [basic_info['MEASUREMENT_DATE']],
            'Magnet Measured': [basic_info['MAGNET_MEASURED']],
            'Magnet Reference': [basic_info['MAGNET_REFERENCE']],
            'Fluxmeter Measured': [basic_info['FLUXMETER_MEASURED']],
            'Fluxmeter Reference': [basic_info['FLUXMETER_REFERENCE']]
        }
    )
    st.dataframe(basic_info_table, use_container_width= True, hide_index= True)

    # Display the data in a Streamlit table
    newdf = mydf.iloc[:, 7:]
    st.title("Magnetic Measurements Data")
    make_df(newdf,False)
    
    # Show the average and sttdev tables
    avgdf = mydf.rename(columns={'CURRENT_APPLIED':'Current'})
    st.session_state.avg_data = avg_stddev_tables(avgdf,all_coils)

else:
    empty_line(3)
    row1 = row([0.7, 0.6], vertical_align="bottom")
    row1.subheader("Please choose first the date or the workorder of the measurement.")
    if row1.button("Back to Home Page 🏠"):
        switch_page("Home_Page")


