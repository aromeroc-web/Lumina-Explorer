# Busca la parte de la configuración y déjala así:
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')
