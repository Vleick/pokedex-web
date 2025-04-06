import streamlit as st
from pathlib import Path
st.set_page_config(
page_title="Pokédex Web",
page_icon=Path("assets/favicon.ico"),
layout="centered"
)

import requests

# Configuración de la página con favicon
page_title="Pokédex",
page_icon=Path("assets/favicon.ico")


# Traducción y emoji de tipos
type_data = {
    'normal':  ('Normal', '⚪'), 'fire':     ('Fuego', '🔥'), 'water':   ('Agua', '🌊'),
    'electric': ('Eléctrico', '⚡'), 'grass':    ('Planta', '🌿'), 'ice':     ('Hielo', '❄️'),
    'fighting': ('Lucha', '🥊'), 'poison':   ('Veneno', '☠️'), 'ground':  ('Tierra', '⛰️'),
    'flying':   ('Volador', '🕊️'), 'psychic':  ('Psíquico', '🧠'), 'bug':     ('Bicho', '🐛'),
    'rock':     ('Roca', '🪨'), 'ghost':    ('Fantasma', '👻'), 'dragon':  ('Dragón', '🐉'),
    'dark':     ('Siniestro', '🌑'), 'steel':    ('Acero', '🛡️'), 'fairy':   ('Hada', '✨')
}

def tipo_con_icono(tipo):
    nombre, icono = type_data.get(tipo.lower(), (tipo.capitalize(), '❔'))
    return f"{icono} {nombre}"

def tipo_con_icono_box(tipo):
    nombre, icono = type_data.get(tipo.lower(), (tipo.capitalize(), ''))
    return f"<span style='padding:4px 8px; background-color:#222; border-radius:8px; margin-right:6px; display:inline-block;'>{icono} {nombre}</span>"

@st.cache_data
def traducir_movimiento(nombre_mov):
    url = f"https://pokeapi.co/api/v2/move/{nombre_mov}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        nombre_es = next((n['name'] for n in data['names'] if n['language']['name'] == 'es'), nombre_mov)
        return nombre_es
    return nombre_mov.replace('-', ' ').title()

def get_pokemon_data(nombre_raw):
    nombre = nombre_raw.strip().lower()
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nombre}")
    if r.status_code != 200:
        return None
    data = r.json()

    tipos = [t['type']['name'] for t in data['types']]
    imagen = data['sprites']['other']['official-artwork']['front_default']

    stats = {s['stat']['name']: s['base_stat'] for s in data['stats']}
    nombres_stats = {
        'hp': 'Salud', 'attack': 'Ataque', 'defense': 'Defensa',
        'special-attack': 'At. Esp.', 'special-defense': 'Def. Esp.', 'speed': 'Velocidad'
    }
    stats_es = {nombres_stats[k]: v for k, v in stats.items()}
    total_stats = sum(stats.values())

    # Debilidades y resistencias
    type_chart = {
        'normal': {'weak': ['fighting'], 'resist': []},
        'fire': {'weak': ['water', 'rock', 'ground'], 'resist': ['fire', 'grass', 'ice', 'bug', 'steel', 'fairy']},
        'water': {'weak': ['electric', 'grass'], 'resist': ['fire', 'water', 'ice', 'steel']},
        'electric': {'weak': ['ground'], 'resist': ['electric', 'flying', 'steel']},
        'grass': {'weak': ['fire', 'ice', 'poison', 'flying', 'bug'], 'resist': ['water', 'electric', 'grass', 'ground']},
        'ice': {'weak': ['fire', 'fighting', 'rock', 'steel'], 'resist': ['ice']},
        'fighting': {'weak': ['flying', 'psychic', 'fairy'], 'resist': ['bug', 'rock', 'dark']},
        'poison': {'weak': ['ground', 'psychic'], 'resist': ['grass', 'fighting', 'poison', 'bug', 'fairy']},
        'ground': {'weak': ['water', 'ice', 'grass'], 'resist': ['poison', 'rock']},
        'flying': {'weak': ['electric', 'ice', 'rock'], 'resist': ['grass', 'fighting', 'bug']},
        'psychic': {'weak': ['bug', 'ghost', 'dark'], 'resist': ['fighting', 'psychic']},
        'bug': {'weak': ['fire', 'flying', 'rock'], 'resist': ['grass', 'fighting', 'ground']},
        'rock': {'weak': ['water', 'grass', 'fighting', 'ground', 'steel'], 'resist': ['normal', 'fire', 'poison', 'flying']},
        'ghost': {'weak': ['ghost', 'dark'], 'resist': ['poison', 'bug']},
        'dragon': {'weak': ['ice', 'dragon', 'fairy'], 'resist': ['fire', 'water', 'electric', 'grass']},
        'dark': {'weak': ['fighting', 'bug', 'fairy'], 'resist': ['ghost', 'dark']},
        'steel': {'weak': ['fire', 'fighting', 'ground'], 'resist': ['normal', 'grass', 'ice', 'flying', 'psychic', 'bug', 'rock', 'dragon', 'steel', 'fairy']},
        'fairy': {'weak': ['poison', 'steel'], 'resist': ['fighting', 'bug', 'dark']}
    }

    debil = set()
    resiste = set()
    for tipo in tipos:
        debil.update(type_chart.get(tipo, {}).get('weak', []))
        resiste.update(type_chart.get(tipo, {}).get('resist', []))

    # Movimientos
    movimientos_nivel = []
    movimientos_mt = []
    for move in data['moves']:
        for v in move['version_group_details']:
            if v['version_group']['name'] == 'scarlet-violet':
                if v['move_learn_method']['name'] == 'level-up':
                    nombre_es = traducir_movimiento(move['move']['name'])
                    movimientos_nivel.append((nombre_es, v['level_learned_at']))
                elif v['move_learn_method']['name'] == 'machine':
                    nombre_es = traducir_movimiento(move['move']['name'])
                    movimientos_mt.append(nombre_es)
    movimientos_nivel = sorted(movimientos_nivel, key=lambda x: x[1])

    # Generación y evolución
    species_url = data['species']['url']
    s = requests.get(species_url).json()
    generacion = s['generation']['name'].replace('-', ' ').title()
    regiones = {
        'generation-i': 'Kanto', 'generation-ii': 'Johto', 'generation-iii': 'Hoenn',
        'generation-iv': 'Sinnoh', 'generation-v': 'Unova', 'generation-vi': 'Kalos',
        'generation-vii': 'Alola', 'generation-viii': 'Galar', 'generation-ix': 'Paldea'
    }
    region = regiones.get(s['generation']['name'], 'Desconocida')

    # Evoluciones
    evo_url = s['evolution_chain']['url']
    cadena = requests.get(evo_url).json()['chain']
    def extraer_cadena(nodo):
        evoluciones = []
        while nodo:
            nombre = nodo['species']['name']
            metodo = ""
            if nodo['evolution_details']:
                detalle = nodo['evolution_details'][0]
                if detalle.get('min_level'):
                    metodo = f"Nivel {detalle['min_level']}"
                elif detalle.get('item'):
                    metodo = f"Usar {detalle['item']['name'].replace('-', ' ').title()}"
                elif detalle.get('trigger', {}).get('name') == 'trade':
                    metodo = "Intercambio"
                else:
                    metodo = detalle.get('trigger', {}).get('name', '').title()
            evoluciones.append((nombre, metodo))
            nodo = nodo['evolves_to'][0] if nodo['evolves_to'] else None
        return evoluciones

    evoluciones = extraer_cadena(cadena)
    imagenes_evo = []
    for nombre_evo, metodo in evoluciones:
        r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nombre_evo}").json()
        img = r['sprites']['front_default']
        imagenes_evo.append((nombre_evo, img, metodo))

    return {
        "nombre": nombre.capitalize(),
        "tipos": tipos,
        "imagen": imagen,
        "stats": stats_es,
        "total_stats": total_stats,
        "debil": list(debil),
        "resiste": list(resiste),
        "movimientos_nivel": movimientos_nivel,
        "movimientos_mt": movimientos_mt,
        "generacion": generacion,
        "region": region,
        "evoluciones": imagenes_evo
    }

