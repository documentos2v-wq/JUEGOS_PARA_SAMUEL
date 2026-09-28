import streamlit as st
from google import genai

# Configuración de la página
st.set_page_config(
    page_title="Asistente Experto del Cuerpo Humano con IA",
    page_icon="🧬",
    layout="centered"
)

st.title("🧬 Asistente Inteligente del Cuerpo Humano (Powered by AI)")
st.write("Pregúntame lo que sea: sobre órganos, sistemas, funciones, enfermedades o cómo cuidarte. ¡Respondo a cualquier duda con inteligencia artificial!")

st.info("⚠️ **Aviso informativo:** Este chat tiene fines educativos y científicos. No sustituye la consulta médica profesional.")

# Obtener la clave de API desde los secretos de Streamlit
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("⚠️ Falta configurar la `GEMINI_API_KEY` en los secretos de Streamlit Cloud para que la IA responda.")
else:
    # Inicializar el cliente de Google GenAI
    client = genai.Client(api_key=api_key)

    # Inicializar el historial del chat en la sesión
    if "ai_chat_messages" not in st.session_state:
        st.session_state.ai_chat_messages = [
            {"role": "assistant", "content": "¡Hola! 👋 Soy tu asistente médico y biológico inteligente. Pregúntame sobre el páncreas, el hígado, por qué se enferman los órganos o cualquier tema del cuerpo humano."}
        ]

    # Mostrar el historial de mensajes en la interfaz
    for message in st.session_state.ai_chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto del usuario
    if user_prompt := st.chat_input("Escribe tu pregunta sobre el cuerpo humano..."):
        # Guardar y mostrar el mensaje del usuario
        st.session_state.ai_chat_messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Generar respuesta utilizando la inteligencia artificial de Gemini
        with st.chat_message("assistant"):
            with st.spinner("Consultando información médica y biológica..."):
                try:
                    # Instrucción de sistema para guiar el comportamiento de la IA
                    system_instruction = (
                        "Eres un asistente médico, biológico y educativo experto en el cuerpo humano. "
                        "Responde de manera amable, clara, estructurada y en español. "
                        "Explica anatomía, funciones, órganos (como el páncreas, hígado, etc.) y causas de enfermedades de forma comprensible."
                    )
                    
                    # Llamada utilizando el modelo estándar activo y compatible
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=user_prompt,
                        config={
                            'system_instruction': system_instruction,
                            'temperature': 0.7,
                        }
                    )
                    
                    ai_reply = response.text
                    st.markdown(ai_reply)
                    
                    # Guardar la respuesta en el historial
                    st.session_state.ai_chat_messages.append({"role": "assistant", "content": ai_reply})
                    
                except Exception as e:
                    error_msg = f"❌ Ocurrió un error al comunicarse con la inteligencia artificial: {e}"
                    st.error(error_msg)
