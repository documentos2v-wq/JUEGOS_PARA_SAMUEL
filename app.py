import streamlit as st
import unicodedata

# Configuración de la página
st.set_page_config(
    page_title="Asistente Experto del Cuerpo Humano",
    page_icon="🧬",
    layout="centered"
)

st.title("🧬 Asistente Inteligente del Cuerpo Humano")
st.write("Pregúntame sobre cualquier órgano, extremidad, sistema, función, partes o enfermedad del cuerpo humano. ¡Tengo una base de conocimientos completa!")

st.info("⚠️ **Aviso informativo:** Este chat tiene fines educativos y científicos. No sustituye la consulta médica profesional.")

# Inicializar el historial del chat
if "local_chat_messages" not in st.session_state:
    st.session_state.local_chat_messages = [
        {"role": "assistant", "content": "¡Hola! 👋 Soy tu asistente biológico y médico. Pregúntame sobre la rodilla, los ojos, el páncreas, el hígado o cualquier duda que tengas."}
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
        answer = "¡Hola, Samuel! 👋 Qué gusto saludarte. ¿Qué tema del cuerpo humano o de salud te gustaría explorar hoy?"
    elif any(w in q_norm for w in ["gracias", "excelente", "genial", "buen trabajo"]):
        answer = "¡De nada! Me alegra mucho poder ayudarte a comprender mejor cómo funciona nuestro organismo. ✨"
    
    # 2. Base de conocimientos depurada y corregida
    elif any(w in q_norm for w in ["rodilla", "rodillas", "rotula"]):
        answer = "🦵 **Sobre la Rodilla y sus Partes:**\nLa rodilla es la articulación más grande y compleja del cuerpo humano. Conecta el fémur con la tibia y está compuesta por:\n* **Rótula (patela):** Hueso sesamoideo que protege la articulación y mejora la palanca del músculo cuádriceps.\n* **Meniscos:** Almohadillas de cartílago en forma de C que actúan como amortiguadores de impactos.\n* **Ligamentos (cruzados y colaterales):** Bandas de tejido fibroso que dan estabilidad y evitan movimientos excesivos.\n* **Cartílago articular:** Reviste los extremos de los huesos para permitir un movimiento suave sin fricción."
    elif any(w in q_norm for w in ["ojo", "ojos", "vision", "ver", "cornea", "pupila"]):
        answer = "👁️ **Los Ojos y sus Partes Principales:**\nLos ojos son los órganos de la visión. Sus estructuras principales incluyen:\n* **Córnea:** Lente transparente externa que ayuda a enfocar la luz.\n* **Pupila:** Orificio central que regula el paso de la luz.\n* **Iris:** Parte coloreada que controla el tamaño de la pupila.\n* **Cristalino:** Lente flexible que enfoca objetos a diferentes distancias.\n* **Retina:** Capa posterior con células fotorreceptoras (bastones y conos).\n* **Nervio óptico:** Transmite la información visual hacia el cerebro."
    elif any(w in q_norm for w in ["pancreas", "pancreatico"]):
        answer = "🩺 **El Páncreas y sus Funciones:**\nEs un órgano glandular ubicado en el abdomen con dos roles clave:\n* **Función Endocrina:** Produce *insulina* y *glucagón* para regular la glucosa en la sangre.\n* **Función Exocrina:** Produce enzimas digestivas (amilasa, lipasa) para descomponer alimentos."
    elif any(w in q_norm for w in ["higado", "hepatitis", "cirrosis", "hepatico"]):
        answer = "🩺 **El Hígado y sus Enfermedades:**\nEs el órgano interno más grande. Se encarga de desintoxicar la sangre, procesar nutrientes y generar bilis. Sus enfermedades comunes derivan del alcohol, hígado graso o infecciones virales."
    elif any(w in q_norm for w in ["pie", "pies", "tobillo", "dedos del pie"]):
        answer = "🦶 **Sobre los Pies:**\nCada pie cuenta con **26 huesos** (52 en total entre ambos), 33 articulaciones y más de 100 músculos, tendones y ligamentos."
    elif any(w in q_norm for w in ["mano", "manos", "muñeca", "dedos"]):
        answer = "✋ **Sobre las Manos:**\nCompuestas por 27 huesos cada una. Poseen una alta concentración de terminaciones nerviosas que otorgan sensibilidad táctil y destreza."
    elif any(w in q_norm for w in ["corazon", "latidos", "sangre", "circulacion"]):
        answer = "❤️ **El Corazón:**\nMúsculo en forma de bomba que late unas 100,000 veces al día, impulsando sangre oxigenada por todo el sistema circulatorio."
    elif any(w in q_norm for w in ["cerebro", "mente", "neuronas", "pensar"]):
        answer = "🧠 **El Cerebro:**\nCentro de control del sistema nervioso. Contiene miles de millones de neuronas que coordinan pensamientos, emociones y movimientos."
    elif any(w in q_norm for w in ["pulmones", "respirar", "aire", "oxigeno", "fumar"]):
        answer = "🫁 **Los Pulmones:**\nRealizan el intercambio gaseoso absorbiendo oxígeno hacia la sangre y expulsando dióxido de carbono a través de los alvéolos."
    elif any(w in q_norm for w in ["estomago", "gestion", "intestino", "comer", "alimento"]):
        answer = "🍏 **El Sistema Digestivo:**\nDescompone los alimentos mediante ácidos y enzimas para la absorción celular de nutrientes."
    elif any(w in q_norm for w in ["riñon", "riñones", "orina", "filtrar"]):
        answer = "💧 **Los Riñones:**\nFiltran unos 150 litros de sangre diarios para eliminar toxinas y regular la presión arterial y líquidos."
    elif any(w in q_norm for w in ["huesos", "esqueleto", "femur"]):
        answer = "🦴 **El Sistema Óseo:**\nFormado por 206 huesos que brindan soporte estructural, protegen órganos vitales y almacenan minerales."
    elif any(w in q_norm for w in ["piel", "tacto", "sudor"]):
        answer = "✨ **La Piel:**\nÓrgano más grande del cuerpo que actúa como barrera inmunológica y regula la temperatura térmica."
    else:
        answer = f"🔍 He analizado tu consulta sobre *'{user_question}'*. El cuerpo humano opera mediante la sinergia de múltiples sistemas interconectados. ¿Te gustaría profundizar en algún órgano o parte específica como la rodilla, el corazón o el hígado?"

    # Mostrar y guardar la respuesta
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.local_chat_messages.append({"role": "assistant", "content": answer})
