import streamlit as st

# Configuración de la página para ocupar todo el ancho
st.set_page_config(
    page_title="Reto Mental Infinito con Pingüino",
    page_icon="🐧",
    layout="wide"
)

# Estilo para quitar márgenes y forzar pantalla negra total
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        z-index: 999999 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Código HTML y JS con el pingüino bailando y modo infinito
game_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            background-color: #000000;
            color: #f8fafc;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            width: 100vw;
            height: 100vh;
            padding: 20px 40px;
            overflow: hidden;
        }
        .stats {
            display: flex;
            justify-content: space-between;
            font-size: 22px;
            font-weight: bold;
            color: #38bdf8;
            border-bottom: 2px solid #1e293b;
            padding-bottom: 10px;
            width: 100%;
        }
        .question-container {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
        }
        /* Estilos del pingüino bailando */
        .penguin-container {
            font-size: 60px;
            text-align: center;
            margin-bottom: 10px;
            animation: dance 0.6s infinite alternate ease-in-out;
        }
        @keyframes dance {
            0% { transform: translateY(0) rotate(-10deg) scale(1); }
            100% { transform: translateY(-15px) rotate(10deg) scale(1.1); }
        }
        .question-box {
            background: #0f172a;
            padding: 25px;
            border-radius: 14px;
            font-size: 24px;
            color: #ffffff;
            border-left: 6px solid #f59e0b;
            line-height: 1.4;
            text-align: center;
            margin-bottom: 20px;
            width: 100%;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }
        .options-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            width: 100%;
        }
        .option-btn {
            background: #1e293b;
            color: white;
            border: 2px solid #334155;
            padding: 18px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 12px;
            cursor: pointer;
            transition: 0.2s;
            text-align: left;
        }
        .option-btn:hover:not(:disabled) {
            background: #38bdf8;
            color: #000000;
            border-color: #38bdf8;
        }
        .option-btn:disabled {
            cursor: not-allowed;
            opacity: 0.7;
        }
        .footer-area {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
            min-height: 50px;
            border-top: 2px solid #1e293b;
            padding-top: 10px;
        }
        #feedback {
            font-size: 22px;
            font-weight: bold;
        }
        #next-btn {
            background: linear-gradient(45deg, #22c55e, #16a34a);
            color: white;
            border: none;
            padding: 12px 30px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 30px;
            cursor: pointer;
            box-shadow: 0 0 15px rgba(34, 197, 94, 0.4);
            display: none;
        }
        #next-btn:hover {
            transform: scale(1.05);
        }
    </style>
</head>
<body>

    <div class="stats">
        <div id="score">Aciertos: 0</div>
        <div id="roundInfo">Modo Infinito 🐧</div>
    </div>

    <div class="question-container">
        <!-- Pingüino bailando para distraer -->
        <div class="penguin-container" id="dancingPenguin">🐧</div>
        
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
            { q: "Hijo de mi padre, pero no mi hermano. ¿Quién es?", options: ["Mi tío", "Yo mismo", "Mi hijo", "Mi sobrino"], answer: 1 },
            { q: "¿Qué tiene cabeza y cuerpo, pero no tiene pies ni piernas?", options: ["Un alfiler o clavo", "Una serpiente", "Una moneda", "Una cama"], answer: 0 },
            { q: "Si hay 3 manzanas y te llevas 2, ¿cuántas manzanas tienes?", options: ["1 manzana", "3 manzanas", "2 manzanas", "Ninguna"], answer: 2 },
            { q: "¿Qué se puede romper sin siquiera tocarlo?", options: ["Un vaso de vidrio", "Una promesa o un secreto", "Un papel", "Un espejo"], answer: 1 },
            { q: "¿De qué nacionalidad es un habitante que nace en la frontera entre Chile y Perú?", options: ["Chileno", "Peruano", "Depende de sus padres", "Ninguno, es ciudadano fronterizo"], answer: 2 },
            { q: "Entra a la iglesia con tres nombres y sale con uno solo. ¿Quién es?", options: ["Un sacerdote", "Una novia al casarse", "Un bautizado", "Un testigo"], answer: 1 }
        ];

        let availableQuestions = [];
        let currentQuestion = null;
        let score = 0;
        let answered = false;

        const penguins = ["🐧", "🕺🐧", "🪩🐧", "🧊🐧", "✨🐧"];

        function initGame() {
            score = 0;
            refillPool();
            loadNextQuestion();
        }

        function refillPool() {
            availableQuestions = [...masterQuestions];
        }

        function loadNextQuestion() {
            if (availableQuestions.length === 0) {
                refillPool();
            }

            answered = false;
            document.getElementById("feedback").innerText = "";
            document.getElementById("next-btn").style.display = "none";

            // Cambiar aleatoriamente el estilo del pingüino bailarín para más variedad
            let randomPenguin = penguins[Math.floor(Math.random() * penguins.length)];
            document.getElementById("dancingPenguin").innerText = randomPenguin;

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

            if (selectedIndex === currentQuestion.answer) {
                selectedBtn.style.background = "#22c55e";
                selectedBtn.style.borderColor = "#22c55e";
                selectedBtn.style.color = "#000000";
                feedbackDiv.style.color = "#22c55e";
                feedbackDiv.innerText = "🎉 ¡Correcto!";
                score++;
                document.getElementById("score").innerText = "Aciertos: " + score;
            } else {
                selectedBtn.style.background = "#ef4444";
                selectedBtn.style.borderColor = "#ef4444";
                buttons[currentQuestion.answer].style.background = "#22c55e";
                buttons[currentQuestion.answer].style.borderColor = "#22c55e";
                buttons[currentQuestion.answer].style.color = "#000000";
                feedbackDiv.style.color = "#ef4444";
                feedbackDiv.innerText = "❌ ¡Incorrecto!";
            }

            document.getElementById("next-btn").style.display = "block";
        }

        initGame();
    </script>
</body>
</html>
"""

st.components.v1.html(game_html, height=850, scrolling=False)
