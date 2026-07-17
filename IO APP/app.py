import streamlit as st
from scipy.optimize import linprog


st.set_page_config(
    page_title="Viaja Seguro",
    layout="wide"
)


# ==================================================================
# CONTROL DE NAVEGACIÓN ENTRE PÁGINAS
# ==================================================================

if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"


# ==================================================================
# BASE DE DATOS DE RUTAS (Ecuador - vuelos nacionales y Galápagos)
# ==================================================================
# Cada ruta incluye la información necesaria para:
# - Las tarjetas del menú (Rutas, Distancias, Tiempo, Costos)
# - El panel de monitoreo / Dashboard (simulación)

rutas = {
    "Quito - Guayaquil": {
        "costo": 250,
        "distancia": 270,
        "tiempo": 0.75,
        "combustible": 850,
        "escalas": 0,
        "estado": "A tiempo"
    },
    "Quito - Cuenca": {
        "costo": 220,
        "distancia": 320,
        "tiempo": 0.83,
        "combustible": 900,
        "escalas": 0,
        "estado": "A tiempo"
    },
    "Quito - Loja": {
        "costo": 280,
        "distancia": 420,
        "tiempo": 1.10,
        "combustible": 1100,
        "escalas": 0,
        "estado": "Retrasado"
    },
    "Quito - Baltra (Galápagos)": {
        "costo": 520,
        "distancia": 1000,
        "tiempo": 1.80,
        "combustible": 2200,
        "escalas": 1,
        "estado": "A tiempo"
    },
    "Quito - San Cristóbal (Galápagos)": {
        "costo": 560,
        "distancia": 1050,
        "tiempo": 1.90,
        "combustible": 2300,
        "escalas": 1,
        "estado": "A tiempo"
    },
    "Guayaquil - Baltra (Galápagos)": {
        "costo": 380,
        "distancia": 970,
        "tiempo": 1.70,
        "combustible": 2100,
        "escalas": 0,
        "estado": "A tiempo"
    },
    "Guayaquil - San Cristóbal (Galápagos)": {
        "costo": 420,
        "distancia": 1000,
        "tiempo": 1.80,
        "combustible": 2150,
        "escalas": 0,
        "estado": "En proceso"
    },
    "Guayaquil - Cuenca": {
        "costo": 190,
        "distancia": 200,
        "tiempo": 0.60,
        "combustible": 700,
        "escalas": 0,
        "estado": "A tiempo"
    },
    "Cuenca - Loja": {
        "costo": 170,
        "distancia": 150,
        "tiempo": 0.50,
        "combustible": 600,
        "escalas": 0,
        "estado": "A tiempo"
    }
}


# ==================================================================
# FUNCIÓN: OPTIMIZACIÓN CON MÉTODO SIMPLEX (linprog)
# ==================================================================

def optimizar_ruta_simplex(rutas_dict):
    """
    Resuelve el problema de selección de ruta óptima como un problema
    de programación lineal:

    Minimizar: costo total
    Sujeto a:  la suma de las variables de decisión = 1 (una sola ruta)
    Límites:   cada variable entre 0 y 1
    """

    nombres = list(rutas_dict.keys())
    c = [rutas_dict[nombre]["costo"] for nombre in nombres]

    # Restricción: elegir una sola ruta
    A_eq = [[1] * len(nombres)]
    b_eq = [1]

    # Límites de las variables
    bounds = [(0, 1) for _ in nombres]

    # Resolver con método simplex
    resultado = linprog(
        c,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds,
        method='highs'
    )

    indice = resultado.x.tolist().index(max(resultado.x))
    ruta_optima = nombres[indice]
    costo_minimo = resultado.fun

    return ruta_optima, costo_minimo, resultado


# ==================================================================
# PÁGINA 1: PORTADA / BIENVENIDA
# ==================================================================

