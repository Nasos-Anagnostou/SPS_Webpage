import streamlit as st
import pandas as pd
from streamlit_extras.row import row
from streamlit_extras.stateful_button import button
from streamlit_extras.switch_page_button import switch_page
from custom_funct import *




# Initialization of the st.session variables
if "magnettype" not in st.session_state:
    st.session_state['magnettype'] = ""

if "coilMeasResistance" not in st.session_state:
    st.session_state['coilMeasResistance'] = {}

if "impedance_img" not in st.session_state:
    st.session_state['impedance_img'] = ""

if "afcorrlist" not in st.session_state:
    st.session_state['afcorrlist'] = []

if "mydf" not in st.session_state:
    st.session_state['mydf'] = None

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
mydf = pd.DataFrame()
# get the database data
df = dbconnect("C:\Oracle\instantclient_12_2")

# Define a radio button to select input method
input_method = st.radio("Select Input Method", ["Choose a specific Workorder and Date","See all data"], horizontal= True)
empty_line(1)


#if database is not empty
if not df.empty:

    # user chooses witch way to analyze the data
    if input_method == "Choose a specific Workorder and Date":  # 1st option
        
        row1 = row([0.3, 0.4, 0.7],gap = "medium", vertical_align="bottom")

        workorder_input = row1.text_input('Workorder number','')
        date_input = row1.date_input('Date of the measurement', value=None, format ="DD/MM/YYYY")
        if date_input != None: date_input = date_input.strftime('%d/%m/%Y') 

        if row1.button("Show measurement data", key="Button"):
            
            if workorder_input and not date_input:
                mydf = df[df["WORKORDER_N"].notnull() & (df["WORKORDER_N"].astype(str) == str(workorder_input))]
            elif date_input and not workorder_input:
                mydf = df[df["MEASUREMENT_DATE"].astype(str).str.contains(date_input)]
            elif workorder_input and date_input:
                mydf = df[df["MEASUREMENT_DATE"].astype(str).str.contains(date_input)]
                mydf = mydf[mydf["WORKORDER_N"].notnull() & (mydf["WORKORDER_N"].astype(str) == str(workorder_input))]
            else:
                empty_line(3)
                st.subheader("⚠️ Please provide a valid Workorder and/or a Date first ")
            

            if not mydf.empty:
                magnet_calibration(mydf)
                st.session_state.mydf = mydf
                st.session_state.flag = True
                switch_page("Raw_data")
                
            else:
                st.session_state.flag = False
                if workorder_input and not date_input:
                    empty_line(2)
                    st.subheader("The selected Workorder has no measurements")
                elif date_input and not workorder_input:
                    empty_line(2)
                    st.subheader("The selected Date has no measurements")
                elif workorder_input and date_input:
                    empty_line(2)
                    st.subheader("The selected Date and Workorder have no measurements")
        
    # Display all data in a Streamlit table and apply filters
    else:   # 2nd Option
    
        st.title("Magnetic measurement data contained in the database")
        empty_line(1)
        st.subheader("Apply the desired filters (workorder number, date, etc.)")
        mydf = make_df(df,True)

        # Add a button to save the modified DataFrame
        if st.button("Analyse Measurement",key= "Button"):

            if not mydf.equals(df):
                # Save the modified DataFrame to a file (modify this part based on your saving preference)
                magnet_calibration(mydf)
                st.session_state.mydf = mydf
                st.session_state.flag = True
                switch_page("Raw_data")
            
            elif (mydf.equals(df)):
                st.session_state.flag = False
                st.subheader("Please apply some filters first!")


else:
    st.write("The database is empty")



