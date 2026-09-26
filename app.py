import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Dino T-Rex HD - Streamlit",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Dinosaurio de Google: Edición Gráfica HD")
st.write("Disfruta del clásico juego con un diseño gráfico vectorial detallado de alta definición. Presiona la **Barra Espaciadora** o **Flecha Arriba** para saltar.")

# Código HTML, CSS y JS con diseño vectorial HD impecable
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
            padding: 10px;
        }
        .container {
            background: rgba(30, 41, 59, 0.9);
            border: 2px solid #38bdf8;
            padding: 15px;
            border-radius: 14px;
            box-shadow: 0 0 25px rgba(56, 189, 248, 0.3);
            text-align: center;
        }
        #score-panel {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #38bdf8;
            letter-spacing: 1px;
        }
        canvas {
            background-color: #f8fafc;
            border-radius: 8px;
            display: block;
            margin: 0 auto;
            outline: none;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.08);
        }
        .instructions {
            margin-top: 10px;
            font-size: 13px;
            color: #94a3b8;
        }
    </style>
</head>
<body>

    <div class="container">
        <div id="score-panel">HI: 00000 &nbsp;&nbsp;&nbsp; 00000</div>
        <canvas id="gameCanvas" width="600" height="220" tabindex="1"></canvas>
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

        // Dinosaurio estilizado HD
        let dino = {
            x: 50,
            y: 130,
            width: 44,
            height: 48,
            vy: 0,
            gravity: 0.6,
            jumpPower: -10.5,
            isJumping: false
        };

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

            dino.vy += dino.gravity;
            dino.y += dino.vy;

            if (dino.y > 130) {
                dino.y = 130;
                dino.vy = 0;
                dino.isJumping = false;
            }

            obstacleTimer++;
            if (obstacleTimer > Math.random() * 55 + 75) {
                obstacles.push({
                    x: canvas.width,
                    y: 135,
                    width: 24,
                    height: 43
                });
                obstacleTimer = 0;
            }

            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].x -= gameSpeed;

                // Colisión precisa
                if (
                    dino.x + 6 < obstacles[i].x + obstacles[i].width - 4 &&
                    dino.x + dino.width - 6 > obstacles[i].x + 4 &&
                    dino.y + 4 < obstacles[i].y + obstacles[i].height &&
                    dino.y + dino.height > obstacles[i].y
                ) {
                    isGameOver = true;
                    if (score > highscore) highscore = Math.floor(score);
                }

                if (obstacles[i].x + obstacles[i].width < 0) {
                    obstacles.splice(i, 1);
                    score += 10;
                }
            }

            gameSpeed = 5 + Math.floor(score / 100);
        }

        function draw() {
            ctx.fillStyle = "#f8fafc";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Suelo del desierto
            ctx.strokeStyle = "#475569";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(0, 178);
            ctx.lineTo(canvas.width, 178);
            ctx.stroke();

            // --- DIBUJAR DINOSAURIO HD DETALLADO ---
            ctx.save();
            let dx = dino.x;
            let dy = dino.y;

            ctx.fillStyle = "#334155"; // Color principal del T-Rex
            
            // Cuerpo principal
            ctx.fillRect(dx + 12, dy + 15, 24, 22);
            // Cabeza
            ctx.fillRect(dx + 24, dy + 2, 18, 16);
            // Hocico y mandíbula
            ctx.fillRect(dx + 35, dy + 8, 8, 8);
            // Ojo brillante
            ctx.fillStyle = "#f8fafc";
            ctx.fillRect(dx + 34, dy + 5, 3, 3);
            // Cola inclinada
            ctx.fillStyle = "#334155";
            ctx.fillRect(dx, dy + 18, 14, 8);
            ctx.fillRect(dx - 6, dy + 22, 8, 6);
            // Patas dinámicas
            ctx.fillRect(dx + 14, dy + 37, 6, 11);
            ctx.fillRect(dx + 26, dy + 37, 6, 11);

            ctx.restore();

            // --- DIBUJAR CACTUS DETALLADOS HD ---
            obstacles.forEach(obs => {
                ctx.fillStyle = "#15803d";
                // Tronco central
                ctx.fillRect(obs.x + 8, obs.y, 8, obs.height);
                // Brazo izquierdo
                ctx.fillRect(obs.x, obs.y + 12, 8, 6);
                ctx.fillRect(obs.x, obs.y + 6, 4, 10);
                // Brazo derecho
                ctx.fillRect(obs.x + 16, obs.y + 20, 8, 6);
                ctx.fillRect(obs.x + 20, obs.y + 14, 4, 12);
            });

            if (!gameStarted) {
                ctx.fillStyle = "#334155";
                ctx.font = "16px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText("Presiona Espacio o Clic para Iniciar", canvas.width / 2, canvas.height / 2);
            } else if (isGameOver) {
                ctx.fillStyle = "#ef4444";
                ctx.font = "bold 22px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText("G A M E   O V E R", canvas.width / 2, canvas.height / 2 - 10);
                ctx.fillStyle = "#334155";
                ctx.font = "14px sans-serif";
                ctx.fillText("Presiona Espacio para Reiniciar", canvas.width / 2, canvas.height / 2 + 18);
            }

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

        draw();
    </script>
</body>
</html>
"""

# Renderizar en Streamlit
components.html(game_code, height=320)
