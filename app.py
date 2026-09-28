import streamlit as st
import unicodedata

# Configuración de la página optimizada para celulares
st.set_page_config(
    page_title="Asistente TerrahealtH",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS con colores bonitos, modernos y adaptados a móviles
st.markdown("""
    <style>
    /* Fondo general suave con un toque moderno */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    .main { padding: 0rem 0.5rem; }
    
    /* Título principal estilizado */
    h1 {
        font-size: 1.8rem !important;
        color: #0f4c81;
        text-align: center;
        margin-bottom: 0.1rem;
        font-weight: 700;
    }
    
    p { font-size: 0.95rem !important; color: #333333; }
    
    /* Estilo elegante para las burbujas del chat */
    .stChatMessage {
        border-radius: 14px;
        padding: 0.6rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Caja de advertencia estética */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid #0f4c81;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧬 Asistente TerrahealtH")
st.markdown("<p style='text-align: center; color: #5a6a85;'>✨ Tu guía inteligente de anatomía y salud con respuestas rápidas y específicas. ✨</p>", unsafe_allow_html=True)

st.info("⚠️ **Aviso:** Fines educativos y científicos. No sustituye la consulta médica profesional.")

# Inicializar historial de chat local con el saludo gracioso y emoticons bonitos
if "local_chat_messages" not in st.session_state:
    st.session_state.local_chat_messages = [
        {"role": "assistant", "content": "¡Hola terrícola! 👽🤖 Soy tu asistente **TerrahealtH** 🌍✨. Pregúntame sobre cualquier sistema u órgano (como el hígado 🩺, páncreas 🧬, rodilla 🦵, etc.) y te daré una respuesta corta, directa y muy útil 🚀."}
    ]

# Mostrar historial
for message in st.session_state.local_chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def normalizar_texto(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn').lower()

# Entrada de texto del usuario
if user_question := st.chat_input("Escribe tu pregunta directa... ✍️"):
    st.session_state.local_chat_messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    q_norm = normalizar_texto(user_question)
    answer = ""

    # Saludos y cortesía cortos
    if any(w in q_norm for w in ["hola", "saludos", "buenas", "que tal", "hey"]):
        answer = "¡Hola terrícola! 👽 ¿Qué órgano 🫀 o sistema 🧬 deseas consultar hoy en TerrahealtH?"
    elif any(w in q_norm for w in ["gracias", "excelente", "genial"]):
        answer = "¡De nada, terrícola! ✨ ¿Tienes alguna otra consulta anatómica o de salud? 🚀"

    # 1. ÓRGANOS Y ESTRUCTURAS ESPECÍFICAS
    elif "higado" in q_norm:
        answer = "🩺 **El Hígado:**\n* **Función:** Órgano interno más grande; desintoxica la sangre, metaboliza nutrientes, almacena glucógeno y produce bilis[cite: 11].\n* **Enfermedades comunes:** Hígado graso, hepatitis, cirrosis.\n* **Prevención/Combate:** Evitar exceso de alcohol, mantener dieta equilibrada y control médico."
    elif "pancreas" in q_norm:
        answer = "🧬 **El Páncreas:**\n* **Función:** Glándula mixta; función endocrina (produce insulina y glucagón) y exocrina (jugos pancreáticos para la digestión)[cite: 11].\n* **Enfermedades comunes:** Pancreatitis, diabetes, cáncer de páncreas.\n* **Prevención/Combate:** Dieta baja en grasas, evitar alcohol y chequeos de glucosa."
    elif "corazon" in q_norm:
        answer = "❤️ **El Corazón:**\n* **Función:** Bombea sangre oxigenada y nutrientes por todo el sistema circulatorio[cite: 10, 19].\n* **Enfermedades comunes:** Hipertensión, infarto agudo de miocardio, arritmias[cite: 19].\n* **Prevención/Combate:** Ejercicio cardiovascular, dieta saludable y control de presión arterial."
    elif "riñon" in q_norm or "riñones" in q_norm:
        answer = "💧 **Los Riñones:**\n* **Función:** Filtran la sangre para eliminar desechos y regular líquidos y presión arterial[cite: 14].\n* **Enfermedades comunes:** Insuficiencia renal, cálculos renales (piedras), infecciones.\n* **Prevención/Combate:** Beber abundante agua, reducir sal y evitar automedicación nefrotóxica."
    elif "rodilla" in q_norm:
        answer = "🦵 **La Rodilla:**\n* **Función:** Articulación compleja que une el fémur con la tibia, permitiendo la movilidad y soporte de peso[cite: 5].\n* **Enfermedades comunes:** Lesiones de meniscos, rotura de ligamentos, artrosis[cite: 5].\n* **Prevención/Combate:** Fortalecimiento muscular, evitar impactos fuertes y control de peso."
    elif "ojo" in q_norm or "ojos" in q_norm:
        answer = "👁️ **Los Ojos:**\n* **Función:** Captan estímulos lumínicos en la retina para procesar la visión a través del nervio óptico[cite: 18].\n* **Enfermedades comunes:** Miopía, astigmatismo, cataratas, conjuntivitis[cite: 18].\n* **Prevención/Combate:** Descanso visual, protección UV y exámenes oftalmológicos."

    # 2. SISTEMAS COMPLETOS
    elif "sistema oseo" in q_norm or "esqueleto" in q_norm:
        answer = "🦴 **Sistema Esquelético:**\n* **Función:** 206 huesos que brindan soporte, protección a órganos y almacenamiento de minerales[cite: 6].\n* **Enfermedades comunes:** Osteoporosis, fracturas, artritis.\n* **Prevención/Combate:** Consumo de calcio, vitamina D y ejercicio de fuerza."
    elif "sistema nervioso" in q_norm:
        answer = "🧠 **Sistema Nervioso:**\n* **Función:** Controla funciones corporales mediante el SNC (cerebro, médula) y nervios periféricos[cite: 7, 16].\n* **Enfermedades comunes:** Alzheimer, epilepsia, neuropatías.\n* **Prevención/Combate:** Buen descanso, estimulación mental y evitar tóxicos."
    elif "sistema endocrino" in q_norm or "hormonas" in q_norm:
        answer = "🧪 **Sistema Endocrino:**\n* **Función:** Regula procesos corporales mediante secreción de hormonas (tiroides, suprarrenales, etc.)[cite: 8, 17].\n* **Enfermedades comunes:** Diabetes, hipotiroidismo.\n* **Prevención/Combate:** Dieta equilibrada y control metabólico."
    elif "sistema respiratorio" in q_norm or "pulmones" in q_norm:
        answer = "🫁 **Sistema Respiratorio:**\n* **Función:** Intercambio de oxígeno y dióxido de carbono mediante vías aéreas y alvéolos[cite: 9, 18].\n* **Enfermedades comunes:** Asma, EPOC, neumonía[cite: 12, 18].\n* **Prevención/Combate:** No fumar y evitar ambientes contaminados[cite: 9, 18]."
    elif "sistema circulatorio" in q_norm:
        answer = "❤️ **Sistema Circulatorio:**\n* **Función:** Distribuye sangre, oxígeno y nutrientes mediante el corazón, arterias y venas[cite: 10, 19].\n* **Enfermedades comunes:** Hipertensión, infartos[cite: 19].\n* **Prevención/Combate:** Dieta baja en grasas y ejercicio."
    elif "sistema digestivo" in q_norm or "estomago" in q_norm:
        answer = "🍏 **Sistema Digestivo:**\n* **Función:** Descompone alimentos y absorbe nutrientes a lo largo del tracto gastrointestinal[cite: 11].\n* **Enfermedades comunes:** Gastritis, úlceras, colitis.\n* **Prevención/Combate:** Hidratación, fibra y evitar irritantes."
    elif "sistema inmunologico" in q_norm or "defensas" in q_norm:
        answer = "🛡️ **Sistema Inmunológico:**\n* **Función:** Defiende al organismo contra patógenos mediante órganos especializados y glóbulos blancos[cite: 12].\n* **Enfermedades comunes:** Alergias, asma, enfermedades autoinmunes[cite: 12].\n* **Prevención/Combate:** Vacunación, nutrición adecuada y buen descanso."
    elif "sistema muscular" in q_norm or "locomotor" in q_norm:
        answer = "💪 **Sistema Muscular:**\n* **Función:** Permite el movimiento y la postura junto al sistema esquelético[cite: 13].\n* **Enfermedades comunes:** Desgarros, distrofias, fibromialgia.\n* **Prevención/Combate:** Estiramientos, hidratación y proteínas."
    elif "sistema excretor" in q_norm:
        answer = "💧 **Sistema Excretor (Urinario):**\n* **Función:** Filtra la sangre en los riñones para eliminar desechos a través de la orina[cite: 14].\n* **Enfermedades comunes:** Cálculos renales, infecciones urinarias.\n* **Prevención/Combate:** Tomar agua y moderar la sal."
    elif "sistema reproductor" in q_norm:
        answer = "👶 **Sistema Reproductor:**\n* **Función:** Encargado de la perpetuación de la especie mediante células sexuales y hormonas[cite: 15].\n* **Enfermedades comunes:** ITS, trastornos prostáticos u ováricos.\n* **Prevención/Combate:** Protección adecuada y chequeos médicos periódicos."
    else:
        answer = f"🔍 Consulta sobre *'{user_question}'*. Por favor, indícame un órgano 🫀 (ej. hígado, páncreas, corazón) o sistema específico 🧬 (ej. esquelético, respiratorio, digestivo) para darte la información exacta."

    # Mostrar y guardar respuesta
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.local_chat_messages.append({"role": "assistant", "content": answer})
