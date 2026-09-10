import os
import random

import streamlit as st
import google.generativeai as genai

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    plt = None
    np = None

# ---------------------------------------------------------------------
# 1. Configuración de la API Key
# ---------------------------------------------------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Error: Revisa la configuración de GOOGLE_API_KEY en los Secrets de Streamlit.")
    st.stop()

# ---------------------------------------------------------------------
# 2. Apariencia
# ---------------------------------------------------------------------
APP_TITLE = "Lumina Spark Explorer"
APP_ICON = "🧠"
LOGO_PATH = "logo.png"

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

if os.path.exists(LOGO_PATH):
    st.image(LOGO_PATH, width=180)

# ---------------------------------------------------------------------
# 3. Catálogos de cualidades (24 por persona), agrupadas por color
#    Cada índice de CUALIDADES_POSITIVAS corresponde al mismo color y
#    grupo que su "sombra" en DESCARRILADORES — así el radar final
#    compara exactamente los mismos 4 colores entre las 3 personas.
# ---------------------------------------------------------------------
CUALIDADES_POSITIVAS = [
    {"nombre": "Complaciente", "desc": "Busca armonía y está dispuesto a ajustar su posición en un conflicto.", "color": "Verde"},
    {"nombre": "Colaborador", "desc": "Juega en equipo con mentalidad ganar/ganar.", "color": "Verde"},
    {"nombre": "Empático", "desc": "Considerado y en contacto con los sentimientos de los otros.", "color": "Verde"},
    {"nombre": "Íntimo", "desc": "Escucha primero y se inclina hacia conversaciones uno a uno.", "color": "Verde"},
    {"nombre": "Observador", "desc": "Reservado y energizado por su mundo interior.", "color": "Verde"},
    {"nombre": "Mesurado", "desc": "Serio y contiene las emociones positivas.", "color": "Verde"},
    {"nombre": "Adaptable", "desc": "Trabaja con pasión en objetivos emergentes.", "color": "Amarillo"},
    {"nombre": "Flexible", "desc": "Relajado e informal.", "color": "Amarillo"},
    {"nombre": "Espontáneo", "desc": "Toma rápidas decisiones espontáneas.", "color": "Amarillo"},
    {"nombre": "Conceptual", "desc": "Un pensador abstracto cómodo con la complejidad y la ambigüedad.", "color": "Amarillo"},
    {"nombre": "Imaginativo", "desc": "Una fuente de ideas nuevas y creativas.", "color": "Amarillo"},
    {"nombre": "Radical", "desc": "Abraza el cambio y está dispuesto a desafiar la tradición.", "color": "Amarillo"},
    {"nombre": "Sociable", "desc": "Amigable y energizado por interactuar con otros.", "color": "Rojo"},
    {"nombre": "Expresivo", "desc": "Entusiasta y expresa emociones positivas.", "color": "Rojo"},
    {"nombre": "Se hace cargo", "desc": "Toma la iniciativa en un grupo y prefiere posiciones de autoridad.", "color": "Rojo"},
    {"nombre": "Duro", "desc": "Discute fuertemente y está a gusto con el conflicto.", "color": "Rojo"},
    {"nombre": "Competitivo", "desc": "Muy decidido, con una mentalidad ganar/perder.", "color": "Rojo"},
    {"nombre": "Lógico", "desc": "Objetivo y aplica rigurosamente la razón.", "color": "Rojo"},
    {"nombre": "Determinado", "desc": "Establece objetivos ambiciosos y luego trabaja diligentemente para alcanzarlos.", "color": "Azul"},
    {"nombre": "Estructurado", "desc": "Un planeador organizado y efectivo.", "color": "Azul"},
    {"nombre": "Confiable", "desc": "Disciplinado y cumple sus compromisos.", "color": "Azul"},
    {"nombre": "Práctico", "desc": "Adopta un enfoque realista y con sentido común.", "color": "Azul"},
    {"nombre": "Basado en la evidencia", "desc": "Enfocado en hechos observables y atento a los detalles.", "color": "Azul"},
    {"nombre": "Cauteloso", "desc": "Resiste el cambio - prefiere los métodos probados.", "color": "Azul"},
]

