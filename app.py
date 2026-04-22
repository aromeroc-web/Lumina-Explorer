import streamlit as st
import google.generativeai as genai

# 1. Configuración de la IA
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

system_prompt = """
Eres un Facilitador experto en Lumina Spark. Tu misión es guiar una autoevaluación para las 3 Personas: Natural, Cotidiana y Sobreextendida.

METODOLOGÍA DE CUALIDADES (Usa estos nombres exactos):
- Inspirado: Imaginativo, Radical, Conceptual, Teórico.
- Disciplinado: Estructurado, Confiable, Basado en evidencia, Práctico.
- Impulsado: Determinado, Se hace cargo, Competitivo, Enfocado en resultados.
- Conector: Sociable, Expresivo, Afirmativo, Animado.
- (Usa las 24 cualidades del PDF adjunto).

PARA LA PERSONA SOBREEXTENDIDA (Usa los descarriladores del PDF):
- Imaginativo -> Fantasioso.
- Se hace cargo -> Controlador.
- Determinado -> Obsesionado por objetivos.
- Estructurado -> Planeación rígida.
- Confiable -> Indeciso.
- Basado en evidencia -> Perdido en los detalles.

PROCESO:
1. Pide 5 cualidades MÁS usadas (75%-99%).
2. Pide 5 cualidades MENOS usadas (1%-15%).
3. Resto de 14 cualidades (16%-74%).
Repite para Natural, Cotidiana y Sobreextendida.

RESULTADOS FINALES:
Muestra promedios por:
- 4 Arquetipos: Amarillo Inspirador, Rojo Directivo, Azul Analítico, Verde Empoderado.
- 8 Atributos: Enfoque en Resultados, Disciplina, Inspiración, Gran Visión, Influencia, Orientación a las Personas, Empoderamiento y Observación.
Calcula esto para las 3 dimensiones (Natural, Cotidiana, Sobreextendida).
"""

model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=system_prompt)

# 2. Interfaz Streamlit
st.set_page_config(page_title="Autoevaluación FTF", layout="wide")
st.title("📊 Autoevaluación People Performance Intelligence")

if "messages" not in st.session_state:
    st.session_state.messages = []
    try:
        response = model.generate_content("Inicia la evaluación solicitando los datos para la Persona Natural.")
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except:
        st.error("Error de API Key. Revisa tus Secrets en Streamlit.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu respuesta aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        history = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