def mostrar_portada():

    st.markdown("""
    <style>
    .stApp {
        background-color: #1976D2;
    }
    .titulo {
        text-align: center;
        color: white;
        font-size: 70px;
        font-weight: bold;
        margin-top: 200px;
    }
    .eslogan {
        text-align: center;
        color: white;
        font-size: 25px;
        margin-top: 10px;
        margin-bottom: 40px;
    }
    div.stButton > button {
        display: block;
        margin: auto;
        background-color: white;
        color: #1976D2;
        font-size: 22px;
        font-weight: bold;
        border-radius: 12px;
        padding: 10px 40px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="titulo">Bienvenidos</div>', unsafe_allow_html=True)
    st.markdown('<div class="eslogan">Viaja seguro y tranquilo</div>', unsafe_allow_html=True)

    if st.button("Inicio"):
        st.session_state.pagina = "menu"
        st.rerun()


# ==================================================================
# PÁGINA 2: MENÚ PRINCIPAL (VIAJA SEGURO)
# ==================================================================

def mostrar_menu():

    st.markdown("""
    <style>
    .stApp{
        background: linear-gradient(135deg,#004e92,#1e88e5,#90caf9);
    }
    .titulo{
        color:white;
        text-align:center;
        font-size:55px;
        font-weight:bold;
    }
    .subtitulo{
        color:white;
        text-align:center;
        font-size:22px;
    }
    .card{
        background:white;
        padding:25px;
        border-radius:20px;
        text-align:center;
        height:180px;
        box-shadow:0px 5px 15px rgba(0,0,0,0.25);
    }
    .texto{
        color:#0d47a1;
        font-size:25px;
        font-weight:bold;
    }
    .descripcion{
        color:#555;
        font-size:17px;
    }
    .stButton button{
        background:#0d47a1;
        color:white;
        border-radius:12px;
        width:100%;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="titulo">
    VIAJA SEGURO
    </div>
    <div class="subtitulo">
    Sistema inteligente de gestión y optimización de rutas aéreas del Ecuador
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # ---------------- PRIMERA FILA ----------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <div class="texto">
        Aeropuertos
        </div>
        <div class="descripcion">
        Aeropuertos principales del Ecuador y Galápagos
        </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Consultar aeropuertos"):
            st.write("""
            Aeropuerto Mariscal Sucre - Quito
            Aeropuerto José Joaquín de Olmedo - Guayaquil
            Aeropuerto Mariscal Lamar - Cuenca
            Aeropuerto Seymour - Baltra
            Aeropuerto San Cristóbal
            """)

    with col2:
        st.markdown("""
        <div class="card">
        <div class="texto">
        Rutas
        </div>
        <div class="descripcion">
        Rutas aéreas nacionales y hacia Galápagos
        </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Consultar rutas"):
            for ruta, datos in rutas.items():
                st.write(ruta + " - Costo estimado: $" + str(datos["costo"]))

    with col3:
        st.markdown("""
        <div class="card">
        <div class="texto">
        Optimización
        </div>
        <div class="descripcion">
        Determina la ruta con menor costo
        </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Calcular costo mínimo"):
            costos_simples = {r: d["costo"] for r, d in rutas.items()}
            ruta_menor = min(costos_simples, key=costos_simples.get)
            costo = costos_simples[ruta_menor]
            st.success(
                "Ruta óptima: " + ruta_menor
                + " | Costo mínimo: $" + str(costo)
            )

    # ---------------- SEGUNDA FILA ----------------
    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
        <div class="card">
        <div class="texto">
        Distancias
        </div>
        <div class="descripcion">
        Distancia aproximada entre destinos
        </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ver distancias"):
            for ruta, datos in rutas.items():
                st.write(ruta + ": " + str(datos["distancia"]) + " km")

    with col5:
        st.markdown("""
        <div class="card">
        <div class="texto">
        Tiempo
        </div>
        <div class="descripcion">
        Duración estimada de vuelos
        </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ver tiempos"):
            for ruta, datos in rutas.items():
                horas = datos["tiempo"]
                st.write(ruta + ": " + str(horas) + " h")

    with col6:
        st.markdown("""
        <div class="card">
        <div class="texto">
        Costos
        </div>
        <div class="descripcion">
        Comparación económica de rutas
        </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ver costos"):

            st.write("Análisis de restricciones - Programación lineal (Simplex)")

            ruta_optima, costo_minimo, resultado = optimizar_ruta_simplex(rutas)

            st.info("Costo mínimo encontrado: $" + str(costo_minimo))
            st.success("Ruta seleccionada: " + ruta_optima)

            with st.expander("Ver detalle de costos por ruta"):
                for ruta, datos in rutas.items():
                    st.write(ruta + ": $" + str(datos["costo"]))

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("Panel de monitoreo (Dashboard)"):
            st.session_state.pagina = "monitoreo"
            st.rerun()

    with col_b:
        if st.button("Volver a la portada"):
            st.session_state.pagina = "inicio"
            st.rerun()


# ==================================================================
# PÁGINA 3: PANEL DE MONITOREO / DASHBOARD (SIMULACIÓN - ECUADOR)
# ==================================================================

def mostrar_dashboard():

    st.markdown("""
    <style>
    .stApp{
        background: linear-gradient(135deg,#0d1b2a,#1b263b,#415a77);
    }
    .titulo-dash{
        color:white;
        text-align:center;
        font-size:45px;
        font-weight:bold;
    }
    .subtitulo-dash{
        color:#cbd5e1;
        text-align:center;
        font-size:20px;
        margin-bottom:30px;
    }
    div[data-testid="stMetric"] {
        background-color: white;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.25);
    }
    .stButton button{
        background:#0d47a1;
        color:white;
        border-radius:12px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="titulo-dash">Panel de Monitoreo</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitulo-dash">Simulación de indicadores de vuelo dentro del Ecuador</div>',
        unsafe_allow_html=True
    )

    ruta_seleccionada = st.selectbox("Seleccione una ruta:", list(rutas.keys()))

    datos = rutas[ruta_seleccionada]

    st.write("")

    fila1_col1, fila1_col2, fila1_col3 = st.columns(3)
    fila1_col1.metric("Distancia total", str(datos["distancia"]) + " km")
    fila1_col2.metric("Tiempo estimado", str(datos["tiempo"]) + " h")
    fila1_col3.metric("Consumo de combustible", str(datos["combustible"]) + " L")

    fila2_col1, fila2_col2, fila2_col3 = st.columns(3)
    fila2_col1.metric("Costo del recorrido", "$" + str(datos["costo"]))
    fila2_col2.metric("Número de escalas", str(datos["escalas"]))
    fila2_col3.metric("Estado del vuelo", datos["estado"])

    st.divider()

    if st.button("Volver al menú"):
        st.session_state.pagina = "menu"
        st.rerun()


# ==================================================================
# ENRUTADOR PRINCIPAL
# ==================================================================

if st.session_state.pagina == "inicio":
    mostrar_portada()

elif st.session_state.pagina == "menu":
    mostrar_menu()

elif st.session_state.pagina == "monitoreo":
    mostrar_dashboard()
