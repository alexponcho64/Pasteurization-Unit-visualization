import streamlit as st
import plotly.express as px
import pandas as pd
import os
import xlrd
import warnings

#Titulo y encabezado
st.set_page_config(page_title="Pateurization Unit", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Pasturization Unit")
st.markdown('<style>div.black-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

#Importar archivos
def load_data():
    df = pd.read_excel("ptc23_steps_1.xlsx")
