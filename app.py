import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Dino T-Rex HD 3D - Streamlit",
    page_icon="🦖",
    layout="centered"
)

st.title("🦖 Dinosaurio de Google: Edición Gráfica HD")
st.write("Disfruta del clásico juego del dinosaurio con sprites e imágenes reales en alta definición. Presiona la **Barra Espaciadora** o **Flecha Arriba** para saltar.")

# Código HTML, CSS y JS con imágenes reales de T-Rex y obstáculos
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
            background-color: #ffffff;
            border-radius: 8px;
            display: block;
            margin: 0 auto;
            outline: none;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
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

        // Cargar imágenes reales en alta definición para el T-Rex y los obstáculos
        const dinoImg = new Image();
        dinoImg.src = "https://cdn.jsdelivr.net/gh/wayou/t-rex-runner/img/trex.png";

        const cactusImg = new Image();
        cactusImg.src = "https://cdn.jsdelivr.net/gh/wayou/t-rex-runner/img/obstacle-1.png";

        // Dinosaurio
        let dino = {
            x: 50,
            y: 135,
            width: 44,
            height: 47,
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
            dino.y = 135;
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

            if (dino.y > 135) {
                dino.y = 135;
                dino.vy = 0;
                dino.isJumping = false;
            }

            obstacleTimer++;
            if (obstacleTimer > Math.random() * 55 + 75) {
                obstacles.push({
                    x: canvas.width,
                    y: 138,
                    width: 30,
                    height: 44
                });
                obstacleTimer = 0;
            }

            for (let i = obstacles.length - 1; i >= 0; i--) {
                obstacles[i].x -= gameSpeed;

                // Colisión ajustada con margen real de las imágenes
                if (
                    dino.x + 8 < obstacles[i].x + obstacles[i].width - 6 &&
                    dino.x + dino.width - 8 > obstacles[i].x + 6 &&
                    dino.y + 5 < obstacles[i].y + obstacles[i].height &&
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
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Suelo detallado
            ctx.strokeStyle = "#535353";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(0, 182);
            ctx.lineTo(canvas.width, 182);
            ctx.stroke();

            // Dibujar Dinosaurio con imagen real HD
            if (dinoImg.complete) {
                ctx.drawImage(dinoImg, dino.x, dino.y, dino.width, dino.height);
            } else {
                ctx.fillStyle = "#535353";
                ctx.fillRect(dino.x, dino.y, dino.width, dino.height);
            }

            // Dibujar Obstáculos (Cactus reales HD)
            obstacles.forEach(obs => {
                if (cactusImg.complete) {
                    ctx.drawImage(cactusImg, obs.x, obs.y, obs.width, obs.height);
                } else {
                    ctx.fillStyle = "#2e7d32";
                    ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
                }
            });

            if (!gameStarted) {
                ctx.fillStyle = "#535353";
                ctx.font = "16px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText("Presiona Espacio o Clic para Iniciar", canvas.width / 2, canvas.height / 2);
            } else if (isGameOver) {
                ctx.fillStyle = "#535353";
                ctx.font = "20px bold sans-serif";
                ctx.textAlign = "center";
                ctx.fillText("G A M E   O V E R", canvas.width / 2, canvas.height / 2 - 10);
                ctx.font = "13px sans-serif";
                ctx.fillText("Presiona Espacio para Reiniciar", canvas.width / 2, canvas.height / 2 + 15);
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

        // Cargar imágenes antes de dibujar el estado estático inicial
        let loadedCount = 0;
        function checkLoaded() {
            loadedCount++;
            if (loadedCount === 2) draw();
        }
        dinoImg.onload = checkLoaded;
        cactusImg.onload = checkLoaded;
        
        // Fallback por si cargan instantáneamente
        setTimeout(draw, 100);
    </script>
</body>
</html>
"""

# Renderizar en Streamlit
components.html(game_code, height=320)
