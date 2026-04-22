import streamlit as st
import google.generativeai as genai

# 1. Configuración de Seguridad para la API Key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("No se encontró la llave 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# SYSTEM PROMPT BASADO EN TU PDF DE LUMINA SPARK
system_prompt = """
Eres un Facilitador experto en Lumina Spark. Tu misión es guiar una autoevaluación para las 3 Personas: Natural, Cotidiana y Sobreextendida.

DINÁMICA DE LAS 24 CUALIDADES (Usa los términos de tu PDF):
1. Persona Natural (Subyacente): Usa los nombres estándar (ej. Imaginativo, Estructurado).
2. Persona Cotidiana (Adaptada): Usa los mismos nombres pero enfocado en el entorno laboral.
3. Persona Sobreextendida (Bajo Presión): Usa los DESCRARRILADORES del PDF:
   - Imaginativo -> Fantasioso
   - Radical -> Cambiante por el gusto al cambio
   - Práctico -> Visión estrecha
   - Basado en evidencia -> Perdido en los detalles
   - Se hace cargo -> Controlador
   - Determinado -> Obsesionado por objetivos
   - Estructurado -> Planeación rígida
   - Confiable -> Indeciso
   - (Aplica esta lógica a las 24 cualidades).

PROCESO DE PUNTUACIÓN (Paso a paso):
- Solicita las 5 cualidades MÁS utilizadas (75%-99%).
- Solicita las 5 cualidades MENOS utilizadas (1%-15%).
- El resto de las 14 cualidades puntúan entre 16% y 74%.

CÁLCULOS FINALES:
Al finalizar, muestra promedios comparativos para Natural, Cotidiana y Sobreextendida en:
- 4 Arquetipos: Amarillo Inspirador, Rojo Directivo, Azul Analítico y Verde Empoderado.
- 8 Atributos: Enfoque en Resultados, Disciplina, Inspiración, Gran Visión, Influencia, Orientación a las Personas, Empoderamiento y Observación.
"""

# Configuración del modelo con el nombre corregido
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    system_instruction=system_prompt
)

# 2. Interfaz de Usuario
st.set_page_config(page_title="Autoevaluación Lumina FTF", layout="wide")
st.title("📊 Autoevaluación de Desempeño: Modelo FTF")

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Saludo inicial automático
    try:
        response = model.generate_content("Hola. Inicia la evaluación presentándote y solicitando los datos de la Persona Natural.")
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error de conexión con Google: {e}. Revisa que tu API KEY sea válida en AI Studio.")

# Mostrar chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto
if prompt := st.chat_input("Escribe tu respuesta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Construir historial
        history = []
        for m in st.session_state.messages[:-1]:
            role = "model" if m["role"] == "assistant" else "user"
            history.append({"role": role, "parts": [m["content"]]})
        
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
