import streamlit as st
import time
from google import genai

# Configuración de la página optimizada para dispositivos móviles
st.set_page_config(
    page_title="Asistente Experto del Cuerpo Humano",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados para mejorar la visualización en celulares
st.markdown("""
    <style>
    /* Ajustes generales para móviles */
    .main {
        padding: 0rem 0.5rem;
    }
    
    /* Contenedor del título principal */
    h1 {
        font-size: 1.8rem !important;
        color: #0d6efd;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    
    p {
        font-size: 1rem !important;
    }
    
    /* Estilo amigable para los mensajes del chat en dispositivos móviles */
    .stChatMessage {
        border-radius: 12px;
        padding: 0.5rem;
        margin-bottom: 0.8rem;
    }
    
    /* Adaptar la barra de entrada de texto para celulares */
    .stChatInputContainer {
        padding-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Asistente del Cuerpo Humano")
st.markdown("<p style='text-align: center; color: #555;'>Tu guía inteligente de anatomía, sistemas, funciones y salud.</p>", unsafe_allow_html=True)

st.info("⚠️ **Aviso:** Fines educativos y científicos. No sustituye la consulta médica profesional.")

# Obtener la clave de API desde los secretos de Streamlit
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("⚠️ Falta configurar la `GEMINI_API_KEY` en los secretos de Streamlit Cloud.")
else:
    # Inicializar el cliente de Google GenAI
    client = genai.Client(api_key=api_key)

    # Inicializar el historial del chat en la sesión
    if "ai_systems_chat" not in st.session_state:
        st.session_state.ai_systems_chat = [
            {"role": "assistant", "content": "¡Hola, Samuel! 👋 Soy tu asistente médico inteligente. Pregúntame sobre cualquier sistema del cuerpo, sus funciones, enfermedades o cómo prevenirlas."}
        ]

    # Mostrar el historial de mensajes en la interfaz
    for message in st.session_state.ai_systems_chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto del usuario adaptada a móviles
    if user_prompt := st.chat_input("Escribe tu consulta médica o anatómica..."):
        # Guardar y mostrar el mensaje del usuario
        st.session_state.ai_systems_chat.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Generar respuesta utilizando la inteligencia artificial con reintentos automáticos
        with st.chat_message("assistant"):
            with st.spinner("Consultando bases médicas..."):
                system_instruction = (
                    "Eres un asistente médico, biológico y científico experto en anatomía humana y salud. "
                    "Cuando el usuario pregunte por cualquier sistema del cuerpo (esquelético, nervioso, endocrino, "
                    "respiratorio, circulatorio, digestivo, inmunológico, muscular, excretor, reproductor) u órgano específico, "
                    "debes estructurar tu respuesta de forma clara y profesional incluyendo obligatoriamente:\n"
                    "1. **Estructura y Funciones principales:** Qué es y para qué sirve.\n"
                    "2. **Posibles Enfermedades o Patologías:** Trastornos comunes asociados.\n"
                    "3. **Cómo prevenirlas o combatirlas:** Recomendaciones médicas, estilo de vida y tratamientos generales.\n"
                    "Si el usuario hace un comentario general de cortesía o felicitación, respóndele de forma amable y acuerdále tu propósito médico. "
                    "Responde siempre en español, con un tono amable, educativo y estructurado mediante viñetas."
                )
                
                max_intentos = 3
                exito = False
                ai_reply = ""

                for intento in range(max_intentos):
                    try:
                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=user_prompt,
                            config={
                                'system_instruction': system_instruction,
                                'temperature': 0.7,
                            }
                        )
                        ai_reply = response.text
                        exito = True
                        break
                    except Exception as e:
                        if intento < max_intentos - 1:
                            time.sleep(2)
                        else:
                            ai_reply = f"❌ Ocurrió un error temporal por alta demanda. Por favor, intenta de nuevo en unos segundos. (Detalle: {e})"

                st.markdown(ai_reply)
                
                # Guardar la respuesta en el historial solo si fue exitosa
                if exito:
                    st.session_state.ai_systems_chat.append({"role": "assistant", "content": ai_reply})
