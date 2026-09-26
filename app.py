import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Dino T-Rex Mobile - Streamlit",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Dinosaurio de Google: Versión Móvil")
st.write("¡Optimizado para celulares! **Toca la pantalla o presiona la pantalla** para hacer saltar al dinosaurio y esquivar los cactus.")

# Código HTML, CSS y JS optimizado para pantallas táctiles y móviles
game_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
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
            padding: 5px;
            touch-action: manipulation;
        }
        .container {
            background: rgba(30, 41, 59, 0.95);
            border: 2px solid #38bdf8;
            padding: 10px;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
            text-align: center;
            width: 100%;
            max-width: 400px;
        }
        #score-panel {
            font-size: 15px;
            font-weight: bold;
            margin-bottom: 8px;
            color: #38bdf8;
            letter-spacing: 1px;
        }
        canvas {
            background-color: #f8fafc;
            border-radius: 6px;
            display: block;
            margin: 0 auto;
            width: 100%;
            max-width: 380px;
            height: 160px;
            outline: none;
            box-shadow: inset 0 0 8px rgba(0,0,0,0.08);
            cursor: pointer;
        }
        .instructions {
            margin-top: 8px;
            font-size: 12px;
            color: #94a3b8;
        }
        #jump-btn {
            background: linear-gradient(45deg, #38bdf8, #2563eb);
            color: white;
            border: none;
            width: 100%;
            padding: 14px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            margin-top: 10px;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
        }
        #jump-btn:active {
            transform: scale(0.98);
        }
    </style>
</head>
<body>

    <div class="container">
        <div id="score-panel">HI: 00000 &nbsp;&nbsp; 00000</div>
        <canvas id="gameCanvas" width="400" height="170" tabindex="1"></canvas>
        <button id="jump-btn" onclick="triggerJump()">¡SALTAR! 🦖</button>
        <div class="instructions">Toca la pantalla o usa el botón para saltar.</div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let score = 0;
        let highscore = 0;
        let gameSpeed = 4.5;
        let isGameOver = false;
        let gameStarted = false;

        let dino = {
            x: 35,
            y: 95,
            width: 36,
            height: 40,
            vy: 0,
            gravity: 0.55,
            jumpPower: -9.5,
            isJumping: false
        };

        let obstacles = [];
        let obstacleTimer = 0;

        function triggerJump() {
            if (!gameStarted || isGameOver) {
                resetGame();
            } else if (!dino.isJumping) {
                dino.vy = dino.jumpPower;
                dino.isJumping = true;
            }
        }

        // Eventos táctiles y de teclado
        window.addEventListener("keydown", (e) => {
            if (["Space", "ArrowUp", "KeyW"].includes(e.code)) {
                e.preventDefault();
                triggerJump();
            }
        });

        canvas.addEventListener("touchstart", (e) => {
            e.preventDefault();
            triggerJump();
        }, { passive: false });

        canvas.addEventListener("click", () => {
            triggerJump();
        });

        function resetGame() {
            score = 0;
            gameSpeed = 4.5;
            obstacles = [];
            obstacleTimer = 0;
            dino.y = 95;
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

            if (dino.y > 95) {
                dino.y = 95;
                dino.vy = 0;
                dino.isJumping = false;
            }

            obstacleTimer++;
            if (obstacleTimer > Math.random() * 55 + 75) {
                obstacles.push({
                    x: canvas.width,
                    y: 100,
                    width: 20,
                    height: 35
                });
                obstacleTimer = 0;
            }

            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].x -= gameSpeed;

                if (
                    dino.x + 5 < obstacles[i].x + obstacles[i].width - 3 &&
                    dino.x + dino.width - 5 > obstacles[i].x + 3 &&
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

            gameSpeed = 4.5 + Math.floor(score / 100);
        }

        function draw() {
            ctx.fillStyle = "#f8fafc";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Suelo
            ctx.strokeStyle = "#475569";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(0, 135);
            ctx.lineTo(canvas.width, 135);
            ctx.stroke();

            // Dinosaurio HD
            ctx.save();
            let dx = dino.x;
            let dy = dino.y;
            ctx.fillStyle = "#334155";
            ctx.fillRect(dx + 10, dy + 12, 20, 18); // Cuerpo
            ctx.fillRect(dx + 20, dy + 2, 14, 13);  // Cabeza
            ctx.fillRect(dx + 29, dy + 6, 6, 6);    // Hocico
            ctx.fillStyle = "#f8fafc";
            ctx.fillRect(dx + 28, dy + 4, 2, 2);    // Ojo
            ctx.fillStyle = "#334155";
            ctx.fillRect(dx, dy + 15, 12, 6);       // Cola
            ctx.fillRect(dx + 12, dy + 30, 5, 8);   // Pata 1
            ctx.fillRect(dx + 21, dy + 30, 5, 8);   // Pata 2
            ctx.restore();

            // Cactus
            obstacles.forEach(obs => {
                ctx.fillStyle = "#15803d";
                ctx.fillRect(obs.x + 6, obs.y, 6, obs.height);
                ctx.fillRect(obs.x, obs.y + 10, 6, 5);
                ctx.fillRect(obs.x + 12, obs.y + 16, 6, 5);
            });

            if (!gameStarted) {
                ctx.fillStyle = "#334155";
                ctx.font = "14px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText("¡Toca la pantalla para Iniciar!", canvas.width / 2, canvas.height / 2);
            } else if (isGameOver) {
                ctx.fillStyle = "#ef4444";
                ctx.font = "bold 18px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 8);
                ctx.fillStyle = "#334155";
                ctx.font = "12px sans-serif";
                ctx.fillText("Toca el botón para Reiniciar", canvas.width / 2, canvas.height / 2 + 14);
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

# Renderizar en Streamlit adaptado a móvil
components.html(game_code, height=360)
