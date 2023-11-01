import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from custom_funct import *
from dbconnection import df,average_data,stddev_data
import pandas as pd


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


# Check if there is data in the DataFrame
if not df.empty:   
    # Access the basic information for the first row (iloc[0])
    basic_info = df.iloc[0]
    
    if "MBA" in basic_info['MAGNET_MEASURED']:
        st.session_state.magnettype = "Dipole"
        
        if "B4" in basic_info['FLUXMETER_REFERENCE']:
            st.session_state.kRefCoil = 0.004460  # R5
            coilRefResistance = 6384.0  # ohm
        elif "Other" in basic_info['FLUXMETER_REFERENCE']:
            st.session_state.kRefCoil = 0.0  # R5
            coilRefResistance = 6400.0 # ohm

        if "A7" in basic_info['FLUXMETER_MEASURED']:
            kMeasCoil = [0.0, 0.002990, 0.0, 0.002670, 0.002680, 0.003990, 0.0, 0.003970, 0.0] # M1, M2, M3, M4, M5, M6, M7, M8, M9
            coilMeasResistance = {
                "R5": coilRefResistance,
                "M1": 6358.0,
                "M2": 6344.0,
                "M3": 6348.0,
                "M4": 6387.0,
                "M5": 6342.0,
                "M6": 6404.0,
                "M7": 6347.0,
                "M8": 6357.0,
                "M9": 6355.0
            }
        elif "Other" in basic_info['FLUXMETER_MEASURED']:
            kMeasCoil = [0.0] * 9  # M1, M2, M3, M4, M5, M6, M7, M8, M9
            coilMeasResistance = {f"M{i}": 6400.0 for i in range(1, 10)}
            coilMeasResistance["R5"] = coilRefResistance

        st.session_state.current_applied = (250, 1000, 2500, 4000, 4900)
        st.session_state.coils_used = ("R5", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9")
        impedance_img = "images/Impedance_dipole.png"
    

    elif "MBB" in basic_info['MAGNET_MEASURED']:
        st.session_state.magnettype = "Dipole"

        if "B4" in basic_info['FLUXMETER_REFERENCE']:
            st.session_state.kRefCoil = 0.004460  # R5
            coilRefResistance = 6384.0  # ohm
        elif "Other" in basic_info['FLUXMETER_REFERENCE']:
            st.session_state.kRefCoil = 0.0  # R5
            coilRefResistance = 6500.0 # ohm

        if "B5" in basic_info['FLUXMETER_MEASURED']:
            kMeasCoil = [0.0, 0.004708, 0.0, 0.003518, 0.003898, 0.004478, 0.0, 0.004538, 0.0] # M1, M2, M3, M4, M5, M6, M7, M8, M9
            coilMeasResistance = {
                "R5": coilRefResistance,
                "M1": 6409.0,
                "M2": 6361.0,
                "M3": 6397.0,
                "M4": 6399.0,
                "M5": 6366.0,
                "M6": 6357.0,
                "M7": 6364.0,
                "M8": 6368.0,
                "M9": 6363.0
            }
        elif "Other" in basic_info['FLUXMETER_MEASURED']:
            kMeasCoil = [0.0] * 9  # M1, M2, M3, M4, M5, M6, M7, M8, M9
            coilMeasResistance = {f"M{i}": 6400.0 for i in range(1, 10)}
            coilMeasResistance["R5"] = coilRefResistance

        st.session_state.current_applied = (250, 1000, 2500, 4000, 4900)
        st.session_state.coils_used = ("R5", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9")
        impedance_img = "images/Impedance_dipole.png"

    elif "Quadrupole" in basic_info['MAGNET_MEASURED']:
        st.session_state.magnettype = "Quadrupole"

        if "Q4" in basic_info['FLUXMETER_REFERENCE']:
            st.session_state.kRefCoil = -0.003890  # R5
            coilRefResistance = 39519.0  # ohm
        elif "Other" in basic_info['FLUXMETER_REFERENCE']:
            st.session_state.kRefCoil = 0.0  # R5
            coilRefResistance = 39000.0  # ohm

        if "Q2" in basic_info['FLUXMETER_MEASURED']:
            kMeasCoil = [0.0, 0.006720, 0.019860, 0.002840, -0.000290, 0.014550, 0.019280, 0.026890, 0.0]  # 0.0, M2, M3, M4, M5, M6, M7, M8, 0.0
            coilMeasResistance = {
                "R5": coilRefResistance,
                "M1": 0,
                "M2": 39651,
                "M3": 39655,
                "M4": 39658,
                "M5": 39547,
                "M6": 39556,
                "M7": 39623,
                "M8": 39734,
                "M9": 0
            }
        elif "Other" in basic_info['FLUXMETER_MEASURED']:
            kMeasCoil = [0.0] * 9  # M1, M2, M3, M4, M5, M6, M7, M8, M9
            coilMeasResistance = {f"M{i}": 3900.0 for i in range(1, 10)}
            coilMeasResistance["R5"] = coilRefResistance

        st.session_state.current_applied = (100, 400, 1000, 1540, 1938)
        st.session_state.coils_used = ("R5", "M2", "M3", "M4", "M5", "M6", "M7", "M8")
        impedance_img = "images/Impedance_quadrople.png"
    
    else:
        st.write("Error! Something went wrong with the magnet selection.")

    # Creating the dictionary
    st.session_state.kMeasCoil = {key: value for key, value in zip(['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9'], kMeasCoil)}

    st.title("Measurement Information")

    # # Display the basic information
    # st.subheader("Basic Measurement Info")
    # st.write(f"Workorder number: {basic_info['WORKORDER_N']}")
    # st.write(f"Date Measured: {basic_info['MEASUREMENT_DATE']}")
    # st.write(f"{basic_info['MAGNET_MEASURED']}")
    # st.write(f"{basic_info['MAGNET_REFERENCE']}")
    # st.write(f"{basic_info['FLUXMETER_MEASURED']}")
    # st.write(f"{basic_info['FLUXMETER_REFERENCE']}")
    # Display the basic information in a horizontal layout
    # Display the basic information in a table
    st.subheader("Basic Measurement Info")

    # Create a table to display the information
    basic_info_table = pd.DataFrame(
        {
            'Workorder number': [basic_info['WORKORDER_N']],
            'Date Measured': [basic_info['MEASUREMENT_DATE']],
            'Magnet Measured': [basic_info['MAGNET_MEASURED']],
            'Magnet Reference': [basic_info['MAGNET_REFERENCE']],
            'Fluxmeter Measured': [basic_info['FLUXMETER_MEASURED']],
            'Fluxmeter Reference': [basic_info['FLUXMETER_REFERENCE']]
        }
    )
    st.table(basic_info_table)


else:
    st.write("No measurement information found in the DataFrame.")


 # Display the data in a Streamlit table
st.title("Magnetic Measurements Data")
df = df.iloc[:, 7:]
st.dataframe(df, width=1200)

# Create two columns for arranging items side by side
left_column, right_column = st.columns(2)


with left_column:
    # for a specific workorder,date, etc 
    st.title("Average Flux")
    # Display the pivoted data
    st.dataframe(average_data)      


with right_column:
    st.title("Stddev Flux")
    # Display the pivoted data
    st.dataframe(stddev_data)