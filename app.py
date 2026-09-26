import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Reto Mental Capcioso - Streamlit",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Reto Mental: Preguntas Capciosas y Adivinanzas")
st.write("Resuelve acertijos ingeniosos. Cada acierto te genera un desafío totalmente nuevo sin repetir preguntas anteriores.")

# Código HTML, CSS y JS con banco de preguntas único y dinámico
game_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            background-color: #0f172a;
            color: #f8fafc;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 15px;
        }
        .card {
            background: rgba(30, 41, 59, 0.95);
            border: 2px solid #38bdf8;
            padding: 20px;
            border-radius: 14px;
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.3);
            width: 100%;
            max-width: 450px;
            text-align: center;
        }
        .stats {
            display: flex;
            justify-content: space-between;
            font-size: 15px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #38bdf8;
        }
        .question-box {
            background: #1e293b;
            padding: 15px;
            border-radius: 10px;
            font-size: 16px;
            margin-bottom: 20px;
            color: #e2e8f0;
            border-left: 4px solid #f59e0b;
            line-height: 1.4;
        }
        .options-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 15px;
        }
        .option-btn {
            background: #334155;
            color: white;
            border: none;
            padding: 12px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.2s;
            text-align: left;
            padding-left: 15px;
        }
        .option-btn:hover:not(:disabled) {
            background: #38bdf8;
            color: #0f172a;
        }
        .option-btn:disabled {
            cursor: not-allowed;
            opacity: 0.7;
        }
        #feedback {
            font-size: 15px;
            font-weight: bold;
            margin-top: 10px;
            min-height: 24px;
        }
        #next-btn {
            background: linear-gradient(45deg, #22c55e, #16a34a);
            color: white;
            border: none;
            padding: 10px 24px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 20px;
            cursor: pointer;
            margin-top: 15px;
            box-shadow: 0 0 10px rgba(34, 197, 94, 0.4);
            display: none;
        }
        #next-btn:hover {
            transform: scale(1.05);
        }
    </style>
</head>
<body>

    <div class="card">
        <div class="stats">
            <div id="score">Aciertos: 0</div>
            <div id="remaining">Restantes: 0</div>
        </div>

        <div class="question-box" id="questionText">Cargando desafío mental...</div>

        <div class="options-container" id="optionsContainer"></div>

        <div id="feedback"></div>

        <button id="next-btn" onclick="loadNextQuestion()">Siguiente Reto 🚀</button>
    </div>

    <script>
        // Banco extenso de preguntas capciosas y adivinanzas para evitar repeticiones
        const masterQuestions = [
            {
                q: "¿Qué sube y baja pero siempre se queda en el mismo lugar?",
                options: ["La temperatura", "Las escaleras", "Una montaña rusa", "El ascensor"],
                answer: 1
            },
            {
                q: "Iba con 7 perros rumbo a Lima. Cada perro llevaba 7 sacos, cada saco 7 gatos, y cada gato 7 gatitos. ¿Cuántos animales iban rumbo a Lima?",
                options: ["2,401 animales", "Ninguno, yo iba solo", "400 animales", "Depende del peso"],
                answer: 1
            },
            {
                q: "¿De qué color son las mangas del chaleco de un abuelo?",
                options: ["Blancas", "Negras", "No tiene, es un chaleco", "Depende del traje"],
                answer: 2
            },
            {
                q: "Si un tren eléctrico viaja de norte a sur a gran velocidad, ¿hacia dónde va el humo?",
                options: ["Hacia el norte", "Hacia el sur", "Hacia arriba", "Los trenes eléctricos no botan humo"],
                answer: 3
            },
            {
                q: "¿Qué cosa es que, cuanto más le quitas, más grande se vuelve?",
                options: ["Un hoyo o zanja", "Una piedra", "Una esponja", "El dinero"],
                answer: 0
            },
            {
                q: "Tengo dos monedas que suman 30 céntimos exactos y una de ellas no es de 10 céntimos. ¿Cuáles son las monedas?",
                options: ["Una de 20 y una de 10", "Tres de 10 céntimos", "Una de 25 y una de 5", "Dos de 15"],
                answer: 0
            },
            {
                q: "¿Qué pasa si tiras un sombrero blanco al Mar Rojo?",
                options: ["Se hunde", "Se moja", "Se pierde", "Flota sin romperse"],
                answer: 1
            },
            {
                q: "Cinco hermanos están en una cabaña jugando ajedrez. Uno lee, otro cocina, otro barre, otro juega cartas. ¿Qué hace el quinto hermano?",
                options: ["Duerme", "Juega ajedrez", "Lava los platos", "Mira la ventana"],
                answer: 1
            },
            {
                q: "¿Cuántos animales metió Moisés en el arca de su viaje?",
                options: ["Una pareja de cada especie", "Muchos animales", "Cien animales", "Ninguno, fue Noé, no Moisés"],
                answer: 3
            },
            {
                q: "Hijo de mi padre, pero no mi hermano. ¿Quién es?",
                options: ["Mi tío", "Yo mismo", "Mi hijo", "Mi sobrino"],
                answer: 1
            },
            {
                q: "¿Qué tiene cabeza y cuerpo, pero no tiene pies ni piernas?",
                options: ["Un alfiler o clavo", "Una serpiente", "Una moneda", "Una cama"],
                answer: 0
            },
            {
                q: "Si hay 3 manzanas y te llevas 2, ¿cuántas manzanas tienes?",
                options: ["1 manzana", "3 manzanas", "2 manzanas", "Ninguna"],
                answer: 2
            }
        ];

        let availableQuestions = [];
        let currentQuestion = null;
        let score = 0;
        let answered = false;

        function initGame() {
            // Copiar todas las preguntas al array disponible
            availableQuestions = [...masterQuestions];
            score = 0;
            loadNextQuestion();
        }

        function loadNextQuestion() {
            if (availableQuestions.length === 0) {
                document.getElementById("questionText").innerText = "🏆 ¡Felicidades! Has respondido correctamente todas las preguntas sin repetir ninguna.";
                document.getElementById("optionsContainer").innerHTML = "";
                document.getElementById("feedback").innerText = "";
                document.getElementById("next-btn").innerText = "REINICIAR TODO";
                document.getElementById("next-btn").style.display = "inline-block";
                document.getElementById("next-btn").onclick = initGame;
                return;
            }

            answered = false;
            document.getElementById("feedback").innerText = "";
            document.getElementById("next-btn").style.display = "none";

            // Seleccionar pregunta aleatoria y retirarla de la lista para que nunca se repita
            let randomIndex = Math.floor(Math.random() * availableQuestions.length);
            currentQuestion = availableQuestions.splice(randomIndex, 1)[0];

            document.getElementById("questionText").innerText = currentQuestion.q;
            document.getElementById("score").innerText = "Aciertos: " + score;
            document.getElementById("remaining").innerText = "Restantes: " + (availableQuestions.length + 1);

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
                feedbackDiv.style.color = "#22c55e";
                feedbackDiv.innerText = "🎉 ¡Correcto! Ingeniosa respuesta.";
                score++;
                document.getElementById("score").innerText = "Aciertos: " + score;
            } else {
                selectedBtn.style.background = "#ef4444";
                buttons[currentQuestion.answer].style.background = "#22c55e";
                feedbackDiv.style.color = "#ef4444";
                feedbackDiv.innerText = "❌ ¡Caíste en la trampa! Esa no era.";
            }

            document.getElementById("next-btn").style.display = "inline-block";
        }

        // Iniciar juego al cargar
        initGame();
    </script>
</body>
</html>
"""

# Renderizar en Streamlit
components.html(game_code, height=525)
