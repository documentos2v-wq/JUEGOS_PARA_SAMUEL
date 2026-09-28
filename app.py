import streamlit as st
import unicodedata

# Configuración de la página
st.set_page_config(
    page_title="Asistente Experto del Cuerpo Humano",
    page_icon="🧬",
    layout="centered"
)

st.title("🧬 Asistente Inteligente del Cuerpo Humano")
st.write("Pregúntame sobre cualquier órgano, extremidad, sistema, función o enfermedad del cuerpo humano. ¡Tengo una base de conocimientos completa!")

st.info("⚠️ **Aviso informativo:** Este chat tiene fines educativos y científicos. No sustituye la consulta médica profesional.")

# Inicializar el historial del chat
if "local_chat_messages" not in st.session_state:
    st.session_state.local_chat_messages = [
        {"role": "assistant", "content": "¡Hola! 👋 Soy tu asistente biológico y médico. Pregúntame sobre el páncreas, el hígado, las manos, los ojos, el sistema nervioso o cualquier duda que tengas."}
    ]

# Mostrar historial de mensajes
for message in st.session_state.local_chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def normalizar_texto(texto):
    """Elimina tildes y pasa a minúsculas para una búsqueda flexible"""
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn').lower()

# Cuadro de entrada de texto
if user_question := st.chat_input("Escribe tu pregunta sobre el cuerpo humano..."):
    st.session_state.local_chat_messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    q_norm = normalizar_texto(user_question)
    answer = ""

    # 1. Saludos y cortesía
    if any(w in q_norm for w in ["hola", "saludos", "buenas", "que tal", "hey"]):
        answer = "¡Hola! 👋 Qué gusto saludarte. ¿Qué tema del cuerpo humano o de salud te gustaría explorar hoy?"
    elif any(w in q_norm for w in ["gracias", "excelente", "genial", "buen trabajo"]):
        answer = "¡De nada! Me alegra mucho poder ayudarte a comprender mejor cómo funciona nuestro organismo. ✨"
    
    # 2. Base de conocimientos ampliada y detallada
    elif any(w in q_norm for w in ["pancreas", "pancreatico"]):
        answer = " pancreas **El Páncreas:**\nEs un órgano glandular vital localizado en el abdomen, detrás del estomago. Tiene dos funciones principales:\n* **Función Endocrina:** Produce hormonas esenciales como la *insulina* y el *glucagón*, encargadas de regular los niveles de azúcar (glucosa) en la sangre.\n* **Función Exocrina:** Produce jugos gástricos y enzimas (como la amilasa y la lipasa) que se liberan en el intestino delgado para descomponer grasas, proteínas y carbohidratos.\n\n🩺 **¿Por qué se enferma?**\nLas principales patologías del páncreas son la *pancreatitis* (inflamación aguda o crónica causada por cálculos biliares o consumo excesivo de alcohol) y el *cáncer de páncreas*."
    elif any(w in q_norm for w in ["ojo", "ojos", "vision", "ver"]):
        answer = "👁️ **Los Ojos y la Visión:**\nSon los órganos sensoriales responsables de captar la luz del entorno. La luz atraviesa la córnea, la pupila y el cristalino para proyectarse en la retina, donde las células fotorreceptoras (bastones y conos) convierten las imágenes en impulsos eléctricos que el cerebro interpreta a través del nervio óptico."
    elif any(w in q_norm for w in ["higado", "hepatitis", "cirrosis", "hepatico"]):
        answer = "🩺 **El Hígado y sus Enfermedades:**\nEs el órgano interno más grande del cuerpo. Se encarga de desintoxicar la sangre, procesar nutrientes y producir bilis. \n* **Causas de enfermedad:** El consumo excesivo de alcohol, el hígado graso no alcohólico (relacionado con la obesidad y mala alimentación), y las infecciones virales (como las hepatitis A, B y C)."
    elif any(w in q_norm for w in ["pie", "pies", "tobillo", "dedos del pie"]):
        answer = "🦶 **Sobre los Pies:**\nCada pie cuenta con **26 huesos** (lo que suma 52 huesos entre ambos, la cuarta parte de todo el cuerpo humano), 33 articulaciones y más de 100 músculos, tendones y ligamentos que soportan todo nuestro peso."
    elif any(w in q_norm for w in ["mano", "manos", "muñeca", "dedos"]):
        answer = "✋ **Sobre las Manos:**\nLas manos humanas están compuestas por 27 huesos cada una. Poseen una enorme cantidad de terminaciones nerviosas que les otorgan una sensibilidad táctil extraordinaria."
    elif any(w in q_norm for w in ["corazon", "latidos", "sangre", "circulacion"]):
        answer = "❤️ **El Corazón y el Sistema Circulatorio:**\nEs un músculo en forma de bomba que late unas 100,000 veces al día, impulsando sangre oxigenada por una red de miles de kilómetros de vasos sanguíneos."
    elif any(w in q_norm for w in ["cerebro", "mente", "neuronas", "pensar"]):
        answer = "🧠 **El Cerebro y el Sistema Nervioso:**\nEs el centro de control del cuerpo. Contiene miles de millones de neuronas que coordinan los pensamientos, las emociones, los movimientos y los sentidos."
    elif any(w in q_norm for w in ["pulmones", "respirar", "aire", "oxigeno", "fumar"]):
        answer = "🫁 **Los Pulmones y la Respiración:**\nPermiten el intercambio gaseoso: absorben oxígeno hacia la sangre y expulsan dióxido de carbono. El humo del tabaco daña los alvéolos pulmonares."
    elif any(w in q_norm for w in ["estomago", "gestion", "intestino", "comer", "alimento"]):
        answer = "🍏 **El Sistema Digestivo:**\nDescompone los alimentos mediante ácidos gástricos y enzimas para absorber los nutrientes necesarios para la obtención de energía."
    elif any(w in q_norm for w in ["riñon", "riñones", "orina", "filtrar"]):
        answer = "💧 **Los Riñones:**\nFiltran aproximadamente 150 litros de sangre al día para eliminar toxinas y regular la presión arterial y el equilibrio de líquidos."
    elif any(w in q_norm for w in ["huesos", "esqueleto", "femur"]):
        answer = "🦴 **El Sistema Óseo:**\nCompuesto por 206 huesos en la edad adulta. Sostienen el cuerpo, protegen órganos vitales y almacenan minerales como el calcio."
    elif any(w in q_norm for w in ["piel", "tacto", "sudor"]):
        answer = "✨ **La Piel:**\nEs el órgano más grande del cuerpo humano. Actúa como barrera protectora contra patógenos externos y regula la temperatura corporal."
    else:
        answer = f"🔍 He analizado tu consulta sobre *'{user_question}'*. El cuerpo humano opera mediante la sinergia de múltiples sistemas interconectados. ¿Te gustaría profundizar en algún órgano específico como el páncreas, el hígado o el corazón?"

    # Mostrar y guardar la respuesta
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.local_chat_messages.append({"role": "assistant", "content": answer})
