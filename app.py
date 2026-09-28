import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Enciclopedia y Chat del Cuerpo Humano",
    page_icon="🧬",
    layout="centered"
)

# Título y descripción principal
st.title("🧬 Asistente Experto del Cuerpo Humano")
st.write("Pregúntame sobre cualquier órgano, sistema (nervioso, circulatorio, digestivo, etc.), huesos, músculos o cómo funciona nuestro organismo.")

# Aviso médico de responsabilidad
st.info("⚠️ **Aviso informativo:** Este chat tiene fines educativos y de divulgación científica sobre anatomía y biología humana. No sustituye la consulta médica profesional.")

# Inicializar el historial del chat
if "body_chat_messages" not in st.session_state:
    st.session_state.body_chat_messages = [
        {"role": "assistant", "content": "¡Hola! Soy tu guía especializado en el cuerpo humano. ¿Qué te gustaría saber hoy? Puedes preguntarme sobre el corazón, el cerebro, los músculos, cómo digerimos los alimentos y mucho más."}
    ]

# Mostrar los mensajes anteriores en la interfaz de chat
for message in st.session_state.body_chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Cuadro de entrada de texto para que el usuario escriba su pregunta
if user_question := st.chat_input("Escribe tu pregunta sobre el cuerpo humano..."):
    # Guardar y mostrar el mensaje del usuario
    st.session_state.body_chat_messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # Procesar la respuesta automática basada en temas del cuerpo humano
    q_lower = user_question.lower()
    
    if any(w in q_lower for w in ["corazón", "latidos", "sangre", "circulación", "arterias", "venas"]):
        answer = "❤️ **El Sistema Circulatorio y el Corazón:**\nEl corazón es un músculo increíble que actúa como una bomba doble. Late unas 100,000 veces al día, impulsando sangre oxigenada por las arterias hacia todo el cuerpo y recibiendo sangre de regreso a través de las venas para purificarla en los pulmones."
    elif any(w in q_lower for w in ["cerebro", "mente", "neuronas", "pensar", "memoria", "encéfalo"]):
        answer = "🧠 **El Cerebro y el Sistema Nervioso:**\nEl cerebro es el centro de control del cuerpo. Contiene aproximadamente 86 mil millones de neuronas que se comunican mediante impulsos eléctricos y químicos. Controla tus pensamientos, memoria, emociones, movimientos y la respiración inconsciente."
    elif any(w in q_lower for w in ["estómago", "digestión", "intestino", "comer", "comida", "hígado"]):
        answer = "🍏 **El Sistema Digestivo:**\nLa digestión comienza en la boca y recorre un tubo de unos 9 metros de longitud. El estómago utiliza ácidos potentes para descomponer los alimentos, mientras que el intestino delgado absorbe los nutrientes y el intestino grueso se encarga del agua."
    elif any(w in q_lower for w in ["pulmones", "respirar", "aire", "oxígeno", "respiratorio"]):
        answer = "🫁 **Los Pulmones y la Respiración:**\nInhalamos aire para capturar oxígeno, el cual pasa a los glóbulos rojos en los alvéolos pulmonares. Al mismo tiempo, expulsamos dióxido de carbone, que es un desecho metabólico de nuestras células."
    elif any(w in q_lower for w in ["huesos", "esqueleto", "fémur", "columna", "articulaciones"]):
        answer = "🦴 **El Sistema Óseo:**\nUn adulto humano tiene 206 huesos. El hueso más largo y fuerte es el fémur (en el muslo), mientras que los más pequeños están dentro del oído (martillo, yunque y estribo). Los huesos no solo dan soporte, sino que producen células sanguíneas en su médula."
    elif any(w in q_lower for w in ["músculos", "muscular", "fuerza", "movimiento"]):
        answer = "💪 **El Sistema Muscular:**\nTenemos más de 600 músculos en el cuerpo. Se dividen en esqueléticos (los que movemos voluntariamente), cardíacos (el corazón) y lisos (los que mueven órganos internos como los intestinos)."
    elif any(w in q_lower for w in ["riñón", "orina", "filtrar", "agua", "toxinas"]):
        answer = "💧 **Los Riñones y el Sistema Excretor:**\nLos riñones actúan como los filtros principales del cuerpo. Filtran la sangre unas 40 veces al día, eliminando toxinas y exceso de agua en forma de orina para mantener el equilibrio químico interno."
    else:
        answer = f"🔍 Es una excelente pregunta sobre el cuerpo humano. El organismo es una red compleja de sistemas interconectados (como el endocrino, inmunológico y tegumentario) que trabajan en armonía (homeostasis). ¿Te gustaría profundizar en algún órgano o función específica relacionada con tu consulta sobre *'{user_question}'*?"

    # Mostrar y guardar la respuesta generada
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.body_chat_messages.append({"role": "assistant", "content": answer})
