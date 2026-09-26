import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Adivina la Palabra 2026 - Streamlit",
    page_icon="🧩",
    layout="centered"
)

st.title("🧩 Adivina la Palabra Oculta")
st.write("Pon a prueba tu agilidad mental. Lee la pista, selecciona las letras correctas antes de quedarte sin vidas y descubre la palabra secreta.")

# Código HTML, CSS y JS del juego de adivinar palabras
game_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
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
        .game-card {
            background: rgba(30, 41, 59, 0.85);
            border: 2px solid #38bdf8;
            padding: 20px;
            border-radius: 14px;
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.2);
            width: 440px;
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
        .clase-pista {
            background: #1e293b;
            padding: 10px;
            border-radius: 8px;
            font-size: 15px;
            margin-bottom: 20px;
            color: #cbd5e1;
            border-left: 4px solid #38bdf8;
        }
        .word-display {
            font-size: 32px;
            letter-spacing: 12px;
            font-weight: bold;
            margin-bottom: 25px;
            color: #f43f5e;
            text-shadow: 0 0 10px rgba(244, 63, 94, 0.4);
        }
        .keyboard {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 6px;
            margin-bottom: 15px;
        }
        .key-btn {
            background: #334155;
            color: #fff;
            border: none;
            padding: 10px 0;
            font-size: 14px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            transition: 0.15s;
        }
        .key-btn:hover:not(:disabled) {
            background: #38bdf8;
            color: #0f172a;
        }
        .key-btn:disabled {
            background: #1e293b;
            color: #64748b;
            cursor: not-allowed;
        }
        #action-btn {
            background: linear-gradient(45deg, #38bdf8, #2563eb);
            color: #fff;
            border: none;
            padding: 10px 22px;
            font-weight: bold;
            font-size: 14px;
            border-radius: 20px;
            cursor: pointer;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.5);
            margin-top: 10px;
        }
        #action-btn:hover {
            transform: scale(1.05);
        }
    </style>
</head>
<body>

    <div class="game-card">
        <div class="stats">
            <div id="score">Puntuación: 0</div>
            <div id="lives">Vidas: ❤️❤️❤️❤️❤️</div>
        </div>

        <div class="clase-pista" id="clasePista">Pista: Cargando...</div>
        
        <div class="word-display" id="wordDisplay">_ _ _ _</div>

        <div class="keyboard" id="keyboard"></div>

        <button id="action-btn" onclick="nextWord()" style="display:none;">SIGUIENTE PALABRA</button>
    </div>

    <script>
        const wordsList = [
            { word: "PYTHON", hint: "Lenguaje de programación muy popular enfocado en IA y desarrollo." },
            { word: "GITHUB", hint: "Plataforma de desarrollo y control de versiones en la nube." },
            { word: "PROGRAMA", hint: "Conjunto de instrucciones que sigue una computadora para ejecutar tareas." },
            { word: "STREAMLIT", hint: "Framework de Python para crear aplicaciones web de datos rápidamente." },
            { word: "TECLADO", hint: "Periférico principal de entrada para escribir texto en un ordenador." },
            { word: "INTERNET", hint: "Red global descentralizada de computadoras conectadas entre sí." },
            { word: "ALGORITMO", hint: "Secuencia lógica de pasos finitos para resolver un problema." },
            { word: "SERVIDOR", hint: "Computadora de alta potencia que procesa y aloja sitios web." },
            { word: "SOFTWARE", hint: "Conjunto de programas, instrucciones y reglas informáticas." },
            { word: "PANTALLA", hint: "Dispositivo donde se muestra la información visual de la computadora." }
        ];

        let currentItem = {};
        let guessedLetters = [];
        let lives = 5;
        let score = 0;
        let gameActive = true;

        const alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ";

        function initGame() {
            // Seleccionar palabra aleatoria
            currentItem = wordsList[Math.floor(Math.random() * wordsList.length)];
            guessedLetters = [];
            lives = 5;
            gameActive = true;
            document.getElementById("action-btn").style.display = "none";
            
            document.getElementById("clasePista").innerText = "Pista: " + currentItem.hint;
            updateDisplay();
            buildKeyboard();
        }

        function buildKeyboard() {
            const kbContainer = document.getElementById("keyboard");
            kbContainer.innerHTML = "";
            for (let char of alphabet) {
                let btn = document.createElement("button");
                btn.classList.add("key-btn");
                btn.innerText = char;
                btn.id = "key-" + char;
                btn.onclick = () => handleGuess(char);
                kbContainer.appendChild(btn);
            }
        }

        function handleGuess(letter) {
            if (!gameActive) return;
            guessedLetters.push(letter);
            
            let btn = document.getElementById("key-" + letter);
            if (btn) btn.disabled = true;

            if (currentItem.word.includes(letter)) {
                // Acierto
                if (btn) btn.style.background = "#22c55e";
                updateDisplay();

                // Verificar si ganó
                let won = true;
                for (let char of currentItem.word) {
                    if (!guessedLetters.includes(char)) {
                        won = false;
                        break;
                    }
                }

                if (won) {
                    score += 50;
                    document.getElementById("score").innerText = "Puntuación: " + score;
                    document.getElementById("clasePista").innerText = "🎉 ¡EXCELENTE! ¡Has adivinado la palabra!";
                    gameActive = false;
                    document.getElementById("action-btn").style.display = "inline-block";
                }
            } else {
                // Fallo
                if (btn) btn.style.background = "#ef4444";
                lives--;
                updateDisplay();

                if (lives <= 0) {
                    document.getElementById("clasePista").innerText = "❌ ¡Game Over! La palabra era: " + currentItem.word;
                    // Revelar palabra completa
                    let displayStr = "";
                    for (let char of currentItem.word) {
                        displayStr += char + " ";
                    }
                    document.getElementById("wordDisplay").innerText = displayStr.trim();
                    gameActive = false;
                    document.getElementById("action-btn").style.display = "inline-block";
                    document.getElementById("action-btn").innerText = "JUGAR OTRA VEZ";
                }
            }
        }

        function updateDisplay() {
            let displayStr = "";
            for (let char of currentItem.word) {
                if (guessedLetters.includes(char)) {
                    displayStr += char + " ";
                } else {
                    displayStr += "_ ";
                }
            }
            document.getElementById("wordDisplay").innerText = displayStr.trim();

            let hearts = "";
            for (let i = 0; i < lives; i++) hearts += "❤️";
            document.getElementById("lives").innerText = "Vidas: " + hearts;
        }

        function nextWord() {
            if(lives <= 0) score = 0; // Reiniciar score si perdió
            initGame();
        }

        // Arrancar al cargar
        initGame();
    </script>
</body>
</html>
"""

# Renderizar la aplicación en Streamlit
components.html(game_code, height=500)
