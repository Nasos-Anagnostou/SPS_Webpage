from PIL import Image
import requests
import streamlit as st
from streamlit_extras.row import row 
import base64
from io import BytesIO
import validators  # You need to import the validators library
from st_aggrid import GridOptionsBuilder, AgGrid
import pandas as pd
import cx_Oracle
from datetime import datetime

####################################################### INITIALIZATION ###############################################################
# init the styles of fonts
title = '<p style="font-family:Arial Black; color:white; font-size: 300%; text-align: center;">Magnetic Measurements SPS Database 🧲💾</p>'


# Functions to connect to the databse and execute queries to get the data
def connect_to_oracle():
    oracle_username = st.secrets["db_username"]
    oracle_password = st.secrets["db_password"]   
    oracle_host = st.secrets["db_host"]
    oracle_port = st.secrets["db_port"]
    oracle_service_name = st.secrets["db_service_name"]

    try:
        connection = cx_Oracle.connect(
            f"{oracle_username}/{oracle_password}@{oracle_host}:{oracle_port}/{oracle_service_name}")
        return connection
    except cx_Oracle.Error as error:
        print(f"Error: {error}")
        return None

# Functions to connect to the databse and execute queries to get the data
def execute_query(connection):
    cursor = connection.cursor()

    try:
        # comment only for the dev of the app
        cursor.execute("ALTER TABLE SPS_SEP_COIL_ACQ NOCACHE")
        cursor.execute("SELECT * FROM SPS_SEP_COIL_ACQ")
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=column_names)

        # convert workorder to int
        df['WORKORDER_N'] = df['WORKORDER_N'].fillna(0).astype(int)
        # Convert the 'MEASUREMENT_DATE' column to datetime format
        df['MEASUREMENT_DATE'] = pd.to_datetime(df['MEASUREMENT_DATE'], format='%Y%m%d_%H%M%S', errors='coerce')
        # Convert the second date format
        df['MEASUREMENT_DATE'] = df['MEASUREMENT_DATE'].combine_first(pd.to_datetime(df['MEASUREMENT_DATE'], format='%Y-%m-%d', errors='coerce'))
        # Format the 'MEASUREMENT_DATE' column as required
        df['MEASUREMENT_DATE'] = df['MEASUREMENT_DATE'].dt.strftime("%H:%M   %d/%m/%Y")

        df['MAGNET_MEASURED'] = df['MAGNET_MEASURED'].apply(modify_string)
        df['MAGNET_REFERENCE'] = df['MAGNET_REFERENCE'].apply(modify_string)
        df['FLUXMETER_MEASURED'] = df['FLUXMETER_MEASURED'].apply(modify_string,)
        df['FLUXMETER_REFERENCE'] = df['FLUXMETER_REFERENCE'].apply(modify_string)

        return df
    
    finally:
        cursor.close()

# Functions to connect to the databse and execute queries to get the data
def dbconnect(oracle_path):

    # initialise the connection
    try:
        cx_Oracle.init_oracle_client(oracle_path)
    except:
        print("It is already initialised")

    # Initialize the database connection
    db_connection = connect_to_oracle()
    df = execute_query(db_connection)

    # Close the connection
    db_connection.close()        

    return df

# Calibrate the parameters for each magnet type
def magnet_calibration(mydf):

    # initialise the values for every magnet type
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

        if mydf['FLUXMETER_MEASURED'].str.contains("Q1|Q2|Q3|Q4").any():
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

    # Creating the dictionary
    st.session_state.kMeasCoil = {key: value for key, value in zip(['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9'], kMeasCoil)}

# Function to modify the string
def modify_string(replacements):
    return replacements.split(':')[-1].strip()

# insert empty spaces
def empty_line(lines_number):
    for i in range(lines_number):
        st.write("\n")

