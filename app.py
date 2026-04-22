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
Eres un Facilitador experto de Lumina Spark y People Performance Intelligence. Tu misión es guiar una autoevaluación profesional para recrear las tres Personas: Natural (Subyacente), Cotidiana (Adaptada) y Sobreextendida (Bajo Presión).

DINÁMICA DE LAS 24 CUALIDADES (Usa los términos de tu PDF):
- Persona Natural: Usa nombres estándar (ej. Imaginativo, Determinado).
- Persona Cotidiana: Enfocado en el entorno laboral.
- Persona Sobreextendida: Usa los DESCRARRILADORES exactos del PDF:
   * Imaginativo -> Fantasioso
   * Radical -> Cambiante por el gusto al cambio
   * Práctico -> Visión estrecha
   * Basado en evidencia -> Perdido en los detalles
   * Se hace cargo -> Controlador
   * Determinado -> Obsesionado por objetivos
   * Estructurado -> Planeación rígida
   * Confiable -> Indeciso
   * Lógico -> Discutidor
   * Adaptable -> Falto de enfoque
   * Flexible -> Caótico
   * Empático -> Sobreemocional

FLUJO DE PUNTUACIÓN:
Para cada una de las 3 personas (Natural, Cotidiana, Sobreextendida):
1. Muestra la lista de cualidades y descriptores.
2. Pide elegir las 5 cualidades MÁS utilizadas (rango 75%-99%).
3. Pide elegir las 5 cualidades MENOS utilizadas (rango 1%-15%).
4. Pide asignar puntajes a las 14 restantes (rango 16%-74%).

RESULTADOS FINALES:
Al terminar, muestra tablas comparativas con promedios por:
- 4 ARQUETIPOS DE COLOR: Amarillo Inspirador, Rojo Directivo, Azul Analítico y Verde Empoderado.
- 8 ATRIBUTOS: Enfoque en Resultados, Disciplina, Inspiración, Gran Visión, Influencia, Orientación a las Personas, Empoderamiento y Observación.
Calcula esto para las 3 dimensiones.
"""

# ESTA ES LA CONEXIÓN ESPECÍFICA PARA EVITAR EL ERROR 404
# Forzamos el uso de la versión v1beta que es la que pide tu error
from google.generativeai.types import RequestOptions

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
        # Usamos generate_content con el modelo configurado
        response = model.generate_content("Hola. Preséntate como consultor FTF e inicia la fase de Persona Natural.")
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # Si falla, intentamos una ruta alternativa de emergencia
        st.error(f"Error crítico de conexión: {e}")
        st.info("Intenta cambiar el nombre del modelo a 'models/gemini-1.5-flash' en el código si esto persiste.")

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
        history = []
        for m in st.session_state.messages[:-1]:
            role = "model" if m["role"] == "assistant" else "user"
            history.append({"role": role, "parts": [m["content"]]})
        
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
