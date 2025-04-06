
import streamlit as st
import requests
from pathlib import Path

st.set_page_config(
    page_title="Pokédex Web by Vleick",
    page_icon=Path("assets/favicon.ico"),
    layout="centered"
)

# Diccionario de tipos con iconos
type_data = {
    'normal': ('Normal', '⚪'),
    'fire': ('Fuego', '🔥'),
    'water': ('Agua', '💧'),
    'electric': ('Eléctrico', '⚡'),
    'grass': ('Planta', '🌿'),
    'ice': ('Hielo', '❄️'),
    'fighting': ('Lucha', '🥊'),
    'poison': ('Veneno', '☠️'),
    'ground': ('Tierra', '🌎'),
    'flying': ('Volador', '🕊️'),
    'psychic': ('Psíquico', '🔮'),
    'bug': ('Bicho', '🐛'),
    'rock': ('Roca', '🪨'),
    'ghost': ('Fantasma', '👻'),
    'dragon': ('Dragón', '🐉'),
    'dark': ('Siniestro', '🌑'),
    'steel': ('Acero', '⚙️'),
    'fairy': ('Hada', '✨')
}

def tipo_con_icono(tipo):
    nombre, icono = type_data.get(tipo.lower(), (tipo.capitalize(), '?'))
    return f"{icono} {nombre}"

def tipo_con_icono_box(tipo):
    nombre, icono = type_data.get(tipo.lower(), (tipo.capitalize(), ''))
    return f"<span style='padding:4px 8px; background-color:#222; border-radius:8px; margin-right:6px; display:inline-block'>{icono} {nombre}</span>"

def get_pokemon_data(nombre):
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre.strip().lower()}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Título con fuente personalizada
st.markdown(
    "<h1 style='text-align: center;'>🔎 Pokédex Web <span style='font-family: Freestyle Script; font-size: 36px;'>by Vleick</span></h1>",
    unsafe_allow_html=True
)

# Campo de búsqueda
nombre_pokemon = st.text_input("Escribe el nombre de un Pokémon:")

if nombre_pokemon:
    data = get_pokemon_data(nombre_pokemon)
    if not data:
        st.error("Pokémon no encontrado. Intenta con otro nombre.")
    else:
        nombre = data['name'].capitalize()
        imagen = data['sprites']['other']['official-artwork']['front_default']
        tipos = [t['type']['name'] for t in data['types']]
        
        st.image(imagen, width=200)
        st.subheader(nombre)
        tipo_html = " ".join([tipo_con_icono_box(t) for t in tipos])
        st.markdown(tipo_html, unsafe_allow_html=True)
