import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Juego de Avioncitos - Streamlit",
    page_icon="✈️",
    layout="centered"
)

st.title("✈️ Batalla de Avioncitos Retro")
st.write("Haz clic dentro del cuadro, usa las **flechas izquierda y derecha** para mover tu avioncito y esquiva los meteoritos.")

# Código HTML y JavaScript del juego de avioncitos
airplane_game_code = """
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
            border: 3px solid #00bcd4;
            background-color: #050515;
            outline: none;
        }
    </style>
</head>
<body>
    <div id="score">Puntuación: 0</div>
    <canvas id="gameCanvas" width="400" height="500" tabindex="1"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        canvas.focus();

        let score = 0;
        let isGameOver = false;

        // Propiedades del avión del jugador
        let plane = {
            x: 180,
            y: 420,
            width: 40,
            height: 40,
            speed: 6
        };

        // Obstáculos (meteoritos)
        let obstacles = [];
        let obstacleTimer = 0;

        // Controles del teclado
        let keys = {};
        window.addEventListener("keydown", (e) => { keys[e.code] = true; });
        window.addEventListener("keyup", (e) => { keys[e.code] = false; });

        function startGame() {
            score = 0;
            obstacles = [];
            isGameOver = false;
            plane.x = 180;
            loop();
        }

        function update() {
            if (isGameOver) return;

            // Movimiento del avión
            if ((keys["ArrowLeft"] || keys["KeyA"]) && plane.x > 0) {
                plane.x -= plane.speed;
            }
            if ((keys["ArrowRight"] || keys["KeyD"]) && plane.x + plane.width < canvas.width) {
                plane.x += plane.speed;
            }

            // Generar obstáculos
            obstacleTimer++;
            if (obstacleTimer > 40) {
                let obsX = Math.random() * (canvas.width - 35);
                obstacles.push({ x: obsX, y: -40, width: 35, height: 35, speed: 4 + Math.random() * 3 });
                obstacleTimer = 0;
            }

            // Mover obstáculos y detectar colisiones
            for (let i = obstacles.length - 1; i >= 0; i--) {
                let obs = obstacles[i];
                obs.y += obs.speed;

                // Colisión con el avión
                if (
                    plane.x < obs.x + obs.width &&
                    plane.x + plane.width > obs.x &&
                    plane.y < obs.y + obs.height &&
                    plane.y + plane.height > obs.y
                ) {
                    isGameOver = true;
                }

                // Eliminar obstáculos fuera de la pantalla y sumar puntos
                if (obs.y > canvas.height) {
                    obstacles.splice(i, 1);
                    score += 10;
                }
            }
        }

        function draw() {
            // Limpiar pantalla
            ctx.fillStyle = "#050515";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Dibujar estrellas de fondo
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(50, 50, 2, 2);
            ctx.fillRect(150, 120, 2, 2);
            ctx.fillRect(300, 80, 2, 2);
            ctx.fillRect(250, 300, 2, 2);
            ctx.fillRect(80, 400, 2, 2);

            // Dibujar Avioncito (Diseño simple en canvas)
            ctx.fillStyle = "#00bcd4";
            // Cuerpo del avión
            ctx.fillRect(plane.x + 15, plane.y, 10, 40);
            // Alas
            ctx.fillStyle = "#ffeb3b";
            ctx.fillRect(plane.x, plane.y + 15, 40, 10);
            // Cabina
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(plane.x + 16, plane.y + 10, 8, 12);

            // Dibujar obstáculos (Meteoritos)
            ctx.fillStyle = "#ff5722";
            obstacles.forEach(obs => {
                ctx.beginPath();
                ctx.arc(obs.x + obs.width / 2, obs.y + obs.height / 2, obs.width / 2, 0, Math.PI * 2);
                ctx.fill();
            });

            // Actualizar marcador
            document.getElementById("score").innerText = "Puntuación: " + score;
        }

        function loop() {
            if (isGameOver) {
                alert("¡Game Over! Te estrellaste. Puntuación final: " + score);
                startGame();
                return;
            }
            update();
            draw();
            requestAnimationFrame(loop);
        }

        // Iniciar juego por primera vez
        startGame();
    </script>
</body>
</html>
"""

# Renderizar el juego en Streamlit con altura para el canvas vertical
components.html(airplane_game_code, height=580)