# add the streamlit logo
def add_logo(logo_url: str, height: int = 180):
    """Add a logo (from logo_url) on the top of the navigation page of a multipage app.
    Taken from https://discuss.streamlit.io/t/put-logo-and-title-above-on-top-of-page-navigation-in-sidebar-of-multipage-app/28213/6

    The url can either be a url to the image, or a local path to the image.

    Args:
        logo_url (str): URL/local path of the logo
    """

    try:
        if validators.url(logo_url):
            # If it's a URL, fetch the image
            response = requests.get(logo_url)
            response.raise_for_status()  # Raise an error if the request fails
            image = Image.open(BytesIO(response.content))
        else:
            # If it's a local file path, load the image
            image = Image.open(logo_url)
        
        # Convert the image to RGB format if it's RGBA
        if image.mode == "RGBA":
            image = image.convert("RGB")
        
        new_size = (200, 200)  # Replace with your desired dimensions
        resized_image = image.resize(new_size)
        
        # Convert the resized image to base64
        buffered = BytesIO()
        resized_image.save(buffered, format="PNG")
        base64_image = base64.b64encode(buffered.getvalue()).decode()

        logo = f"url(data:image/jpeg;base64,{base64_image})"

        st.markdown(
            f"""
            <style>
                [data-testid="stSidebarNav"] {{
                    background-image: {logo};
                    background-repeat: no-repeat;
                    padding-top: {height - 20}px;
                    background-position: +20px 25px;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.error(f"Error: {str(e)}")

# set background wallpaper and subtitle title & sidebar name
def add_bg_from_url(title):
    st.markdown(
        f"""
       <style>
       .stApp {{
       background-image: url("https://static.vecteezy.com/system/resources/previews/021/565/019/non_2x/minimalist-abstract-background-design-smooth-and-clean-subtle-background-vector.jpg");
       background-attachment: fixed;
       background-size: cover
       }}
       </style>
       """,
        unsafe_allow_html=True
    )
    add_logo("images//LogoBadge_Logo Badge.png")
    st.sidebar.markdown("# Magnetic Measurements  🧲 SPS Database 🖥️")
    # set the homepage style
    st.markdown(title, unsafe_allow_html=True)
    empty_line(2)

# Avg and stddev tables creation
def avg_stddev_tables(dataframe,coils_used):
    # Create two columns for arranging items side by side
    left_column, right_column = st.columns(2)
    
    # Average Flux of the coils for different current applied
    avg_data = dataframe.pivot_table(index='Current', values= coils_used, aggfunc='mean')
    avg_data_styler = avg_data.style.format("{:.6f}")

    # Stddev Flux of the coils for different current applied
    grouped_data = dataframe.groupby('Current')[coils_used].std()
    pivoted_data = grouped_data.reset_index().pivot_table(index='Current')
    stddev_data = pivoted_data.style.format("{:.6f}")

    with left_column:
        # for a specific workorder,date, etc 
        st.title("Average Flux")
        # Display the pivoted data
        st.dataframe(avg_data_styler, column_order= ('R5','M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9'))      

    with right_column:
        st.title("Stddev Flux")
        # Display the pivoted data
        st.dataframe(stddev_data, column_order= ('R5','M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9'))

    return avg_data

# Create an interactive dataframe presentation
def make_df(data, alldata):

    gb = GridOptionsBuilder.from_dataframe(data)
    if alldata:
        gb.configure_grid_options(pagination = True,alwaysShowHorizontalScroll = True)

    gb.configure_side_bar()  # Add a sidebar
    gb.configure_selection('multiple', use_checkbox=False, groupSelectsFiltered = True, groupSelectsChildren="Group checkbox select children")  # Enable multi-row selection
    gb.configure_auto_height(False)
    gridOptions = gb.build()

    grid_response = AgGrid(
        data,
        gridOptions=gridOptions,
        data_return_mode='FILTERED',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load= not alldata,
        theme='alpine',  # Add theme color to the table
        enable_enterprise_modules=True,
        height=850,
        width="Any",
    )
    return_data = grid_response['data']   

    df = pd.DataFrame(return_data)  # Pass the selected rows to a new dataframe df
    #df = df.iloc[:, 1:]

    return df

# Show the Correction results in a structured way
def show_results(current_applied, avg_data, coilMeasResistance, coils_used):

    fdiInputImpedance   = 400010
    # Initialize an empty dictionary to store DataFrames
    afcorrlist = []

    for current in current_applied:
        current_avg = avg_data.loc[avg_data.index == current]
                
        for coil in coils_used:
            bfr_corr = current_avg.loc[current,coil]
            aftr_corr = ((fdiInputImpedance + coilMeasResistance[coil])/ fdiInputImpedance) * bfr_corr
            
            # Create a dictionary for the current row of data
            row_data = {
                'Current':current,
                'Coil': coil,
                'Before Correction': bfr_corr,
                'After Correction': aftr_corr
            }
            # Append the row_data dictionary to the data_list
            afcorrlist.append(row_data)

    # Create a DataFrame from the data_list
    result_df = pd.DataFrame(afcorrlist)

    # Create a dropdown menu for selecting the "current" value
    row1 = row([0.3, 0.7], vertical_align="center")
    selected_current = row1.selectbox("Select a Current", current_applied)
    row1.write("")
    
    # Filter the DataFrame based on the selected "current"
    filtered_df = result_df[result_df['Current'] == selected_current].iloc[:, 1:]

    # Display the selected table
    st.header(f" Current {selected_current}:")
    st.dataframe(filtered_df, hide_index=1, width=600)

    return afcorrlist  