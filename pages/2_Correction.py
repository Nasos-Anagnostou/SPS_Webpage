import streamlit as st

from streamlit_extras.switch_page_button import switch_page
from custom_funct import *
from dbconnection import *
import pandas as pd


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
    df = df.iloc[:, 7:]
    
    if "Dipole" in basic_info['MAGNET_MEASURED']:
        print("This is a Dipole")
        coil_impedances = {
            "R5": 6384,
            "M1": 6409,
            "M2": 6361,
            "M3": 6397,
            "M4": 6399,
            "M5": 6366,
            "M6": 6357,
            "M7": 6364,
            "M8": 6368,
            "M9": 6363,
            "FDI": 400010
        }
        current_applied = (250, 1000, 2500, 4000, 4900)
        coils_used = ('R5', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9')
        impedance_img = "images/Impedance_dipole.png"

    elif "Quadrupole" in basic_info['MAGNET_MEASURED']:
        print("This is a Quadruple")
        coil_impedances = {
            "R5": 39519,
            "M2": 39651,
            "M3": 39655,
            "M4": 39658,
            "M5": 39547,
            "M6": 39556,
            "M7": 39623,
            "M8": 39734,
            "FDI": 400010
        }
        current_applied = (100, 400, 1000, 1540, 1938)
        coils_used = ('R5','M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8')
        impedance_img = "images/Impedance_quadrople.png"
    
    # Initialize an empty dictionary to store DataFrames
    result_dfs = {}
    data_list = []
    for current in current_applied:
        current_avg = avg_data.loc[avg_data.index == current]
        # Initialize an empty list to store data
        #data_list = []
                  
        for coil in coils_used:
            bfr_corr = current_avg.loc[current,coil]
            aftr_corr = ((coil_impedances["FDI"] + coil_impedances[coil])/ coil_impedances["FDI"]) * bfr_corr
            
            # Create a dictionary for the current row of data
            row_data = {
                'Current':current,
                'Coil': coil,
                'Before Correction': bfr_corr,
                'After Correction': aftr_corr
            }
            # Append the row_data dictionary to the data_list
            data_list.append(row_data)
        
        # # Create a DataFrame from the data_list
        # current_df  = pd.DataFrame(data_list)
        # # Store the DataFrame in the result_dfs dictionary with the current as the key
        # result_dfs[current] = current_df

    # Create a DataFrame from the data_list
    result_df = pd.DataFrame(data_list)

    # # Display each DataFrame in the result_dfs dictionary
    # for current, current_df in result_dfs.items():
    #     st.write(f"Data for Current {current}:")
    #     st.dataframe(current_df)

    # Create two columns for arranging items side by side
    left_column, right_column = st.columns(2)

    # Add content to the left column
    with left_column:

        # Create a dropdown menu for selecting the "current" value
        selected_current = st.selectbox("Select a Current", current_applied)
        # Filter the DataFrame based on the selected "current"
        filtered_df = result_df[result_df['Current'] == selected_current].iloc[:, 1:]

        # Display the selected table
        st.write(f" Current {selected_current}:")
        st.dataframe(filtered_df, hide_index=1, width=600)        

    # Add content to the right column
    with right_column:
        empty_line(5)
        st.write("Impedance of every coil")
        st.image(impedance_img)
        st.image("images/Correction_image.png")
       
else:
    print("No measurement information found in the DataFrame.")




