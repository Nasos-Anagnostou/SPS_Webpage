import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.row import row 
from custom_funct import *
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Initialization of the st.session variables
if "afcorrlist" not in st.session_state:
    st.session_state['afcorrlist'] = []

if "magnettype" not in st.session_state:
    st.session_state['magnettype'] = ""

if "mydf" not in st.session_state:
    st.session_state['mydf'] = None

if "coilMeasResistance" not in st.session_state:
    st.session_state['coilMeasResistance'] = {}

if "current_applied" not in st.session_state:
    st.session_state['current_applied'] = []

if "kRefCoil" not in st.session_state:
    st.session_state['kRefCoil'] = 0

if "kMeasCoil" not in st.session_state:
    st.session_state['kMeasCoil'] = None

if "coils_used" not in st.session_state:
    st.session_state['coils_used'] = []

if "avg_data" not in st.session_state:
    st.session_state['avg_data'] = None

if "impedance_img" not in st.session_state:
    st.session_state['impedance_img'] = ""

if "flag" not in st.session_state:
    st.session_state['flag'] = False


######################################## THE LAYOUT OF THE PAGE ###########################################
#config of the page
st.set_page_config(page_title="Magnetic Measurements SPS Database 🧲📏", page_icon="🧲", layout="wide",
                   initial_sidebar_state="expanded", menu_items=None)
# add background
add_bg_from_url(title)
######################################## THE LAYOUT OF THE PAGE ###########################################

