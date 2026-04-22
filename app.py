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
Eres un Facilitador experto de Lumina Spark. Tu misión es realizar una autoevaluación profesional.

METODOLOGÍA DE LAS 24 CUALIDADES (Usa los nombres del PDF):
- Persona Natural (Subyacente): Usa nombres estándar (ej. Imaginativo, Determinado).
- Persona Cotidiana (Adaptada): Enfocado en el entorno laboral actual.
- Persona Sobreextendida (Bajo Presión): Usa los DESCRARRILADORES exactos del PDF:
   - Imaginativo -> Fantasioso
   - Se hace cargo -> Controlador
   - Determinado -> Obsesionado por objetivos
   - Estructurado -> Planeación rígida
   - Confiable -> Indeciso
   - Basado en evidencia -> Perdido en los detalles

DINÁMICA DE PUNTUACIÓN:
Para cada una de las 3 personas, solicita:
1. Las 5 cualidades MÁS usadas (rango 75%-99%).
2. Las 5 cualidades MENOS usadas (rango 1%-15%).
3. Las 14 restantes (rango 16%-74%).

RESULTADOS ESPERADOS:
Al finalizar, muestra tablas comparativas para Natural, Cotidiana y Sobreextendida en:
- 4 Arquetipos de Color: Amarillo, Rojo, Azul y Verde.
- 8 Atributos: Enfoque en Resultados, Disciplina, Inspiración, Gran Visión, Influencia, Orientación a las Personas, Empoderamiento y Observación.
"""

# ESTA LÍNEA ES LA QUE CORRIGE EL ERROR 404
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
        # Historial para mantener el contexto de la evaluación
        history = []
        for m in st.session_state.messages[:-1]:
            role = "model" if m["role"] == "assistant" else "user"
            history.append({"role": role, "parts": [m["content"]]})
        
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
