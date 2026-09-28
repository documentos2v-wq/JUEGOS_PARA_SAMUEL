import streamlit as st
from google import genai

# Configuración de la página
st.set_page_config(
    page_title="Asistente Experto del Cuerpo Humano con IA",
    page_icon="🧬",
    layout="centered"
)

st.title("🧬 Asistente Inteligente del Cuerpo Humano (Powered by AI)")
st.write("Pregúntame sobre cualquier sistema (esquelético, nervioso, endocrino, respiratorio, circulatorio, digestivo, inmunológico, muscular, excretor, reproductor), sus funciones, posibles enfermedades y cómo prevenirlas o combatirlas.")

st.info("⚠️ **Aviso informativo:** Este chat tiene fines educativos y científicos. No sustituye la consulta médica profesional.")

# Obtener la clave de API desde los secretos de Streamlit
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("⚠️ Falta configurar la `GEMINI_API_KEY` en los secretos de Streamlit Cloud para que la IA responda.")
else:
    # Inicializar el cliente de Google GenAI
    client = genai.Client(api_key=api_key)

    # Inicializar el historial del chat en la sesión
    if "ai_systems_chat" not in st.session_state:
        st.session_state.ai_systems_chat = [
            {"role": "assistant", "content": "¡Hola, Samuel! 👋 Soy tu asistente médico y biológico inteligente. Ya tengo integradas las bases de todos los sistemas del cuerpo humano. Pregúntame sobre las funciones de cualquier sistema, sus enfermedades más comunes y cómo prevenirlas o combatirlas."}
        ]

    # Mostrar el historial de mensajes en la interfaz
    for message in st.session_state.ai_systems_chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto del usuario
    if user_prompt := st.chat_input("Escribe tu pregunta sobre anatomía, funciones o enfermedades..."):
        # Guardar y mostrar el mensaje del usuario
        st.session_state.ai_systems_chat.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Generar respuesta utilizando la inteligencia artificial de Gemini
        with st.chat_message("assistant"):
            with st.spinner("Consultando bases de conocimiento médico y anatómico..."):
                try:
                    # Instrucción de sistema experta para cubrir funciones, patologías y tratamientos
                    system_instruction = (
                        "Eres un asistente médico, biológico y científico experto en anatomía humana y salud. "
                        "Cuando el usuario pregunte por cualquier sistema del cuerpo (esquelético, nervioso, endocrino, "
                        "respiratorio, circulatorio, digestivo, inmunológico, muscular, excretor, reproductor) u órgano específico, "
                        "debes estructurar tu respuesta de forma clara y profesional incluyendo obligatoriamente:\n"
                        "1. **Estructura y Funciones principales:** Qué es y para qué sirve.\n"
                        "2. **Posibles Enfermedades o Patologías:** Trastornos comunes asociados.\n"
                        "3. **Cómo prevenirlas o combatirlas:** Recomendaciones médicas, estilo de vida y tratamientos generales.\n"
                        "Responde siempre en español, con un tono amable, educativo y estructurado mediante viñetas."
                    )
                    
                    # Llamada al modelo oficial de Gemini
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=user_prompt,
                        config={
                            'system_instruction': system_instruction,
                            'temperature': 0.7,
                        }
                    )
                    
                    ai_reply = response.text
                    st.markdown(ai_reply)
                    
                    # Guardar la respuesta en el historial
                    st.session_state.ai_systems_chat.append({"role": "assistant", "content": ai_reply})
                    
                except Exception as e:
                    error_msg = f"❌ Ocurrió un error al comunicarse con la inteligencia artificial: {e}"
                    st.error(error_msg)