# Check if there is data in the DataFrame
if st.session_state.flag:     

    font_css = """
    <style>
    button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
    font-size: 28px;
    }
    </style>
    """
    st.write(font_css, unsafe_allow_html=True)

    whitespace = 24
    ## Fills and centers each tab label with em-spaces
    #correction, tracking, homogeneity = st.tabs([s.center(whitespace,"\u2001") for s in ["Correction", "Tracking", "Homogeneity"]])
    correction, tracking, homogeneity = st.tabs(["Correction", "Tracking", "Homogeneity"])

    # Correction
    with correction:

        empty_line(2)
        # get the session state variables
        current_applied = st.session_state.current_applied
        coils_used = st.session_state.coils_used
        impedance_img = st.session_state.impedance_img
        kRefCoil = st.session_state.kRefCoil
        kMeasCoil = st.session_state.kMeasCoil
        avg_data = st.session_state.avg_data
        coilMeasResistance = st.session_state.coilMeasResistance

        # Define a radio button to select input method
        input_method = st.radio("Select Input Method", ["Default Values", "Custom Input"], horizontal= True)
        # Create two columns for arranging items side by side
        left_column, right_column = st.columns(2)
        
        # If the user selects "Custom Input," collect user inputs
        if input_method == "Custom Input":
            with left_column:
                with st.expander("Custom Coil Resistances"):
                    for coil_name in coilMeasResistance:
                        coilMeasResistance[coil_name] = st.number_input(f"{coil_name} Resistance", 0.0)
                
            with right_column:
                st.session_state.afcorrlist = show_results(current_applied, avg_data,
                                                           coilMeasResistance,coils_used)
                #     # Create a "Show Results" button
                #     if st.button("Show Results"):
                #         # Display the selected values
                        
        else:
            with left_column:
                st.session_state.afcorrlist = show_results(current_applied, avg_data, 
                                                           coilMeasResistance,coils_used)

            with right_column:
                st.header("Impedance of every coil")
                st.image(impedance_img)
                st.image("images/Correction_image.png")
        

    # Tracking
    with tracking:

        empty_line(2)
        # get the session state variables
        afcorrlist = st.session_state.afcorrlist
        current_applied = st.session_state.current_applied
        kRefCoil = st.session_state.kRefCoil
        kMeasCoil = st.session_state.kMeasCoil

        tracking_list = []

        for current in current_applied:
            # Extract 'After Correction' values where 'Coil' is 'R5' and 'M5'
            r5_aftcorr = [entry["After Correction"] for entry in afcorrlist if (entry["Coil"] == "R5" and entry["Current"] == current)]
            m5_aftercorr = [entry["After Correction"] for entry in afcorrlist if (entry["Coil"] == "M5" and entry["Current"] == current)]
            r5_aftcorr = r5_aftcorr[0]
            m5_aftercorr = m5_aftercorr[0]

            dVcorr = m5_aftercorr - r5_aftcorr
            dv_vref = 1000 * ( dVcorr / r5_aftcorr)
            dvcorr_vref = dv_vref - (1000* (kMeasCoil["M5"] - kRefCoil))

            # Creating a DataFrame
            data = {
                'Current': current,
                'R5': r5_aftcorr,
                'M5': m5_aftercorr,
                'M5-R5': dVcorr,
                '(Vmeas-Vref)/Vref   (E-3)': dv_vref,
                'dV/Vref corrected   (E-3)': dvcorr_vref
            }
            tracking_list.append(data)

        st.header("Tracking Results")
        df_tracking = pd.DataFrame(tracking_list)
        st.dataframe(df_tracking, hide_index=1, use_container_width=True)

        st.header("Line Charts for Magnetization Curve and Tracking")
        # Create two columns for arranging items side by side
        left_column, right_column = st.columns(2)

        with left_column:
            # Create a line chart using Plotly Express
            fig = px.line(df_tracking, x='Current', y='M5', title='Magnetization curve', markers= True, 
                        labels={'Current': 'Current in A', 'M5': 'Flux (V.s)'})
            fig.update_layout(title_x = 0.4)
            fig.update_traces(marker=dict(color='white', size=8))

            st.plotly_chart(fig)

        with right_column:
            # Create a line chart using Plotly Express
            fig = px.line(df_tracking, x='Current', y='dV/Vref corrected   (E-3)', title='Tracking', markers= True, 
                        labels={'Current': 'Current in A', 'M5': 'dG/G (E-3)'})
            fig.update_layout(title_x = 0.4)
            fig.update_traces(marker=dict(color='white', size=8))

            st.plotly_chart(fig)

    
    # Homogenity            
    with homogeneity:
        
        empty_line(2)
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
            # get rid of the irelevant data
            df_filtered = df_dvcorr[~df_dvcorr.index.isin(["M8 - M5", "M2 - M5"])]

        elif magnettype == "Dipole":
            df_dvcorr.insert(0, 'Position', [11, 44, -11, 25, 0, -25, 11, -44, -11]) #M1...M9
            # get rid of the irelevant data
            df_filtered = df_dvcorr[~df_dvcorr.index.isin(["M1 - M5", "M3 - M5", "M7 - M5", "M9 - M5"])]
        
        # Get column names and store in a list
        column_names = df_filtered.columns[1:].tolist()  # Exclude the 'Position' column


        left_column, right_column = st.columns(2)

        with left_column:
            #selected_table = st.selectbox("Select a Table", ("Mi-M5","Vmeas-Vref /Vref (E-3)", "Vmeas-Vref /Vref (E-3) corrected" ))
            st.header("Mi-M5")
            st.dataframe(df,use_container_width= True)
            
            
            
            st.header("Vmeas-Vref /Vref (E-4) corrected")
            st.dataframe(df_dvcorr,use_container_width= True)

        with right_column:
            st.header("Vmeas-Vref /Vref (E-4)")
            st.dataframe(df_dv,use_container_width= True)

            st.header("Homogeneity shown only for x-axis coils")
            # # Create Plotly figure
            # fig = px.line(df_filtered, x='Position', title='Homogeneity', markers=True,
            #             labels={'Position': 'Position of the coil with respect to the central coil (mm)', 'value':'dG/Gref (E-3)'})
            # # Add lines for each column in column_names
            # for col in column_names:
            #     fig.add_scatter(x=df_filtered['Position'], y=df_filtered[col], name=col)

            # fig.update_layout(title_x = 0.35, title_font =dict(size=30))
            # fig.update_layout(yaxis=dict(title=dict(text="dG/Gref (E-3)", font=dict(size=25))))

            # fig.update_yaxes(showticklabels=False)
            # st.plotly_chart(fig)

            # Create an empty figure
            fig = go.Figure()

            # Add lines for each column in column_names, each column is a current value

            for col in column_names:
                fig.add_trace(go.Scatter(
                    x=df_filtered['Position'], 
                    y=df_filtered[col], 
                    mode='lines+markers', 
                    name=col
                ))

            # Update layout
            fig.update_layout(
                title='Homogeneity',
                title_x=0.35,
                title_font=dict(size=30),
                xaxis_title='Position of the coil with respect to the central coil (mm)',
                yaxis_title='dG/Gref (E-4)',
                yaxis=dict(title_font=dict(size=25)),
            )

            # Optionally hide y-axis tick labels
            fig.update_yaxes(showticklabels=True)

            # Render the plot in Streamlit
            st.plotly_chart(fig)

else:
    empty_line(3)
    row1 = row([0.7, 0.6], vertical_align="bottom")
    row1.subheader("Please choose first the date or the workorder of the measurement.")
    if row1.button("Back to Home Page 🏠"):
        switch_page("Raw_data")



