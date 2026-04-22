import streamlit as st
import google.generativeai as genai

# 1. Configuración de la API Key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("Error: Revisa la configuración de GOOGLE_API_KEY en los Secrets de Streamlit.")
    st.stop()

# SYSTEM PROMPT: Configuración de Lumina Spark basada en tu PDF
system_prompt = """
Eres un Facilitador experto de Lumina Spark. Tu misión es guiar una autoevaluación profesional.

METODOLOGÍA (Basado en el PDF):
- Persona Natural (Subyacente): Nombres estándar (ej. Imaginativo, Determinado).
- Persona Cotidiana (Adaptada): Respuesta al entorno laboral.
- Persona Sobreextendida (Bajo Presión): Usa los DESCRARRILADORES del PDF (Fantasioso, Controlador, Obsesionado por objetivos, Planeación rígida, Indeciso, Perdido en los detalles).

DINÁMICA:
Para cada persona (Natural, Cotidiana, Sobreextendida):
1. Pide 5 cualidades MÁS usadas (75%-99%).
2. Pide 5 cualidades MENOS usadas (1%-15%).
3. Las otras 14 cualidades (16%-74%).

RESULTADOS:
Al final, muestra promedios comparativos para las 3 Personas en:
- 4 Arquetipos de Color: Amarillo, Rojo, Azul y Verde.
- 8 Atributos del modelo Lumina.
"""

# CAMBIO CRÍTICO: Usamos el nombre del modelo más simple posible
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=system_prompt
)

# 2. Interfaz de la aplicación
st.set_page_config(page_title="Autoevaluación Lumina FTF", layout="wide")
st.title("📊 Autoevaluación People Performance Intelligence")

if "messages" not in st.session_state:
    st.session_state.messages = []
    try:
        # Generar primer saludo
        response = model.generate_content("Hola. Preséntate como consultor FTF e inicia la fase de Persona Natural.")
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # Si el error persiste, lo capturamos aquí
        st.error(f"Error de conexión: {e}")

# Mostrar chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de respuestas
if prompt := st.chat_input("Escribe tu respuesta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Construir historial para mantener contexto
        history = []
        for m in st.session_state.messages[:-1]:
            role = "model" if m["role"] == "assistant" else "user"
            history.append({"role": role, "parts": [m["content"]]})
        
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
