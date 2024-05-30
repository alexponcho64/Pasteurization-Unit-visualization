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
selected_variables = st.sidebar.multiselect(
    "Selecciona las variables para visualizar",
    ['Pc', 'Ph', 'Pf', 'T1', 'T2', 'T3', 'T4'],
    default=['Pc', 'Ph']
)


# Función para cargar y mostrar datos
def cargar_y_mostrar_datos(file_path, selected_variables):
    if os.path.exists(file_path):
        # Leer los datos del archivo Excel
        df = pd.read_excel(file_path)

        # Convertir la columna Time a datetime
        #df['Time'] = pd.to_datetime(df['Time'])

        # Mostrar el DataFrame cargado (opcional, para depuración)
        # st.write(df)

        # Gráfico de las variables seleccionadas
        if selected_variables:
            st.line_chart(df[['Time'] + selected_variables].set_index('Time'))
        else:
            st.warning("Por favor selecciona al menos una variable para visualizar.")
    else:
        st.warning(f"El archivo {file_path} no existe. Por favor verifica la ruta.")


# Mostrar la gráfica correspondiente al experimento y variables seleccionadas
experiment_title = f"Experimento: {selected_experiment}"
file_path = os.path.join(data_dir, files[selected_experiment])
st.subheader(experiment_title)
cargar_y_mostrar_datos(file_path, selected_variables)

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
