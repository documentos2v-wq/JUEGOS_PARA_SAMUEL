import streamlit as st
import wikipedia

# Configurar Wikipedia en idioma español
wikipedia.set_lang("es")

# Configuración de la página
st.set_page_config(
    page_title="Asistente Inteligente del Cuerpo Humano",
    page_icon="🧬",
    layout="centered"
)

# Título y descripción principal
st.title("🧬 Asistente Inteligente del Cuerpo Humano + Wikipedia")
st.write("Pregúntame sobre cualquier parte, órgano, hueso o sistema del cuerpo. Si no lo sé de memoria, lo buscaré automáticamente en Wikipedia para darte la mejor información.")

# Aviso médico de responsabilidad
st.info("⚠️ **Aviso informativo:** Este chat tiene fines educativos y científicos. No sustituye la consulta médica profesional.")

# Inicializar el historial del chat
if "body_chat_messages" not in st.session_state:
    st.session_state.body_chat_messages = [
        {"role": "assistant", "content": "¡Hola! 👋 Ahora estoy conectado para buscar información verídica en tiempo real. Pregúntame sobre los pies, las manos, los órganos o cualquier duda anatómica que tengas."}
    ]

# Mostrar los mensajes anteriores en la interfaz de chat
for message in st.session_state.body_chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Cuadro de entrada de texto
if user_question := st.chat_input("Escribe tu pregunta sobre el cuerpo humano..."):
    # Guardar y mostrar el mensaje del usuario
    st.session_state.body_chat_messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    q_lower = user_question.lower()
    answer = ""

    # 1. Saludos y cortesía
    if any(w in q_lower for w in ["hola", "saludos", "buenas", "qué tal", "hey"]):
        answer = "¡Hola! 👋 Qué gusto saludarte. ¿Qué parte o funcionamiento del cuerpo humano te gustaría investigar hoy?"
    elif any(w in q_lower for w in ["gracias", "excelente", "genial", "buen trabajo"]):
        answer = "¡De nada! Me alegra mucho poder ayudarte a descubrir más sobre anatomía. ¿Tienes alguna otra duda? ✨"
    
    # 2. Respuestas rápidas para temas principales
    elif any(w in q_lower for w in ["corazón", "latidos", "sangre", "circulación"]):
        answer = "❤️ **El Corazón y el Sistema Circulatorio:**\nEs un músculo en forma de bomba que late unas 100,000 veces al día, impulsando sangre oxigenada por todo el cuerpo a través de arterias y venas."
    elif any(w in q_lower for w in ["cerebro", "mente", "neuronas", "pensar"]):
        answer = "🧠 **El Cerebro:**\nEs el centro de control del cuerpo humano. Contiene miles de millones de neuronas que coordinan los pensamientos, las emociones, los movimientos y los sentidos."
    
    # 3. Búsqueda automática en Wikipedia para cualquier otra consulta (como "pies", "rodilla", "hígado", etc.)
    else:
        try:
            # Buscar en Wikipedia en español un resumen de hasta 3 oraciones
            wiki_summary = wikipedia.summary(user_question, sentences=3, auto_suggest=True)
            answer = f"📚 **Información verificada (vía Wikipedia):**\n\n{wiki_summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            answer = f"🔍 Tu búsqueda es muy amplia y encontré varios temas relacionados ({e.options[:3]}). ¿Podrías ser un poco más específico en tu pregunta?"
        except wikipedia.exceptions.PageError:
            answer = f"🤔 No encontré registros exactos sobre *'{user_question}'*. Intenta preguntar por un órgano, hueso o parte del cuerpo específica (por ejemplo: 'el pie humano', 'el fémur', 'el hígado')."
        except Exception:
            answer = f"🔍 El cuerpo humano es fascinante y conecta muchos sistemas. Aunque no hallé detalles exactos sobre *'{user_question}'*, te sugiero consultar sobre anatomía general, músculos u órganos principales."

    # Mostrar y guardar la respuesta generada
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.body_chat_messages.append({"role": "assistant", "content": answer})