DESCARRILADORES = [
    {"nombre": "Condescendiente", "desc": "Puede parecer excesivamente sumiso o carente de opinión propia bajo presión.", "color": "Verde"},
    {"nombre": "Obsesionado por el consenso", "desc": "Dificultad para avanzar sin la aprobación unánime de todos.", "color": "Verde"},
    {"nombre": "Sobreemocional", "desc": "Las emociones de los demás le afectan tanto que pierde la objetividad.", "color": "Verde"},
    {"nombre": "Pasivo", "desc": "Se retrae tanto que deja de participar o aportar valor.", "color": "Verde"},
    {"nombre": "Distante e indiferente", "desc": "Parece desconectado o poco interesado en lo que sucede a su alrededor.", "color": "Verde"},
    {"nombre": "Serio y retraído", "desc": "Su falta de expresividad resulta inquietante o fría para los demás.", "color": "Verde"},
    {"nombre": "Falto de enfoque", "desc": "Cambia de rumbo tan seguido que no termina lo que empieza.", "color": "Amarillo"},
    {"nombre": "Caótico", "desc": "La falta de estructura genera desorden e ineficiencia extrema.", "color": "Amarillo"},
    {"nombre": "Impulsivo", "desc": "Actúa sin pensar en las consecuencias a largo plazo.", "color": "Amarillo"},
    {"nombre": "Impráctico", "desc": "Se pierde en la teoría y olvida la ejecución real.", "color": "Amarillo"},
    {"nombre": "Fantasioso", "desc": "Sus ideas están tan alejadas de la realidad que son inviables.", "color": "Amarillo"},
    {"nombre": "Cambiar por cambiar", "desc": "Destruye lo que funciona solo por el deseo de novedad.", "color": "Amarillo"},
    {"nombre": "No poder estar solo", "desc": "Necesita atención constante de los demás para funcionar.", "color": "Rojo"},
    {"nombre": "Avasallador", "desc": "Su intensidad emocional invade el espacio de los demás.", "color": "Rojo"},
    {"nombre": "Controlador", "desc": "Impone su voluntad sin escuchar otras opiniones.", "color": "Rojo"},
    {"nombre": "Conflictivo", "desc": "Busca la confrontación innecesaria y es agresivo.", "color": "Rojo"},
    {"nombre": "Ganar a toda costa", "desc": "Abandona la ética con tal de no ser derrotado.", "color": "Rojo"},
    {"nombre": "Discutidor", "desc": "Usa la lógica como un arma para humillar o invalidar a otros.", "color": "Rojo"},
    {"nombre": "Obsesionado por los objetivos", "desc": "Ignora el bienestar humano con tal de alcanzar la meta.", "color": "Azul"},
    {"nombre": "Planeación rígida", "desc": "Incapaz de reaccionar si algo sale del plan original.", "color": "Azul"},
    {"nombre": "Indeciso", "desc": "Tanta precaución por cumplir bien que se bloquea al decidir.", "color": "Azul"},
    {"nombre": "Visión estrecha", "desc": "Rechaza cualquier idea nueva que no sea inmediatamente obvia.", "color": "Azul"},
    {"nombre": "Perdido en los detalles", "desc": "Inmerso en minucias innecesarias que paralizan el proceso.", "color": "Azul"},
    {"nombre": "Resistente al cambio", "desc": "Miedo paralizante a cualquier novedad o riesgo.", "color": "Azul"},
]

COLOR_DOT = {"Verde": "🟢", "Amarillo": "🟡", "Rojo": "🔴", "Azul": "🔵"}
COLORES = ["Amarillo", "Rojo", "Azul", "Verde"]

PERSONAS = [
    {
        "key": "natural",
        "titulo": "Persona Natural (Subyacente)",
        "intro": "Piensa en quién eres verdaderamente en tu estado más relajado, natural y auténtico — sin pensar en lo que exige tu trabajo actual.",
        "catalogo": CUALIDADES_POSITIVAS,
    },
    {
        "key": "cotidiana",
        "titulo": "Persona Cotidiana (Adaptada)",
        "intro": "Piensa en cómo te comportas normalmente en tu trabajo actual, respondiendo a las exigencias del entorno.",
        "catalogo": CUALIDADES_POSITIVAS,
    },
    {
        "key": "sobreextendida",
        "titulo": "Persona Sobreextendida (Bajo Presión)",
        "intro": "Piensa en cómo reaccionas cuando el estrés, el cansancio o la presión te superan — tu versión menos equilibrada.",
        "catalogo": DESCARRILADORES,
    },
]

# ---------------------------------------------------------------------
# 4. Estado de la sesión
# ---------------------------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "landing"  # landing -> select_<persona> -> calibrate_<persona> -> ... -> resultados
if "seleccion" not in st.session_state:
    st.session_state.seleccion = {p["key"]: {"top": [], "bottom": []} for p in PERSONAS}
