import streamlit as st
import unicodedata

# Configuración de la página optimizada para celulares
st.set_page_config(
    page_title="Asistente del Cuerpo Humano",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS limpios y modernos para móviles
st.markdown("""
    <style>
    .main { padding: 0rem 0.5rem; }
    h1 { font-size: 1.7rem !important; color: #0d6efd; text-align: center; margin-bottom: 0.1rem; }
    p { font-size: 0.95rem !important; }
    .stChatMessage { border-radius: 10px; padding: 0.4rem; margin-bottom: 0.6rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Asistente del Cuerpo Humano")
st.markdown("<p style='text-align: center; color: #555;'>Respuestas directas, rápidas y específicas.</p>", unsafe_allow_html=True)

st.info("⚠️ **Aviso:** Fines educativos y científicos. No sustituye la consulta médica profesional.")

# Inicializar historial de chat local
if "local_chat_messages" not in st.session_state:
    st.session_state.local_chat_messages = [
        {"role": "assistant", "content": "¡Hola, Samuel! 👋 Pregúntame sobre cualquier sistema u órgano y te daré una respuesta corta y directa."}
    ]

# Mostrar historial
for message in st.session_state.local_chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def normalizar_texto(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn').lower()

# Entrada de texto del usuario
if user_question := st.chat_input("Escribe tu pregunta directa..."):
    st.session_state.local_chat_messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    q_norm = normalizar_texto(user_question)
    answer = ""

    # Saludos y cortesía cortos
    if any(w in q_norm for w in ["hola", "saludos", "buenas", "que tal", "hey"]):
        answer = "¡Hola, Samuel! 👋 ¿Qué sistema u órgano deseas consultar?"
    elif any(w in q_norm for w in ["gracias", "excelente", "genial"]):
        answer = "¡De nada! ¿Tienes alguna otra consulta específica?"

    # Sistemas y órganos (Respuestas estrictas y directas)
    elif "sistema oseo" in q_norm or "esqueleto" in q_norm:
        answer = "🦴 **Sistema Esquelético:**\n* **Función:** Compuesto por 206 huesos que dan soporte, protección a órganos y almacenamiento de minerales.\n* **Enfermedades comunes:** Osteoporosis, fracturas y artritis.\n* **Prevención/Combate:** Consumo de calcio y vitamina D, ejercicio de fuerza y revisiones densitométricas."
    elif "sistema nervioso" in q_norm:
        answer = "🧠 **Sistema Nervioso:**\n* **Función:** Controla y coordina las funciones corporales mediante el SNC (cerebro, médula) y nervios periféricos.\n* **Enfermedades comunes:** Alzheimer, epilepsia y neuropatías.\n* **Prevención/Combate:** Descanso adecuado, estimulación mental y evitar sustancias neurotóxicas."
    elif "sistema endocrino" in q_norm or "hormonas" in q_norm:
        answer = "🧪 **Sistema Endocrino:**\n* **Función:** Regula procesos metabólicos y corporales mediante la secreción de hormonas (tiroides, páncreas, etc.).\n* **Enfermedades comunes:** Diabetes mellitus, hipotiroidismo.\n* **Prevención/Combate:** Dieta equilibrada, control de glucosa y manejo del estrés."
    elif "sistema respiratorio" in q_norm or "pulmones" in q_norm:
        answer = "🫁 **Sistema Respiratorio:**\n* **Función:** Realiza el intercambio gaseoso (oxígeno y dióxido de carbono) a través de las vías aéreas y alvéolos.\n* **Enfermedades comunes:** Asma, EPOC, neumonía.\n* **Prevención/Combate:** Evitar el tabaquismo, ejercicio aeróbico y alejarse de contaminantes."
    elif "sistema circulatorio" in q_norm or "corazon" in q_norm:
        answer = "❤️ **Sistema Circulatorio:**\n* **Función:** Bombea y transporta sangre, oxígeno y nutrientes por todo el cuerpo a través del corazón, arterias y venas.\n* **Enfermedades comunes:** Hipertensión arterial, infartos, arritmias.\n* **Prevención/Combate:** Dieta baja en grasas saturadas, ejercicio cardiovascular y control de presión."
    elif "sistema digestivo" in q_norm or "estomago" in q_norm:
        answer = "🍏 **Sistema Digestivo:**\n* **Función:** Descompone los alimentos y absorbe nutrientes mediante el tracto gastrointestinal y glándulas anexas.\n* **Enfermedades comunes:** Gastritis, úlceras, colitis.\n* **Prevención/Combate:** Hidratación constante, fibra en la dieta y evitar irritantes gástricos."
    elif "sistema inmunologico" in q_norm or "defensas" in q_norm:
        answer = "🛡️ **Sistema Inmunológico:**\n* **Función:** Defiende al organismo contra infecciones y patógenos mediante órganos linfoides y glóbulos blancos.\n* **Enfermedades comunes:** Alergias, enfermedades autoinmunes, inmunodeficiencias.\n* **Prevención/Combate:** Sueño reparador, buena nutrición y esquemas de vacunación al día."
    elif "sistema muscular" in q_norm or "locomotor" in q_norm:
        answer = "💪 **Sistema Muscular:**\n* **Función:** Permite el movimiento, la postura y genera calor corporal junto al sistema óseo.\n* **Enfermedades comunes:** Desgarros, distrofias musculares, fibromialgia.\n* **Prevención/Combate:** Estiramientos previos al ejercicio, hidratación y aporte adecuado de proteínas."
    elif "sistema excretor" in q_norm or "riñon" in q_norm:
        answer = "💧 **Sistema Excretor (Urinario):**\n* **Función:** Filtra la sangre en los riñones para eliminar desechos metabólicos a través de la orina.\n* **Enfermedades comunes:** Insuficiencia renal, cálculos renales (nefrolitiasis), infecciones urinarias.\n* **Prevención/Combate:** Alto consumo de agua, reducir el exceso de sal y control médico periódico."
    elif "sistema reproductor" in q_norm:
        answer = "👶 **Sistema Reproductor:**\n* **Función:** Encargado de la perpetuación de la especie mediante la producción de células sexuales y hormonas.\n* **Enfermedades comunes:** Infecciones de transmisión sexual (ITS), trastornos ováricos/prostáticos.\n* **Prevención/Combate:** Prácticas de protección, higiene adecuada y chequeos ginecológicos/urológicos."
    elif "rodilla" in q_norm:
        answer = "🦵 **La Rodilla:**\n* **Función:** Articulación compleja que une el fémur con la tibia, soportando el peso y permitiendo la flexión.\n* **Enfermedades comunes:** Lesiones de meniscos, rotura de ligamentos, artrosis.\n* **Prevención/Combate:** Fortalecimiento del cuádriceps, evitar impactos bruscos y control de peso corporal."
    elif "ojo" in q_norm or "ojos" in q_norm:
        answer = "👁️ **Los Ojos:**\n* **Función:** Captan estímulos luminosos y los transforman en impulsos eléctricos interpretados por el cerebro.\n* **Enfermedades comunes:** Miopía, astigmatismo, cataratas, conjuntivitis.\n* **Prevención/Combate:** Descanso visual ante pantallas, uso de protección UV y revisiones oftalmológicas."
    else:
        answer = f"🔍 He registrado tu consulta sobre *'{user_question}'*. Para ofrecerte una respuesta exacta y directa, por favor indícame el sistema específico (ej. esquelético, circulatorio, nervioso, etc.) u órgano que deseas consultar."

    # Mostrar y guardar respuesta
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.local_chat_messages.append({"role": "assistant", "content": answer})
