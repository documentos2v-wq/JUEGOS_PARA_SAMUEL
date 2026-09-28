import streamlit as st
import wikipedia
import re

# Configurar Wikipedia en idioma español
wikipedia.set_lang("es")

# Configuración de la página
st.set_page_config(
    page_title="Asistente Inteligente del Cuerpo Humano",
    page_icon="🧬",
    layout="centered"
)

st.title("🧬 Asistente Inteligente del Cuerpo Humano + Wikipedia")
st.write("Pregúntame sobre cualquier parte, órgano, hueso o sistema del cuerpo. Analizaré tu pregunta y buscaré la información verídica.")

st.info("⚠️ **Aviso informativo:** Este chat tiene fines educativos y científicos. No sustituye la consulta médica profesional.")

# Inicializar el historial del chat
if "body_chat_messages" not in st.session_state:
    st.session_state.body_chat_messages = [
        {"role": "assistant", "content": "¡Hola! 👋 Escribe cualquier pregunta o tema sobre el cuerpo humano (por ejemplo: 'las manos', 'el hígado', 'los ojos') y te buscaré la información."}
    ]

# Mostrar historial de mensajes
for message in st.session_state.body_chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Cuadro de entrada de texto
if user_question := st.chat_input("Escribe tu pregunta sobre el cuerpo humano..."):
    st.session_state.body_chat_messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    q_lower = user_question.lower()
    answer = ""

    # 1. Saludos y cortesía
    if any(w in q_lower for w in ["hola", "saludos", "buenas", "qué tal", "hey"]):
        answer = "¡Hola! 👋 Qué gusto saludarte. ¿Qué parte del cuerpo humano te gustaría investigar hoy?"
    elif any(w in q_lower for w in ["gracias", "excelente", "genial", "buen trabajo"]):
        answer = "¡De nada! Me alegra mucho poder ayudarte a descubrir más sobre anatomía. ¿Tienes alguna otra duda? ✨"
    
    # 2. Respuestas rápidas predeterminadas
    elif any(w in q_lower for w in ["corazón", "latidos", "sangre", "circulación"]):
        answer = "❤️ **El Corazón y el Sistema Circulatorio:**\nEs un músculo en forma de bomba que late unas 100,000 veces al día, impulsando sangre oxigenada por todo el cuerpo a través de arterias y venas."
    elif any(w in q_lower for w in ["cerebro", "mente", "neuronas", "pensar"]):
        answer = "🧠 **El Cerebro:**\nEs el centro de control del cuerpo humano. Contiene miles de millones de neuronas que coordinan los pensamientos, las emociones, los movimientos y los sentidos."
    
    # 3. Extracción de palabras clave y búsqueda inteligente en Wikipedia
    else:
        try:
            # Limpiar palabras comunes de la pregunta para buscar el término clave exacto en Wikipedia
            stopwords = ["que", "sabes", "sobre", "el", "la", "los", "las", "de", "del", "en", "y", "a", "un", "una", "por", "para", "es", "son", "cuantos", "tiene", "está", "compuesto", "como", "huesos", "piel", "podrias", "decirme"]
            words = re.findall(r'\b\w+\b', q_lower)
            clean_words = [w for w in words if w not in stopwords and len(w) > 2]
            
            search_query = " ".join(clean_words) if clean_words else user_question
            
            # Intentar buscar en Wikipedia
            wiki_summary = wikipedia.summary(search_query, sentences=3, auto_suggest=True)
            answer = f"📚 **Información verificada sobre '{search_query}' (vía Wikipedia):**\n\n{wiki_summary}"
            
        except wikipedia.exceptions.DisambiguationError as e:
            # Si hay varias opciones, intentamos buscar la primera opción sugerida
            try:
                wiki_summary = wikipedia.summary(e.options[0], sentences=3, auto_suggest=False)
                answer = f"📚 **Información verificada (vía Wikipedia):**\n\n{wiki_summary}"
            except Exception:
                answer = f"🔍 Tu búsqueda arrojó varios temas. ¿Podrías ser más específico con el órgano o parte del cuerpo?"
        except wikipedia.exceptions.PageError:
            answer = f"🤔 No encontré registros exactos sobre *'{user_question}'*. Intenta buscar por el nombre directo del órgano o parte (ejemplo: 'mano humana', 'hígado', 'fémur')."
        except Exception:
            answer = f"🔍 El cuerpo humano es fascinante. Intenta consultar por un órgano o sistema específico para darte una respuesta detallada."

    # Mostrar y guardar la respuesta
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.body_chat_messages.append({"role": "assistant", "content": answer})
