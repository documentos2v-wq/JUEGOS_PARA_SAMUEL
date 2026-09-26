import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Dino T-Rex Game 2026 - Streamlit",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Dinosaurio de Google: Edición Nocturna")
st.write("Presiona la **Barra Espaciadora** o la **Flecha Arriba** para saltar sobre los cactus y descansar un rato antes de dormir.")

# Código HTML, CSS y JS del juego del T-Rex
game_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 10px;
        }
        .container {
            background: #1e1e1e;
            border: 2px solid #555;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
            text-align: center;
        }
        #score-panel {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #aaa;
            letter-spacing: 1px;
        }
        canvas {
            background-color: #f7f7f7;
            border-radius: 6px;
            display: block;
            margin: 0 auto;
            outline: none;
        }
        .instructions {
            margin-top: 10px;
            font-size: 13px;
            color: #888;
        }
    </style>
</head>
<body>

    <div class="container">
        <div id="score-panel">HI: 00000 &nbsp;&nbsp;&nbsp; 00000</div>
        <canvas id="gameCanvas" width="600" height="200" tabindex="1"></canvas>
        <div class="instructions">Usa la <strong>Barra Espaciadora</strong> o <strong>Flecha Arriba</strong> para saltar.</div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        canvas.focus();

        let score = 0;
        let highscore = 0;
        let gameSpeed = 5;
        let isGameOver = false;
        let gameStarted = false;

        // Dinosaurio
        let dino = {
            x: 50,
            y: 130,
            width: 30,
            height: 40,
            vy: 0,
            gravity: 0.6,
            jumpPower: -10,
            isJumping: false
        };

        // Obstáculos (Cactus)
        let obstacles = [];
        let obstacleTimer = 0;

        window.addEventListener("keydown", (e) => {
            if (["Space", "ArrowUp", "KeyW"].includes(e.code)) {
                e.preventDefault();
                if (!gameStarted || isGameOver) {
                    resetGame();
                } else if (!dino.isJumping) {
                    dino.vy = dino.jumpPower;
                    dino.isJumping = true;
                }
            }
        });

        // Click en canvas para saltar en móviles/tablets
        canvas.addEventListener("click", () => {
            if (!gameStarted || isGameOver) {
                resetGame();
            } else if (!dino.isJumping) {
                dino.vy = dino.jumpPower;
                dino.isJumping = true;
            }
        });

        function resetGame() {
            score = 0;
            gameSpeed = 5;
            obstacles = [];
            obstacleTimer = 0;
            dino.y = 130;
            dino.vy = 0;
            dino.isJumping = false;
            isGameOver = false;
            gameStarted = true;
            loop();
        }

        function update() {
            if (isGameOver || !gameStarted) return;

            // Movimiento del Dinosaurio (Gravedad)
            dino.vy += dino.gravity;
            dino.y += dino.vy;

            // Suelo
            if (dino.y > 130) {
                dino.y = 130;
                dino.vy = 0;
                dino.isJumping = false;
            }

            // Generar obstáculos
            obstacleTimer++;
            if (obstacleTimer > Math.random() * 50 + 70) {
                let obsWidth = 15 + Math.random() * 15;
                let obsHeight = 25 + Math.random() * 20;
                obstacles.push({
                    x: canvas.width,
                    y: 170 - obsHeight,
                    width: obsWidth,
                    height: obsHeight
                });
                obstacleTimer = 0;
            }

            // Mover obstáculos y detectar colisiones
            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].x -= gameSpeed;

                // Colisión AABB
                if (
                    dino.x < obstacles[i].x + obstacles[i].width &&
                    dino.x + dino.width > obstacles[i].x &&
                    dino.y < obstacles[i].y + obstacles[i].height &&
                    dino.y + dino.height > obstacles[i].y
                ) {
                    isGameOver = true;
                    if (score > highscore) highscore = Math.floor(score);
                }

                // Eliminar fuera de pantalla
                if (obstacles[i].x + obstacles[i].width < 0) {
                    obstacles.splice(i, 1);
                    score += 10;
                }
            }

            // Incrementar dificultad progresiva
            gameSpeed = 5 + Math.floor(score / 100);
        }

        function draw() {
            // Limpiar lienzo
            ctx.fillStyle = "#f7f7f7";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Suelo
            ctx.strokeStyle = "#535353";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(0, 170);
            ctx.lineTo(canvas.width, 170);
            ctx.stroke();

            // Dibujar Dinosaurio (Clásico T-Rex pixelado minimalista)
            ctx.fillStyle = "#535353";
            ctx.fillRect(dino.x, dino.y, dino.width, dino.height);
            // Ojo del dino
            ctx.fillStyle = "#f7f7f7";
            ctx.fillRect(dino.x + 20, dino.y + 6, 4, 4);

            // Dibujar Cactus
            ctx.fillStyle = "#2e7d32";
            obstacles.forEach(obs => {
                ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
            });

            // Pantalla de inicio o fin
            if (!gameStarted) {
                ctx.fillStyle = "#535353";
                ctx.font = "16px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText("Presiona Espacio o Clic para Jugar", canvas.width / 2, canvas.height / 2);
            } else if (isGameOver) {
                ctx.fillStyle = "#535353";
                ctx.font = "20px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText("G A M E   O V E R", canvas.width / 2, canvas.height / 2 - 10);
                ctx.font = "12px sans-serif";
                ctx.fillText("Presiona Espacio para Reiniciar", canvas.width / 2, canvas.height / 2 + 15);
            }

            // Actualizar Marcador
            let scStr = Math.floor(score).toString().padStart(5, '0');
            let hiStr = highscore.toString().padStart(5, '0');
            document.getElementById("score-panel").innerText = `HI: ${hiStr}    ${scStr}`;
        }

        function loop() {
            update();
            draw();
            if (!isGameOver) {
                requestAnimationFrame(loop);
            }
        }

        // Renderizado inicial estático
        draw();
    </script>
</body>
</html>
"""

# Renderizar en Streamlit
components.html(game_code, height=300)
