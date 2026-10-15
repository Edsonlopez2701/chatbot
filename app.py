import streamlit as st
from google import genai
from google.genai.errors import ServerError

# Configuración de la interfaz
st.set_page_config(page_title="Chatbot con Google Gemini", page_icon="✨")
st.title("✨ Chatbot con Google Gemini")

# Reemplaza con tu API Key de Google AI Studio
GEMINI_API_KEY = ""

# 1. Guardar el cliente en el session_state
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=GEMINI_API_KEY)

# 2. Inicializar el chat con el modelo recomendado
if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(model="gemini-2.5-flash")

# Mostrar el historial de mensajes
for message in st.session_state.chat.get_history():
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Capturar la entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje..."):
    # Mostrar el mensaje del usuario en pantalla
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar y mostrar la respuesta del modelo controlando posibles sobrecargas
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
        except ServerError:
            st.warning("⚠️ Los servidores de Gemini están saturados en este momento. Por favor, intenta de nuevo en unos segundos.")
        except Exception as e:
            st.error(f"Ocurrió un error inesperado: {e}")
            
if st.button("Reiniciar chat"):
    st.session_state.chat = st.session_state.client.chats.create(model="gemini-2.5-flash")
    st.experimental_rerun()

