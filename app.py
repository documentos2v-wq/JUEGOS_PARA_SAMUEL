import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Juego de la Culebrita - Streamlit",
    page_icon="🐍",
    layout="centered"
)

st.title("🐍 Culebrita Retro en Streamlit")
st.write("Usa las **flechas del teclado** dentro del recuadro para mover la serpiente.")

# Código HTML y JavaScript del juego encapsulado
game_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            background-color: #0e1117;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 10px;
        }
        #score {
            font-size: 20px;
            margin-bottom: 10px;
            font-weight: bold;
        }
        canvas {
            border: 3px solid #4CAF50;
            background-color: #111;
        }
    </style>
</head>
<body>
    <div id="score">Puntuación: 0</div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        const tileSize = 20;
        const tileCount = canvas.width / tileSize;

        let snake = [{ x: 10, y: 10 }];
        let food = { x: 5, y: 5 };
        let dx = 0;
        let dy = 0;
        let score = 0;
        let gameInterval;
        let changingDirection = false;

        document.addEventListener("keydown", changeDirection);
        startGame();

        function startGame() {
            resetGame();
            gameInterval = setInterval(main, 100);
        }

        function main() {
            if (hasGameEnded()) {
                alert("¡Juego terminado! Puntuación final: " + score);
                resetGame();
                return;
            }
            changingDirection = false;
            clearCanvas();
            drawFood();
            moveSnake();
            drawSnake();
        }

        function clearCanvas() {
            ctx.fillStyle = "#111";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
        }

        function drawSnake() {
            snake.forEach((part, index) => {
                ctx.fillStyle = index === 0 ? "#4CAF50" : "#81C784";
                ctx.fillRect(part.x * tileSize, part.y * tileSize, tileSize - 2, tileSize - 2);
            });
        }

        function moveSnake() {
            const head = { x: snake[0].x + dx, y: snake[0].y + dy };
            snake.unshift(head);

            if (head.x === food.x && head.y === food.y) {
                score += 10;
                document.getElementById("score").innerText = "Puntuación: " + score;
                generateFood();
            } else {
                snake.pop();
            }
        }

        function generateFood() {
            food.x = Math.floor(Math.random() * tileCount);
            food.y = Math.floor(Math.random() * tileCount);
            snake.forEach(part => {
                if (part.x === food.x && part.y === food.y) {
                    generateFood();
                }
            });
        }

        function drawFood() {
            ctx.fillStyle = "#FF5252";
            ctx.fillRect(food.x * tileSize, food.y * tileSize, tileSize - 2, tileSize - 2);
        }

        function changeDirection(event) {
            const keyPressed = event.keyCode;
            const LEFT = 37, UP = 38, RIGHT = 39, DOWN = 40;

            if (changingDirection) return;

            if (keyPressed === LEFT && dx === 0) { dx = -1; dy = 0; changingDirection = true; }
            if (keyPressed === UP && dy === 0) { dx = 0; dy = -1; changingDirection = true; }
            if (keyPressed === RIGHT && dx === 0) { dx = 1; dy = 0; changingDirection = true; }
            if (keyPressed === DOWN && dy === 0) { dx = 0; dy = 1; changingDirection = true; }
        }

        function hasGameEnded() {
            for (let i = 4; i < snake.length; i++) {
                if (snake[i].x === snake[0].x && snake[i].y === snake[0].y) return true;
            }
            return snake[0].x < 0 || snake[0].x >= tileCount || snake[0].y < 0 || snake[0].y >= tileCount;
        }

        function resetGame() {
            snake = [{ x: 10, y: 10 }];
            dx = 1;
            dy = 0;
            score = 0;
            document.getElementById("score").innerText = "Puntuación: " + score;
            generateFood();
        }
    </script>
</body>
</html>
"""

# Renderizar el juego en Streamlit
components.html(game_code, height=480)
