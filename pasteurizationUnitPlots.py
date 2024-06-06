import pandas as pd
import streamlit as st
import os
import altair as alt
import base64
from streamlit.components.v1 import html

# Application title
st.title("Visualization of Pasteurization Unit Data")

# Directory where the Excel files are located (relative path)
data_dir = "data"

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
def load_and_display_data(file_path, selected_input_vars, selected_output_vars, time_range):
    if os.path.exists(file_path):
        # Load data using the cached function
        df = load_data(file_path)

        # Filter data based on time range
        df = df[(df['Time'] >= time_range[0]) & (df['Time'] <= time_range[1])]

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

# Load data to get the time range
df = load_data(file_path)
min_time = df['Time'].min()
max_time = df['Time'].max()

# Add a range slider for the time axis
time_range = st.slider("Select time range [s]: ", min_value=float(min_time), max_value=float(max_time),
                       value=(float(min_time), float(max_time)))

# Load and display data based on selected time range
load_and_display_data(file_path, selected_input_variables, selected_output_variables, time_range)

# Display the image with interactive tooltips
st.subheader("Pasteurization Unit Diagram")

# Function to load image and convert to base64
def get_image_as_base64(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load the image and read HTML file
image_path = "pasteurizationUnit.png"
image_base64 = get_image_as_base64(image_path)

# Read the HTML file
html_file_path = "pasteurization_diagram.html"
with open(html_file_path, "r") as html_file:
    html_content = html_file.read().replace("{{image_base64}}", image_base64)

# Display the HTML content
html(html_content, height=1000)

