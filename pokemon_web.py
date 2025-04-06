import streamlit as st
from pathlib import Path
import requests
import time

st.set_page_config(
    page_title="Pokédex Web",
    page_icon=Path("assets/favicon.ico"),
    layout="centered"
)

# Mostrar gif en un contenedor temporal
loader = st.empty()
loader.markdown("""
    <div style="display:flex; justify-content:center; align-items:center; height:100vh;">
        <img src="https://github.com/Vleick/pokedex-web/blob/main/assets/loading.gif?raw=true" width="120">
    </div>
""", unsafe_allow_html=True)

# Simular carga
time.sleep(2)

# Borrar el gif
loader.empty()

# Contenido de la Pokédex
st.title("🔍 Pokédex Web en Español")
st.write("¡La app está lista!")
