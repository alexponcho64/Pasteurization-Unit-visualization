import pandas as pd
import streamlit as st
import os
import altair as alt

# Application title
st.title("Visualization of Pasteurization Unit Data")

# Directory where the Excel files are located
data_dir = "C:/Users/Alejandro/PycharmProjects/bachelorThesis/data"

# Names of the Excel files for each experiment
files = {
    "Individual step responses": "ptc23_steps_1.xlsx",
    "Concurrent step responses": "ptc23_steps_2.xlsx",
    "Ramp responses": "ptc23_ramps.xlsx",
    "Responses to harmonic signals": "ptc23_harmon.xlsx"
}

# Sidebar configuration
st.sidebar.header("Chart Configuration")
selected_experiment = st.sidebar.selectbox("Select Experiment", list(files.keys()))

# Input and output variables
input_variables = ['Pc', 'Ph', 'Pf']
output_variables = ['T1', 'T2', 'T3', 'T4']

# Checkboxes to select input variables
st.sidebar.header("Select Input Variables (Power)")
selected_input_variables = []
for var in input_variables:
    if st.sidebar.checkbox(var, value=True):
        selected_input_variables.append(var)

# Checkboxes to select output variables
st.sidebar.header("Select Output Variables (Temperature)")
selected_output_variables = []
for var in output_variables:
    if st.sidebar.checkbox(var, value=True):
        selected_output_variables.append(var)


# Cache decorator to cache data loading
@st.cache_data
def load_data(file_path):
    # Read data from Excel file
    df = pd.read_excel(file_path)
    return df


# Function to load and display data
def load_and_display_data(file_path, selected_input_vars, selected_output_vars):
    if os.path.exists(file_path):
        # Load data using the cached function
        df = load_data(file_path)

        # Optionally display loaded DataFrame (for debugging)
        # st.write(df)

        # Chart of input variables (power)
        if selected_input_vars:
            st.subheader("Input Profiles (Power)")
            input_chart = alt.Chart(df).transform_fold(
                selected_input_vars,
                as_=['Variable', 'Value']
            ).mark_line().encode(
                x=alt.X('Time:Q', title='Time [s]'),
                y=alt.Y('Value:Q', title='Controlled inputs [%]'),
                color='Variable:N'
            ).interactive()
            st.altair_chart(input_chart, use_container_width=True)

        # Chart of output variables (temperature)
        if selected_output_vars:
            st.subheader("Output Profiles (Temperature)")
            output_chart = alt.Chart(df).transform_fold(
                selected_output_vars,
                as_=['Variable', 'Value']
            ).mark_line().encode(
                x=alt.X('Time:Q', title='Time [s]'),
                y=alt.Y('Value:Q', title='Process Outputs [%]'),
                color='Variable:N'
            ).interactive()
            st.altair_chart(output_chart, use_container_width=True)
    else:
        st.warning(f"The file {file_path} does not exist. Please verify the path.")


# Display the chart for the selected experiment
experiment_title = f"Experiment: {selected_experiment}"
file_path = os.path.join(data_dir, files[selected_experiment])
st.subheader(experiment_title)
load_and_display_data(file_path, selected_input_variables, selected_output_variables)

# Display information about the variables
st.subheader("Variable Descriptions")
st.markdown("""
- **T1**: Temperature of heated product (°C)
- **T2**: Temperature in the boiler (°C)
- **T3**: Temperature of cooled product (°C)
- **T4**: Temperature of heated feed (°C)
- **Pc**: Power of the coil heating the water in the boiler (%)
- **Ph**: Power of the pump delivering the heating water to the exchanger (%)
- **Pf**: Power of the pump supplying the raw material (%)
""")
