import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Asistente Amigable del Cuerpo Humano",
    page_icon="🧬",
    layout="centered"
)

# Título y descripción principal
st.title("🧬 Tu Guía Amigable del Cuerpo Humano")
st.write("¡Hola! Pregúntame lo que quieras sobre anatomía, órganos, sistemas o cómo funciona nuestro organismo. ¡Estoy aquí para explicártelo de forma sencilla!")

# Aviso médico de responsabilidad
st.info("⚠️ **Aviso informativo:** Este chat tiene fines educativos y de divulgación científica. No sustituye la consulta médica profesional.")

# Inicializar el historial del chat
if "body_chat_messages" not in st.session_state:
    st.session_state.body_chat_messages = [
        {"role": "assistant", "content": "¡Hola! Qué gusto saludarte 😊. ¿Qué te gustaría descubrir hoy sobre el cuerpo humano? Puedes preguntarme sobre el corazón, el cerebro, los huesos o cualquier curiosidad."}
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

    # Procesar la respuesta inteligente y amigable
    q_lower = user_question.lower()
    
    # 1. Saludos y cortesía
    if any(w in q_lower for w in ["hola", "saludos", "buenas", "qué tal", "hey"]):
        answer = "¡Hola de nuevo! 👋 Qué bueno tener esta charla contigo. Dime, ¿qué parte del cuerpo humano te da curiosidad hoy?"
    elif any(w in q_lower for w in ["gracias", "excelente", "genial", "buen trabajo", "te agradezco"]):
        answer = "¡De nada! Me alegra mucho poder ayudarte a conocer más sobre nuestra increíble biología. ¿Tienes alguna otra duda? ✨"
    
    # 2. Corazón y sistema circulatorio
    elif any(w in q_lower for w in ["corazón", "latidos", "sangre", "circulación", "arterias", "venas"]):
        answer = "❤️ **¡Hablemos del corazón!**\nEs un órgano fascinante: es un músculo que actúa como una bomba perfecta. Late unas 100,000 veces al día y mueve la sangre por miles de kilómetros de vasos sanguíneos en tu cuerpo para llevar oxígeno a cada rincón. ¿Te gustaría saber cómo se oxigena la sangre?"
    
    # 3. Cerebro y sistema nervioso
    elif any(w in q_lower for w in ["cerebro", "mente", "neuronas", "pensar", "memoria", "encéfalo"]):
        answer = "🧠 **¡El supercerebro!**\nEs el centro de mando de todo tu cuerpo. Contiene cerca de 86 mil millones de neuronas que se comunican mediante impulsos eléctricos rapidísimos. Controla tus movimientos, tus recuerdos, tus emociones y hasta tus sueños cuando duermes. ¿Qué te sorprende más de la mente?"
    
    # 4. Digestión y estómago
    elif any(w in q_lower for w in ["estómago", "digestión", "intestino", "comer", "comida", "hígado", "alimento"]):
        answer = "🍏 **El viaje de la comida (Sistema Digestivo):**\n¡Es todo un proceso de transformación! Comienza en tu boca y recorre un tubo de unos 9 metros. El estómago usa ácidos fuertes para triturar los alimentos, y luego el intestino delgado absorbe todos los nutrientes que te dan energía. ¿Quieres saber cuánto tarda el cuerpo en digerir?"
    
    # 5. Pulmones y respiración
    elif any(w in q_lower for w in ["pulmones", "respirar", "aire", "oxígeno", "respiratorio", "oxigeno"]):
        answer = "🫁 **Los pulmones y el aire:**\nCada vez que respiras, tus pulmones expanden millones de pequeños saquitos llamados alvéolos para capturar el oxígeno del aire y pasarlo directo a la sangre, mientras expulsan el dióxido de carbono. ¡Es un ciclo automático vital!"
    
    # 6. Huesos y esqueleto
    elif any(w in q_lower for w in ["huesos", "esqueleto", "fémur", "columna", "articulaciones", "ehuesos", "hueso"]):
        answer = "🦴 **El sistema óseo (¡Tus huesos!):**\nUn adulto tiene 206 huesos. El más largo y fuerte es el fémur en la pierna. Aunque parecen simples estructuras duras, ¡están vivos!, se regeneran constantemente y en su interior (la médula ósea) se producen las células de la sangre."
    
    # 7. Músculos
    elif any(w in q_lower for w in ["músculos", "muscular", "fuerza", "movimiento", "musculos"]):
        answer = "💪 **El sistema muscular:**\nTenemos más de 600 músculos. Gracias a ellos podemos sonreír, caminar, correr y levantar objetos. Trabajan en equipo con los huesos como si fueran palancas. ¿Sabías que para sonreír usas muchos menos músculos que para enojarte?"
    
    # 8. Riñones y sistema excretor
    elif any(w in q_lower for w in ["riñón", "riñones", "orina", "filtrar", "agua", "toxinas"]):
        answer = "💧 **Los riñones, tus filtros naturales:**\nTus riñones limpian y filtran la sangre de tu cuerpo unas 40 veces al día, eliminando los desechos y el exceso de líquido en forma de orina. Por eso es tan importante tomar agua regularmente para cuidarlos."
    
    # 9. Piel y sentido del tacto
    elif any(w in q_lower for w in ["piel", "tacto", "órgano más grande", "sudor"]):
        answer = "✨ **La piel, el órgano más grande:**\n¡Así es! La piel cubre todo tu cuerpo, te protege de las bacterias, regula tu temperatura mediante el sudor y te permite sentir el tacto, el frío y el calor gracias a millones de terminaciones nerviosas."
    
    # 3. Respuesta por defecto más amable si no coincide con las anteriores
    else:
        answer = f"🤔 Es una pregunta muy interesante. El cuerpo humano es tan asombroso que conecta muchísimos sistemas a la vez. Aunque no tengo una respuesta exacta para *'{user_question}'*, te invito a preguntarme sobre órganos específicos como el corazón, el cerebro, los pulmones, los huesos o la digestión. ¡Dime cuál te llama más la atención!"

    # Mostrar y guardar la respuesta generada
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.body_chat_messages.append({"role": "assistant", "content": answer})
