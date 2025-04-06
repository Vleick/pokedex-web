import streamlit as st
from pathlib import Path
import requests

# Configuración de la página con favicon
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
        # Extraer información del Pokémon
        nombre = data['name'].capitalize()
        imagen = data['sprites']['other']['official-artwork']['front_default']
        tipos = [t['type']['name'] for t in data['types']]
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        habilidades = [h['ability']['name'] for h in data['abilities']]

        # Mostrar imagen y datos del Pokémon
        st.image(imagen, width=200)
        st.subheader(nombre)

        tipo_html = " ".join([tipo_con_icono_box(t) for t in tipos])
        st.markdown(tipo_html, unsafe_allow_html=True)

        # Mostrar estadísticas
        st.write("**Estadísticas**:")
        for stat, value in stats.items():
            st.write(f"{stat.capitalize()}: {value}")

        # Mostrar habilidades
        st.write("**Habilidades**:")
        for habilidad in habilidades:
            st.write(f"- {habilidad.capitalize()}")

        # Cadena evolutiva
        url_evo = f"https://pokeapi.co/api/v2/pokemon-species/{nombre_pokemon.strip().lower()}"
        evo_data = requests.get(url_evo).json()
        if evo_data.get('evolution_chain'):
            evo_url = evo_data['evolution_chain']['url']
            evo_chain = requests.get(evo_url).json()

            st.write("**Cadena evolutiva:**")
            evolutions = [evo_chain['chain']]
            while 'evolves_to' in evolutions[-1]:
                evolutions.append(evolutions[-1]['evolves_to'][0])

            for evo in evolutions:
                st.write(f"🔄 {evo['species']['name'].capitalize()}")
