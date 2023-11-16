from PIL import Image
import requests
import streamlit as st
from streamlit_extras.stateful_button import button
import base64
from io import BytesIO
import validators  # You need to import the validators library
from st_aggrid import GridOptionsBuilder, AgGrid
import pandas as pd

####################################################### INITIALIZATION ###############################################################
# init the styles of fonts
homepage = '<p style="font-family:Arial Black; color:black; font-size: 200%;"><strong>Homepage 🏠</strong></p>'
comp = '<p style="font-family:Arial Black; color:#262730; font-size: 150%;"><strong>Chose competition🏆</strong></p>'
title = '<p style="font-family:Arial Black; color:white; font-size: 300%; text-align: center;">Magnetic Measurements SPS Database 🧲💾</p>'


# Function to modify the string
def modify_string(replacements):
    return replacements.split(':')[-1].strip()

# insert empty spaces
def empty_line(lines_number):
    for i in range(lines_number):
        st.write("\n")


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


def avg_stddev_tables(dataframe,coils_used):
    # Create two columns for arranging items side by side
    left_column, right_column = st.columns(2)
    
    # Average Flux of the coils for different current applied
    st.session_state.avg_data = dataframe.pivot_table(index='Current', values= coils_used, aggfunc='mean')
    average_data = st.session_state.avg_data.style.format("{:.6f}")

    # Stddev Flux of the coils for different current applied
    grouped_data = dataframe.groupby('Current')[coils_used].std()
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


