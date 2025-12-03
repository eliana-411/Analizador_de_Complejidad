import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from Backend.logic import  procesar_dato

st.title("Mi Proyecto Integrado con Streamlit")

nombre = st.text_input("Escribe tu nombre:")

if st.button("Procesar"):
    resultado = procesar_dato(nombre)
    st.success(resultado)
