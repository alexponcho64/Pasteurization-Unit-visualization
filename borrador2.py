import pandas as pd
import streamlit as st
import os

# Título de la aplicación
st.title("Visualización de Datos de la Unidad de Pasteurización")

# Directorio donde se encuentran los archivos Excel
data_dir = "C:/Users/Alejandro/PycharmProjects/bachelorThesis/data"

# Nombres de los archivos Excel para cada experimento
files = {
    "Individual step responses": "ptc23_steps_1.xlsx",
    "Concurrent step responses": "ptc23_steps_2.xlsx",
    "Ramp responses": "ptc23_ramps.xlsx",
    "Responses to harmonic signals": "ptc23_harmon.xlsx"
}

# Configuración de la barra lateral
st.sidebar.header("Configuración del gráfico")
selected_experiment = st.sidebar.selectbox("Selecciona el experimento", list(files.keys()))

# Variables de entrada y salida
input_variables = ['Pc', 'Ph', 'Pf']
output_variables = ['T1', 'T2', 'T3', 'T4']

# Checkboxes para seleccionar variables de entrada
st.sidebar.header("Selecciona las variables de entrada (potencias)")
selected_input_variables = []
for var in input_variables:
    if st.sidebar.checkbox(var, value=True):
        selected_input_variables.append(var)

# Checkboxes para seleccionar variables de salida
st.sidebar.header("Selecciona las variables de salida (temperaturas)")
selected_output_variables = []
for var in output_variables:
    if st.sidebar.checkbox(var, value=True):
        selected_output_variables.append(var)


# Decorador @st.cache_data para almacenar en caché la carga de datos
@st.cache_data
def cargar_datos(file_path):
    # Leer los datos del archivo Excel
    df = pd.read_excel(file_path)
    return df


# Función para cargar y mostrar datos
def cargar_y_mostrar_datos(file_path, selected_input_vars, selected_output_vars):
    if os.path.exists(file_path):
        # Cargar datos usando la función almacenada en caché
        df = cargar_datos(file_path)

        # Convertir la columna Time a datetime
        #df['Time'] = pd.to_datetime(df['Time'])

        # Mostrar los DataFrame cargados (opcional, para depuración)
        # st.write(df)

        # Gráfico de las variables de entrada (potencias)
        if selected_input_vars:
            st.subheader("Input Profiles (Potencias)")
            st.line_chart(df[['Time'] + selected_input_vars].set_index('Time'))

        # Gráfico de las variables de salida (temperaturas)
        if selected_output_vars:
            st.subheader("Output Profiles (Temperaturas)")
            st.line_chart(df[['Time'] + selected_output_vars].set_index('Time'))
    else:
        st.warning(f"El archivo {file_path} no existe. Por favor verifica la ruta.")


# Mostrar la gráfica correspondiente al experimento seleccionado
experiment_title = f"Experimento: {selected_experiment}"
file_path = os.path.join(data_dir, files[selected_experiment])
st.subheader(experiment_title)
cargar_y_mostrar_datos(file_path, selected_input_variables, selected_output_variables)

# Mostrar información sobre las variables
st.subheader("Descripción de las Variables")
st.markdown("""
- **T1**: Temperatura del producto calentado (°C)
- **T2**: Temperatura en la caldera (°C)
- **T3**: Temperatura del producto enfriado (°C)
- **T4**: Temperatura del material alimentado calentado (°C)
- **Pc**: Potencia de la bobina que calienta el agua en la caldera (%)
- **Ph**: Potencia de la bomba que entrega el agua de calentamiento al intercambiador (%)
- **Pf**: Potencia de la bomba que suministra la materia prima (%)
""")