# Interfaz principal
st.title("🔎 Pokédex Web en Español")

params = st.query_params
nombre = params.get("pokemon")
if isinstance(nombre, list):
    nombre = nombre[0]

nombre = st.text_input("Escribe el nombre de un Pokémon:", value=nombre or "")

if nombre:
    st.query_params["pokemon"] = nombre.lower()
    datos = get_pokemon_data(nombre)
    if datos:
        st.image(datos["imagen"], width=200)
        st.header(f"✅ {datos['nombre']}")
        st.markdown(f"**Tipo(s):** {' / '.join([tipo_con_icono(t) for t in datos['tipos']])}", unsafe_allow_html=True)
        st.markdown(f"🌍 **Región:** {datos['region']} · **Generación:** {datos['generacion']}")

        st.markdown("**❌ Débil contra:**")
        st.markdown("".join([tipo_con_icono_box(t) for t in datos['debil']]), unsafe_allow_html=True)

        st.markdown("**🛡️ Resiste:**")
        st.markdown("".join([tipo_con_icono_box(t) for t in datos['resiste']]), unsafe_allow_html=True)

        st.subheader("📊 Estadísticas base")
        for stat, val in datos['stats'].items():
            st.text(f"{stat}: {val}")
        st.text(f"🔢 Total: {datos['total_stats']}")

        st.subheader("🔁 Cadena evolutiva")
        cols = st.columns(len(datos['evoluciones']))
        for i, (nombre_evo, img, metodo) in enumerate(datos['evoluciones']):
            with cols[i]:
                link = f"?pokemon={nombre_evo}"
                st.markdown(f"<a href='{link}'><img src='{img}' width='80'></a>", unsafe_allow_html=True)
                st.caption(nombre_evo.capitalize())
                if metodo:
                    st.caption(f"➡️ {metodo}")

        with st.expander("📘 Mostrar movimientos por nivel"):
            for mov, lvl in datos['movimientos_nivel']:
                st.markdown(f"- Nivel {lvl}: `{mov}`")

        with st.expander("💿 Mostrar movimientos por MT (traducción lenta)"):
            for mov in datos['movimientos_mt'][:30]:
                st.markdown(f"- `{mov}`")
    else:
        st.error("Pokémon no encontrado.")