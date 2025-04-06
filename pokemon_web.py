
import streamlit as st
import requests
from pathlib import Path

# Configuración de la página con favicon
st.set_page_config(
    page_title="Pokédex",
    page_icon=Path("assets/favicon.ico"),
    layout="centered"
)

# Pantalla de carga
with st.spinner("Cargando la Pokédex..."):
    st.markdown("""
        <div style='text-align: center;'>
            <img src="https://github.com/Vleick/pokedex-web/blob/main/assets/loading.gif?raw=true" width="120">
        </div>
    """, unsafe_allow_html=True)
    import time
    time.sleep(2)

# Aquí continúa tu app
st.title("🔵 Pokédex Web en Español")
