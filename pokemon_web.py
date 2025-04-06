import streamlit as st
from pathlib import Path
import time
import requests

st.set_page_config(
    page_title="Pokédex",
    page_icon=Path("assets/favicon.ico"),
    layout="centered"
)

# Pantalla de carga con gif desde GitHub
st.markdown("""
    <div style="display:flex; justify-content:center; align-items:center; height:100vh;">
        <img src="https://github.com/Vleick/pokedex-web/blob/main/assets/loading.gif?raw=true" alt="loading gif">
    </div>
""", unsafe_allow_html=True)

# Simulación de carga
time.sleep(3)

# Borrar la pantalla de carga
st.empty()

# --- CONTINÚA TU CÓDIGO AQUÍ ABAJO ---
# Ejemplo de contenido para asegurar que la app carga
st.title("🧠 Pokédex Web en Español")
st.write("La aplicación se ha cargado correctamente después de la animación.")
