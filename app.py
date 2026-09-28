import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Portal de Samuel - Juegos y Salud",
    page_icon="⚡",
    layout="wide"
)

# Estilo global para limpiar la interfaz de Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Portal Interactivo de Samuel")

# Pestañas principales para separar el juego y el chat de salud limpiamente
tab1, tab2 = st.tabs(["🧠 Reto Mental Infinito", "💬 Chat de Consejos de Salud"])

with tab1:
    st.subheader("Reto Mental: Preguntas Capciosas y Adivinanzas (Modo Infinito)")
    
    # Juego enbebido con el emoji interactivo
    game_html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                background-color: #0b0f19;
                color: #f8fafc;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                width: 100%;
                height: 520px;
                padding: 20px;
                border-radius: 14px;
                border: 2px solid #38bdf8;
            }
            .stats {
                display: flex;
                justify-content: space-between;
                font-size: 18px;
                font-weight: bold;
                color: #38bdf8;
                border-bottom: 2px solid #1e293b;
                padding-bottom: 8px;
            }
            .question-container {
                flex-grow: 1;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                width: 100%;
                max-width: 800px;
                margin: 0 auto;
            }
            .interactive-emoji {
                font-size: 65px;
                text-align: center;
                margin-bottom: 6px;
            }
            .thinking-anim { animation: thinkMotion 1.2s infinite alternate ease-in-out; }
            @keyframes thinkMotion {
                0% { transform: scale(1) rotate(-5deg); }
                100% { transform: scale(1.15) rotate(5deg); }
            }
            .happy-anim { animation: happyMotion 0.5s infinite alternate ease-in-out; }
            @keyframes happyMotion {
                0% { transform: translateY(0) scale(1.2); }
                100% { transform: translateY(-12px) scale(1.3); }
            }
            .angry-anim { animation: angryMotion 0.3s infinite alternate ease-in-out; }
            @keyframes angryMotion {
                0% { transform: translateX(-5px) scale(1.2); }
                100% { transform: translateX(5px) scale(1.2); }
            }
            .question-box {
                background: #0f172a;
                padding: 20px;
                border-radius: 12px;
                font-size: 20px;
                color: #ffffff;
                border-left: 6px solid #f59e0b;
                line-height: 1.4;
                text-align: center;
                margin-bottom: 15px;
                width: 100%;
                box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            }
            .options-container {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
                width: 100%;
            }
            .option-btn {
                background: #1e293b;
                color: white;
                border: 2px solid #334155;
                padding: 14px;
                font-size: 15px;
                font-weight: bold;
                border-radius: 10px;
                cursor: pointer;
                transition: 0.2s;
                text-align: left;
            }
            .option-btn:hover:not(:disabled) {
                background: #38bdf8;
                color: #000000;
                border-color: #38bdf8;
            }
            .option-btn:disabled { cursor: not-allowed; opacity: 0.7; }
            .footer-area {
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 100%;
                min-height: 40px;
                border-top: 2px solid #1e293b;
                padding-top: 8px;
            }
            #feedback { font-size: 18px; font-weight: bold; }
            #next-btn {
                background: linear-gradient(45deg, #22c55e, #16a34a);
                color: white;
                border: none;
                padding: 10px 24px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 25px;
                cursor: pointer;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="stats">
            <div id="score">Aciertos: 0</div>
            <div id="roundInfo">Modo Infinito 🎮</div>
        </div>
        <div class="question-container">
            <div id="dynamicEmoji" class="interactive-emoji thinking-anim">🤔</div>
            <div class="question-box" id="questionText">Cargando desafío mental...</div>
            <div class="options-container" id="optionsContainer"></div>
        </div>
        <div class="footer-area">
            <div id="feedback"></div>
            <button id="next-btn" onclick="loadNextQuestion()">Siguiente Reto 🚀</button>
        </div>
        <script>
            const masterQuestions = [
                { q: "¿Qué sube y baja pero siempre se queda en el mismo lugar?", options: ["La temperatura", "Las escaleras", "Una montaña rusa", "El ascensor"], answer: 1 },
                { q: "Iba con 7 perros rumbo a Lima. Cada perro llevaba 7 sacos, cada saco 7 gatos, y cada gato 7 gatitos. ¿Cuántos animales iban rumbo a Lima?", options: ["2,401 animales", "Ninguno, yo iba solo", "400 animales", "Depende del peso"], answer: 1 },
                { q: "¿De qué color son las mangas del chaleco de un abuelo?", options: ["Blancas", "Negras", "No tiene, es un chaleco", "Depende del traje"], answer: 2 },
                { q: "Si un tren eléctrico viaja de norte a sur a gran velocidad, ¿hacia dónde va el humo?", options: ["Hacia el norte", "Hacia el sur", "Hacia arriba", "Los trenes eléctricos no botan humo"], answer: 3 },
                { q: "¿Qué cosa es que, cuanto más le quitas, más grande se vuelve?", options: ["Un hoyo o zanja", "Una piedra", "Una esponja", "El dinero"], answer: 0 },
                { q: "Tengo dos monedas que suman 30 céntimos exactos y una de ellas no es de 10 céntimos. ¿Cuáles son las monedas?", options: ["Una de 20 y una de 10", "Tres de 10 céntimos", "Una de 25 y una de 5", "Dos de 15"], answer: 0 },
                { q: "¿Qué pasa si tiras un sombrero blanco al Mar Rojo?", options: ["Se hunde", "Se moja", "Se pierde", "Flota sin romperse"], answer: 1 },
                { q: "Cinco hermanos están en una cabaña jugando ajedrez. Uno lee, otro cocina, otro barre, otro juega cartas. ¿Qué hace el quinto hermano?", options: ["Duerme", "Juega ajedrez", "Lava los platos", "Mira la ventana"], answer: 1 },
                { q: "¿Cuántos animales metió Moisés en el arca de su viaje?", options: ["Una pareja de cada especie", "Muchos animales", "Cien animales", "Ninguno, fue Noé, no Moisés"], answer: 3 },
                { q: "Hijo de mi padre, pero no mi hermano. ¿Quién es?", options: ["Mi tío", "Yo mismo", "Mi hijo", "Mi sobrino"], answer: 1 }
            ];
            let availableQuestions = [], currentQuestion = null, score = 0, answered = false;
            const thinkingGestures = ["🤔", "🤨", "🧐", "🤪", "🙃", "🤫"];
            function initGame() { score = 0; refillPool(); loadNextQuestion(); }
            function refillPool() { availableQuestions = [...masterQuestions]; }
            function loadNextQuestion() {
                if (availableQuestions.length === 0) refillPool();
                answered = false;
                document.getElementById("feedback").innerText = "";
                document.getElementById("next-btn").style.display = "none";
                let randomThink = thinkingGestures[Math.floor(Math.random() * thinkingGestures.length)];
                let emojiEl = document.getElementById("dynamicEmoji");
                emojiEl.innerText = randomThink;
                emojiEl.className = "interactive-emoji thinking-anim";
                let randomIndex = Math.floor(Math.random() * availableQuestions.length);
                currentQuestion = availableQuestions.splice(randomIndex, 1)[0];
                document.getElementById("questionText").innerText = currentQuestion.q;
                document.getElementById("score").innerText = "Aciertos: " + score;
                let optContainer = document.getElementById("optionsContainer");
                optContainer.innerHTML = "";
                currentQuestion.options.forEach((opt, index) => {
                    let btn = document.createElement("button");
                    btn.classList.add("option-btn");
                    btn.innerText = opt;
                    btn.onclick = () => checkAnswer(index, btn);
                    optContainer.appendChild(btn);
                });
            }
            function checkAnswer(selectedIndex, selectedBtn) {
                if (answered) return;
                answered = true;
                let buttons = document.querySelectorAll(".option-btn");
                buttons.forEach(b => b.disabled = true);
                let feedbackDiv = document.getElementById("feedback");
                let emojiEl = document.getElementById("dynamicEmoji");
                if (selectedIndex === currentQuestion.answer) {
                    selectedBtn.style.background = "#22c55e"; selectedBtn.style.color = "#000";
                    feedbackDiv.style.color = "#22c55e"; feedbackDiv.innerText = "🎉 ¡Correcto!";
                    score++; document.getElementById("score").innerText = "Aciertos: " + score;
                    emojiEl.innerText = "🥳"; emojiEl.className = "interactive-emoji happy-anim";
                } else {
                    selectedBtn.style.background = "#ef4444";
                    buttons[currentQuestion.answer].style.background = "#22c55e"; buttons[currentQuestion.answer].style.color = "#000";
                    feedbackDiv.style.color = "#ef4444"; feedbackDiv.innerText = "❌ ¡Incorrecto!";
                    emojiEl.innerText = "😡"; emojiEl.className = "interactive-emoji angry-anim";
                }
                document.getElementById("next-btn").style.display = "block";
            }
            initGame();
        </script>
    </body>
    </html>
    """
    st.components.v1.html(game_html, height=540, scrolling=False)

with tab2:
    st.subheader("💬 Asistente Virtual de Consejos de Salud")
    st.write("Escribe tus dudas sobre bienestar, nutrición, descanso o hábitos de vida y obtén respuestas automáticas al instante.")
    
    st.info("⚠️ **Aviso legal:** Este chat ofrece orientación general de bienestar y salud preventiva, pero no sustituye el diagnóstico ni la consulta de un médico especialista.")

    # Inicializar el historial de conversación
    if "health_messages" not in st.session_state:
        st.session_state.health_messages = [
            {"role": "assistant", "content": "¡Hola! Soy tu asistente virtual de bienestar. ¿Qué consulta o consejo de salud te gustaría explorar hoy?"}
        ]

    # Mostrar el historial de mensajes
    for message in st.session_state.health_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto del usuario
    if user_input := st.chat_input("Escribe tu pregunta de salud aquí..."):
        st.session_state.health_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generar respuesta automática inteligente basada en el contenido
        query = user_input.lower()
        if any(w in query for w in ["agua", "hidratación", "beber", "tos"]):
            reply = "💧 **Consejo de hidratación:** Se aconseja consumir entre 2 y 2.5 litros de agua al día para mantener un buen rendimiento físico y mental. ¡Lleva siempre agua contigo!"
        elif any(w in query for w in ["sueño", "dormir", "cansancio", "insomnio"]):
            reply = "😴 **Consejo de descanso:** Un adulto saludable requiere de 7 a 8 horas de sueño continuo. Evita usar dispositivos electrónicos justo antes de dormir para mejorar la melatonina."
        elif any(w in query for w in ["estrés", "ansiedad", "relajar", "calmar"]):
            reply = "🧘 **Consejo antiestrés:** Prueba la respiración diafragmática: inhala en 4 segundos, mantén 4 segundos y exhala en 4 segundos. Te ayudará a disminuir la frecuencia cardíaca de inmediato."
        elif any(w in query for w in ["comer", "dieta", "nutrición", "alimento", "saludable"]):
            reply = "🥗 **Consejo nutricional:** Enfócate en alimentos reales y ricos en fibra (verduras, frutas, granos enteros). Reduce el consumo de azúcares y grasas saturadas."
        elif any(w in query for w in ["ejercicio", "deporte", "caminar", "actividad"]):
            reply = "🏃 **Consejo de actividad física:** Intenta realizar al menos 30 minutos diarios de caminata rápida o actividad aeróbica para cuidar tu salud cardiovascular."
        else:
            reply = f"Comprendo tu consulta sobre *'{user_input}'*. Para mantener una buena salud general, te sugiero priorizar una dieta equilibrada, mantenerte hidratado, dormir bien y, ante cualquier síntoma persistente, visitar a un médico profesional."

        with st.chat_message("assistant"):
            st.markdown(reply)
        
        st.session_state.health_messages.append({"role": "assistant", "content": reply})
