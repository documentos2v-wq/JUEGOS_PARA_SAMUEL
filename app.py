import streamlit as st
import unicodedata

# Configuración de la página
st.set_page_config(
    page_title="Enciclopedia Global del Cuerpo Humano",
    page_icon="🧬",
    layout="centered"
)

st.title("🧬 Enciclopedia Global y Asistente del Cuerpo Humano")
st.write("Pregúntame sobre cualquier parte, órgano, extremidad, sistema o causa de enfermedad del cuerpo humano. ¡Tengo un amplio conocimiento integrado!")

st.info("⚠️ **Aviso informativo:** Este chat tiene fines educativos y científicos. No sustituye la consulta médica profesional.")

# Inicializar el historial del chat
if "global_chat_messages" not in st.session_state:
    st.session_state.global_chat_messages = [
        {"role": "assistant", "content": "¡Hola! 👋 Estoy listo para ayudarte. Pregúntame sobre los pies, las manos, enfermedades del hígado, el sistema nervioso o cualquier duda que tengas."}
    ]

# Mostrar historial de mensajes
for message in st.session_state.global_chat_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def normalizar_texto(texto):
    """Elimina tildes y pasa a minúsculas para una búsqueda mucho más flexible"""
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn').lower()

# Cuadro de entrada de texto
if user_question := st.chat_input("Escribe tu pregunta sobre el cuerpo humano..."):
    st.session_state.global_chat_messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    q_norm = normalizar_texto(user_question)
    answer = ""

    # 1. Saludos y cortesía
    if any(w in q_norm for w in ["hola", "saludos", "buenas", "que tal", "hey"]):
        answer = "¡Hola! 👋 Qué gusto saludarte. ¿Qué tema del cuerpo humano o de salud te gustaría explorar hoy?"
    elif any(w in q_norm for w in ["gracias", "excelente", "genial", "buen trabajo"]):
        answer = "¡De nada! Me alegra mucho poder ayudarte a comprender mejor cómo funciona nuestro organismo. ✨"
    
    # 2. Base de conocimientos global ampliada (Extremidades, órganos, causas y enfermedades)
    elif any(w in q_norm for w in ["pie", "pies", "tobillo", "dedos del pie"]):
        answer = "🦶 **Sobre los Pies:**\nEl pie humano es una estructura biomecánica compleja y una verdadera obra maestra de la evolución. Cada pie cuenta con **26 huesos** (lo que suma 52 huesos entre ambos, es decir, la cuarta parte de todos los huesos de tu cuerpo), 33 articulaciones, y más de 100 músculos, tendones y ligamentos. Soportan todo nuestro peso corporal y actúan como amortiguadores al caminar o correr."
    elif any(w in q_norm for w in ["mano", "manos", "muñeca", "dedos"]):
        answer = "✋ **Sobre las Manos:**\nLas manos humanas son herramientas de precisión extraordinarias compuestas por 27 huesos cada una. Poseen una enorme cantidad de terminaciones nerviosas que las hacen extremadamente sensibles al tacto, permitiéndonos realizar desde tareas delicadas hasta ejercer gran fuerza."
    elif any(w in q_norm for w in ["higado hepatico", "higado se enferme", "enfermar el higado", "enfermedades del higado", "hepatitis", "cirrosis", "higado"]):
        answer = "🩺 **Causas de que el Hígado se Enferme:**\nEl hígado es el órgano encargado de desintoxicar la sangre, procesar nutrientes y producir bilis. Las principales causas por las que puede enfermarse (como hígado graso, hepatitis o cirrosis) incluyen:\n* **Consumo excesivo de alcohol:** Daña y cicatriza las células hepáticas.\n* **Mala alimentación y obesidad:** Provocan acumulación de grasa (hígado graso no alcohólico).\n* **Infecciones virales:** Como los virus de la hepatitis A, B y C.\n* **Uso excesivo de ciertos medicamentos o tóxicos:** Sobredosis de fármacos como el paracetamol sin supervisión médica."
    elif any(w in q_norm for w in ["corazon", "latidos", "sangre", "circulacion"]):
        answer = "❤️ **El Corazón y el Sistema Circulatorio:**\nEs un órgano muscular que bombea sangre a todo el cuerpo. Late unas 100,000 veces al día, recorriendo una red de más de 96,000 kilómetros de vasos sanguíneos para suministrar oxígeno y nutrientes."
    elif any(w in q_norm for w in ["cerebro", "mente", "neuronas", "pensar"]):
        answer = "🧠 **El Cerebro y el Sistema Nervioso:**\nControla todas las funciones del cuerpo, procesa información sensorial, emociones y pensamientos gracias a sus casi 86 mil millones de neuronas conectadas mediante sinapsis eléctricas y químicas."
    elif any(w in q_norm for w in ["pulmones", "respirar", "aire", "oxigeno", "fumar"]):
        answer = "🫁 **Los Pulmones y la Respiración:**\nPermiten el intercambio gaseoso: absorben oxígeno del aire ambiental hacia la sangre y expulsan dióxido de carbono. El humo del tabaco y la contaminación dañan los alvéolos pulmonares, dificultando este proceso."
    elif any(w in q_norm for w in ["estomago", "gestion", "intestino", "comer", "alimento"]):
        answer = "🍏 **El Sistema Digestivo:**\nDescompone los alimentos en moléculas pequeñas mediante ácidos gástricos y enzimas para que las células puedan absorber los nutrientes necesarios para obtener energía y reparar tejidos."
    elif any(w in q_norm for w in ["riñon", "riñones", "orina", "filtrar"]):
        answer = "💧 **Los Riñones:**\nFiltran aproximadamente 150 litros de sangre al día para eliminar toxinas, exceso de sales y agua, produciendo orina y regulando la presión arterial y el equilibrio electrolítico."
    elif any(w in q_norm for w in ["huesos", "esqueleto", "femur"]):
        answer = "🦴 **El Sistema Óseo:**\nCompuesto por 206 huesos en la edad adulta. Sostienen el cuerpo, protegen órganos internos vitales (como el cráneo al cerebro) y almacenan minerales esenciales como el calcio."
    elif any(w in q_norm for w in ["piel", "tacto", "sudor"]):
        answer = "✨ **La Piel:**\nEs el órgano más grande del cuerpo humano. Actúa como barrera protectora contra patógenos externos, regula la temperatura corporal y alberga los receptores sensoriales del tacto."
    else:
        answer = f"🔍 He analizado tu consulta sobre *'{user_question}'*. Aunque es un tema muy específico, el cuerpo humano funciona mediante la integración de múltiples sistemas (nervioso, endocrino, circulatorio, etc.). ¿Te gustaría que profundicemos en algún órgano, extremidad o condición médica relacionada?"

    # Mostrar y guardar la respuesta
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.global_chat_messages.append({"role": "assistant", "content": answer})
