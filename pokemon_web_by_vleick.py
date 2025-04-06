
import streamlit as st
import requests
from pathlib import Path

st.set_page_config(
    page_title="Pokédex Web by Vleick",
    page_icon=Path("assets/favicon.ico"),
    layout="centered"
)

def main():
    st.markdown(
        "<h1 style='text-align: center;'>🔎 Pokédex Web <span style='font-family: Freestyle Script; font-size: 36px;'>by Vleick</span></h1>",
        unsafe_allow_html=True
    )
    
    st.text_input("Escribe el nombre de un Pokémon:")

if __name__ == "__main__":
    main()