if "puntajes" not in st.session_state:
    st.session_state.puntajes = {p["key"]: {} for p in PERSONAS}


def persona_por_key(key):
    return next(p for p in PERSONAS if p["key"] == key)


def siguiente_stage(actual):
    orden = ["landing"]
    for p in PERSONAS:
        orden += [f"select_{p['key']}", f"calibrate_{p['key']}"]
    orden += ["resultados"]
    return orden[orden.index(actual) + 1]


# ---------------------------------------------------------------------
# 5. Pantalla: selección de cualidades (tarjetas clicables)
# ---------------------------------------------------------------------
def pantalla_seleccion(persona):
    sel = st.session_state.seleccion[persona["key"]]
    st.header(persona["titulo"])
    st.write(persona["intro"])
    st.write("Selecciona 5 cualidades que MÁS utilices y 5 que MENOS utilices en esta dimensión.")
    st.info(f"Más utilizadas: {len(sel['top'])}/5     ·     Menos utilizadas: {len(sel['bottom'])}/5")

    cols = st.columns(4)
    for i, cualidad in enumerate(persona["catalogo"]):
        nombre = cualidad["nombre"]
        with cols[i % 4]:
            with st.container(border=True):
                st.markdown(f"{COLOR_DOT[cualidad['color']]} **{nombre}**")
                st.caption(cualidad["desc"])
                if nombre in sel["top"]:
                    st.success("⭐ Más presente")
                    if st.button("Quitar", key=f"quitar_{persona['key']}_{nombre}"):
                        sel["top"].remove(nombre)
                        st.rerun()
                elif nombre in sel["bottom"]:
                    st.error("🔻 Menos presente")
                    if st.button("Quitar", key=f"quitar_{persona['key']}_{nombre}"):
                        sel["bottom"].remove(nombre)
                        st.rerun()
                else:
                    lleno = len(sel["top"]) >= 5 and len(sel["bottom"]) >= 5
                    if st.button("Elegir", key=f"elegir_{persona['key']}_{nombre}", disabled=lleno):
                        if len(sel["top"]) < 5:
                            sel["top"].append(nombre)
                        else:
                            sel["bottom"].append(nombre)
                        st.rerun()

    st.divider()
    listo = len(sel["top"]) == 5 and len(sel["bottom"]) == 5
    if st.button("Continuar a Calibración →", disabled=not listo, type="primary"):
        st.session_state.stage = siguiente_stage(st.session_state.stage)
        st.rerun()


# ---------------------------------------------------------------------
# 6. Pantalla: calibración (sliders con porcentaje exacto)
# ---------------------------------------------------------------------
def pantalla_calibracion(persona):
    sel = st.session_state.seleccion[persona["key"]]
    puntajes = st.session_state.puntajes[persona["key"]]
    todos = {c["nombre"]: c for c in persona["catalogo"]}
    restantes = [n for n in todos if n not in sel["top"] and n not in sel["bottom"]]

    st.header(f"{persona['titulo']} — Calibración")
    st.write("Asigna el puntaje porcentual exacto para cada cualidad.")

    st.subheader("⭐ Top 5: predominantes (75% – 99%)")
    cols = st.columns(2)
    for i, nombre in enumerate(sel["top"]):
        default = puntajes.get(nombre, random.randint(75, 99))
        with cols[i % 2]:
            puntajes[nombre] = st.slider(nombre, 75, 99, default, key=f"cal_{persona['key']}_{nombre}")

    st.subheader("🔻 Bottom 5: menos utilizadas (1% – 15%)")
    cols = st.columns(2)
    for i, nombre in enumerate(sel["bottom"]):
        default = puntajes.get(nombre, random.randint(1, 15))
        with cols[i % 2]:
            puntajes[nombre] = st.slider(nombre, 1, 15, default, key=f"cal_{persona['key']}_{nombre}")

    st.subheader("◐ Calibración restante (16% – 74%)")
    st.caption("Ajusta también estas 14 cualidades para completar el perfil.")
    cols = st.columns(2)
    for i, nombre in enumerate(restantes):
        default = puntajes.get(nombre, random.randint(16, 74))
        with cols[i % 2]:
            puntajes[nombre] = st.slider(nombre, 16, 74, default, key=f"cal_{persona['key']}_{nombre}")

    st.divider()
    if st.button("Continuar →", type="primary"):
        st.session_state.stage = siguiente_stage(st.session_state.stage)
        st.rerun()


