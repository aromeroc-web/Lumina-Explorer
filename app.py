import streamlit as st
import google.generativeai as genai

# 1. Configuración de la IA usando la llave de la "caja fuerte"
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Aquí puedes pegar tus instrucciones de Studio
system_prompt = "Eres un experto senior en People Performance Intelligence."

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=system_prompt
)

# 2. Interfaz de la App
st.set_page_config(page_title="Lumina Explorer", page_icon="📈")
st.title("Asistente de People Performance Intelligence")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
