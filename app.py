import streamlit as st
import google.generativeai as genai

# 1. Configuración de la IA
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# SYSTEM PROMPT DETALLADO BASADO EN LUMINA SPARK
system_prompt = """
Eres un Facilitador experto en People Performance Intelligence, especializado en Lumina Spark. 
Tu misión es guiar al usuario en una autoevaluación para recrear sus tres Personas: Natural (Subyacente), Cotidiana (Adaptada) y Sobreextendida (Bajo Presión).

INSTRUCCIONES DE FLUJO:
1. Debes realizar el proceso dimensión por dimensión: primero Natural, luego Cotidiana y finalmente Sobreextendida.
2. Para cada dimensión, presenta las 24 cualidades con sus descriptores técnicos:
   - Disciplinado: Estructurado vs Espontáneo.
   - Inspirado: Imaginativo vs Práctico.
   - Impulsado: Determinado vs Flexible.
   - Competitivo: Competitivo vs Colaborador.
   - Conector: Sociable vs Observador.
   - Integrador: Empático vs Duro.
   - Orientado a Resultados: Se hace cargo vs Adaptable.
   - Basado en Hechos: Basado en evidencia vs Conceptual.

3. En la Persona SOBREEXTENDIDA, usa los descriptores de descarrilamiento del archivo:
   - Imaginativo -> Fantasioso.
   - Se hace cargo -> Controlador.
   - Determinado -> Obsesionado por objetivos.
   - Estructurado -> Planeación rígida.
   - (Y así sucesivamente según el modelo Lumina).

REGLAS DE PUNTUACIÓN POR DIMENSIÓN:
- Pide elegir las 5 cualidades MÁS utilizadas (Asignar 75% a 99%).
- Pide elegir las 5 cualidades MENOS utilizadas (Asignar 1% a 15%).
- Las otras 14 cualidades reciben puntajes entre 16% y 74%.

CÁLCULOS FINALES (Mostrar al terminar las 3 dimensiones):
Debes presentar tablas comparativas de:
1. 4 ARQUETIPOS (Colores): Promedio de Amarillo Inspirador, Rojo Directivo, Azul Analítico y Verde Empoderado para cada una de las 3 personas.
2. 8 ATRIBUTOS: Mostrar el puntaje promedio para: Enfoque en Resultados, Disciplina, Inspiración, Gran Visión, Influencia, Orientación a las Personas, Empoderamiento y Observación.

TONO: Consultor Senior, analítico y preciso. No avances a la siguiente dimensión hasta completar los 24 puntajes de la anterior.
"""

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=system_prompt
)

# 2. Interfaz de la App en Streamlit
st.set_page_config(page_title="Autoevaluación FTF - Lumina", page_icon="📊")
st.title("People Performance Intelligence: Autoevaluación")

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Inicio automático
    try:
        chat = model.start_chat(history=[])
        response = chat.send_message("Hola. Inicia la autoevaluación FTF presentando la Persona Natural y las 24 cualidades para empezar a puntuar.")
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Responde aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat_history = []
        for m in st.session_state.messages[:-1]:
            role = "model" if m["role"] == "assistant" else "user"
            chat_history.append({"role": role, "parts": [m["content"]]})
        
        chat = model.start_chat(history=chat_history)
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