# ---------------------------------------------------------------------
# 7. Resultados: radar comparando las 3 personas por color
# ---------------------------------------------------------------------
def promedio_por_color(persona_key):
    persona = persona_por_key(persona_key)
    puntajes = st.session_state.puntajes[persona_key]
    resultado = {}
    for color in COLORES:
        nombres_color = [c["nombre"] for c in persona["catalogo"] if c["color"] == color]
        valores = [puntajes.get(n, 50) for n in nombres_color]
        resultado[color] = sum(valores) / len(valores) if valores else 50
    return resultado


def dibujar_radar(datos_por_persona):
    if plt is None or np is None:
        st.warning("Falta la librería matplotlib para dibujar el radar (agrégala a requirements.txt).")
        return

    etiquetas = COLORES
    angulos = np.linspace(0, 2 * np.pi, len(etiquetas), endpoint=False).tolist()
    angulos += angulos[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    colores_linea = {"natural": "#22c55e", "cotidiana": "#6366f1", "sobreextendida": "#ef4444"}
    nombres_legibles = {"natural": "Natural", "cotidiana": "Cotidiana", "sobreextendida": "Sobreextendida"}

    for persona_key, valores_color in datos_por_persona.items():
        valores = [valores_color[e] for e in etiquetas]
        valores += valores[:1]
        ax.plot(angulos, valores, label=nombres_legibles[persona_key], color=colores_linea[persona_key], linewidth=2)
        ax.fill(angulos, valores, color=colores_linea[persona_key], alpha=0.1)

    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(etiquetas)
    ax.set_ylim(0, 100)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    st.pyplot(fig)


def pantalla_resultados():
    st.header("📊 Resultados: comparación de tus 3 personas")

    datos = {p["key"]: promedio_por_color(p["key"]) for p in PERSONAS}
    dibujar_radar(datos)

    for p in PERSONAS:
        st.subheader(p["titulo"])
        sel = st.session_state.seleccion[p["key"]]
        puntajes = st.session_state.puntajes[p["key"]]
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Más presentes**")
            for n in sel["top"]:
                st.write(f"- {n}: {puntajes.get(n)}%")
        with c2:
            st.write("**Menos presentes**")
            for n in sel["bottom"]:
                st.write(f"- {n}: {puntajes.get(n)}%")

    st.divider()
    st.subheader("💬 Interpretación con IA")
    if "interpretacion" not in st.session_state:
        with st.spinner("Generando interpretación..."):
            resumen = "Estos son los promedios por color (0-100) para cada persona:\n\n"
            for p in PERSONAS:
                resumen += f"{p['titulo']}: {datos[p['key']]}\n"
            resumen += (
                "\nComo facilitador experto de Lumina Spark, interpreta brevemente estos resultados: "
                "qué cambia entre la Persona Natural y la Cotidiana (adaptación al entorno laboral), "
                "y qué riesgos aparecen en la Persona Sobreextendida (bajo presión). "
                "Sé breve, profesional y en español."
            )
            try:
                model = genai.GenerativeModel(model_name="gemini-3.6-flash")
                respuesta = model.generate_content(resumen)
                st.session_state.interpretacion = respuesta.text
            except Exception as e:
                st.session_state.interpretacion = f"No se pudo generar la interpretación: {e}"
    st.markdown(st.session_state.interpretacion)

    if st.button("↺ Empezar de nuevo"):
        for key in ["stage", "seleccion", "puntajes", "interpretacion"]:
            st.session_state.pop(key, None)
        st.rerun()


# ---------------------------------------------------------------------
# 8. Pantalla de inicio
# ---------------------------------------------------------------------
def pantalla_landing():
    st.markdown(f"<h1 style='text-align:center'>{APP_ICON} {APP_TITLE}</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center'>Una experiencia de autodescubrimiento. Identifica tus cualidades "
        "en tres dimensiones: <b>Natural</b>, <b>Cotidiana</b> y <b>Sobreextendida</b>.</p>",
        unsafe_allow_html=True,
    )
    st.write("")
    if st.button("Hacer Evaluación Completa →", type="primary", use_container_width=True):
        st.session_state.stage = "select_natural"
        st.rerun()


# ---------------------------------------------------------------------
# 9. Enrutador principal
# ---------------------------------------------------------------------
stage = st.session_state.stage

if stage == "landing":
    pantalla_landing()
elif stage == "resultados":
    pantalla_resultados()
else:
    modo, persona_key = stage.split("_", 1)
    persona = persona_por_key(persona_key)
    if modo == "select":
        pantalla_seleccion(persona)
    else:
        pantalla_calibracion(persona)
