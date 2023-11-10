import streamlit as st
from streamlit_extras.row import row
from streamlit_extras.stateful_button import button

from custom_funct import *
from dbconnection import df
import pandas as pd



# Initialization of the st.session variables
if "magnettype" not in st.session_state:
    st.session_state['magnettype'] = ""

if "coilMeasResistance" not in st.session_state:
    st.session_state['coilMeasResistance'] = {}

if "impedance_img" not in st.session_state:
    st.session_state['impedance_img'] = ""

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

if "avg_data" not in st.session_state:
    st.session_state['avg_data'] = None

if "flag" not in st.session_state:
    st.session_state['flag'] = False

######################################## THE LAYOUT OF THE PAGE ###########################################
#config of the page
st.set_page_config(page_title="Magnetic Measurements SPS Database 🧲📏", page_icon="🧲", layout="wide",
                   initial_sidebar_state="expanded", menu_items=None)

# add background
add_bg_from_url(title)
######################################## THE LAYOUT OF THE PAGE ###########################################

# coils used and dataframe init
coils_used = ['R5', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9']
mydf = pd.DataFrame()

# Define a radio button to select input method
input_method = st.radio("Select Input Method", ["Choose a specific Workorder and Date", "See all data"], horizontal= True)

#if database is not empty
if not df.empty:
        
    if input_method == "Choose a specific Workorder and Date":

        st.session_state.flag = False

        df = df.rename(columns={'CURRENT_APPLIED':'Current'})
        row1 = row([0.5, 0.5], vertical_align="center")
        workorder_input = row1.text_input('Provide the Workorder number','')
        date_input = row1.date_input('Date of the measurement', value=None, format ="DD/MM/YYYY")
        if date_input != None: date_input = date_input.strftime('%d/%m/%Y') 
        

        if st.button("Show measurement data", key="Button"):
            
            if workorder_input and not date_input:
                mydf = df[df["WORKORDER_N"].notnull() & (df["WORKORDER_N"].astype(str) == str(workorder_input))]
            elif date_input and not workorder_input:
                mydf = df[df["MEASUREMENT_DATE"].astype(str).str.contains(date_input)]
            elif workorder_input and date_input:
                mydf = df[df["MEASUREMENT_DATE"].astype(str).str.contains(date_input)]
                mydf = mydf[mydf["WORKORDER_N"].astype(str) == workorder_input]
            else:
                st.subheader("Please provide a valid Workorder and/or the Date first")


            if not mydf.empty:
                st.session_state.flag = True

                if "MBA" in str(mydf['MAGNET_MEASURED']):
                    st.session_state.magnettype = "Dipole"
                    
                    if "B4" in str(mydf['FLUXMETER_REFERENCE']):
                        st.session_state.kRefCoil = 0.004460  # R5
                        coilRefResistance = 6384.0  # ohm
                    elif "Other" in str(mydf['FLUXMETER_REFERENCE']):
                        st.session_state.kRefCoil = 0.0  # R5
                        coilRefResistance = 6400.0 # ohm

                    if "A7" in str(mydf['FLUXMETER_MEASURED']):
                        kMeasCoil = [0.0, 0.002990, 0.0, 0.002670, 0.002680, 0.003990, 0.0, 0.003970, 0.0] # M1, M2, M3, M4, M5, M6, M7, M8, M9
                        st.session_state.coilMeasResistance = {
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
                    elif "Other" in str(mydf['FLUXMETER_MEASURED']):
                        kMeasCoil = [0.0] * 9  # M1, M2, M3, M4, M5, M6, M7, M8, M9
                        st.session_state.coilMeasResistance = {f"M{i}": 6400.0 for i in range(1, 10)}
                        st.session_state.coilMeasResistance["R5"] = coilRefResistance

                    st.session_state.current_applied = (250, 1000, 2500, 4000, 4900)
                    st.session_state.coils_used = ("R5", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9")
                    st.session_state.impedance_img = "images/Impedance_dipole.png"
                

                elif "MBB" in str(mydf['MAGNET_MEASURED']):
                    st.session_state.magnettype = "Dipole"

                    if "B4" in str(mydf['FLUXMETER_REFERENCE']):
                        st.session_state.kRefCoil = 0.004460  # R5
                        coilRefResistance = 6384.0  # ohm
                    elif "Other" in str(mydf['FLUXMETER_REFERENCE']):
                        st.session_state.kRefCoil = 0.0  # R5
                        coilRefResistance = 6500.0 # ohm

                    if "B5" in str(mydf['FLUXMETER_MEASURED']):
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
                    elif "Other" in str(mydf['FLUXMETER_MEASURED']):
                        kMeasCoil = [0.0] * 9  # M1, M2, M3, M4, M5, M6, M7, M8, M9
                        st.session_state.coilMeasResistance = {f"M{i}": 6400.0 for i in range(1, 10)}
                        st.session_state.coilMeasResistance["R5"] = coilRefResistance

                    st.session_state.current_applied = (250, 1000, 2500, 4000, 4900)
                    st.session_state.coils_used = ("R5", "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9")
                    st.session_state.impedance_img = "images/Impedance_dipole.png"

                elif "Quadrupole" in str(mydf['MAGNET_MEASURED']):
                    st.session_state.magnettype = "Quadrupole"

                    if "Q4" in str(mydf['FLUXMETER_REFERENCE']):
                        st.session_state.kRefCoil = -0.003890  # R5
                        coilRefResistance = 39519.0  # ohm
                    elif "Other" in str(mydf['FLUXMETER_REFERENCE']):
                        st.session_state.kRefCoil = 0.0  # R5
                        coilRefResistance = 39000.0  # ohm

                    if "Q2" in str(mydf['FLUXMETER_MEASURED']):
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
                    elif "Other" in str(mydf['FLUXMETER_MEASURED']):
                        kMeasCoil = [0.0] * 9  # M1, M2, M3, M4, M5, M6, M7, M8, M9
                        st.session_state.coilMeasResistance = {f"M{i}": 3900.0 for i in range(1, 10)}
                        st.session_state.coilMeasResistance["R5"] = coilRefResistance

                    st.session_state.current_applied = (100, 400, 1000, 1540, 1938)
                    st.session_state.coils_used = ("R5", "M2", "M3", "M4", "M5", "M6", "M7", "M8")
                    st.session_state.impedance_img = "images/Impedance_quadrople.png"
                
                else:
                    st.write("Error! Something went wrong with the magnet selection.")
                    exit()
                
                # Access the basic information for the first row (iloc[0])            
                basic_info = mydf.iloc[0]
                mydf = mydf.iloc[:, 7:]
                st.subheader("Basic Measurement Info")
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

                # Creating the dictionary
                st.session_state.kMeasCoil = {key: value for key, value in zip(['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9'], kMeasCoil)}
            
                # Display the data in a Streamlit table
                st.title("Magnetic Measurements Data")
                make_df(mydf,False)

                # Create two columns for arranging items side by side
                left_column, right_column = st.columns(2)
                
                # Average Flux of the coils for different current applied
                st.session_state.avg_data = mydf.pivot_table(index='Current', values= coils_used, aggfunc='mean')
                average_data = st.session_state.avg_data.style.format("{:.6f}")

                # Stddev Flux of the coils for different current applied
                grouped_data = mydf.groupby('Current')[coils_used].std()
                pivoted_data = grouped_data.reset_index().pivot_table(index='Current')
                stddev_data = pivoted_data.style.format("{:.6f}")

                with left_column:
                    # for a specific workorder,date, etc 
                    st.title("Average Flux")
                    # Display the pivoted data
                    st.dataframe(average_data, column_order= ('R5','M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9'))      


                with right_column:
                    st.title("Stddev Flux")
                    # Display the pivoted data
                    st.dataframe(stddev_data, column_order= ('R5','M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9'))
            else:
                
                if workorder_input and not date_input:
                    st.subheader("The selected Workorder has no measurements")
                elif date_input and not workorder_input:
                    st.subheader("The selected Date has no measurements")
                elif workorder_input and date_input:
                    st.subheader("The selected Date and Workorder have no measurements")
    
        
    else:
        # Display the data in a Streamlit table
        st.title("Magnetic measurement data contained in the database")
        make_df(df,True)
        
else:
    st.write("The database is empty")



