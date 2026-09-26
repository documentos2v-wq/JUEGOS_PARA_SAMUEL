import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Drone Delivery 2026 - Streamlit",
    page_icon="🛸",
    layout="centered"
)

st.title("🛸 Drone Delivery 2026: Quantum Flight")
st.write("Pilota el dron de reparto autónomo de última generación. Esquiva los satélites en órbita y las tormentas de datos cibernéticos.")

# Código HTML, CSS y JS con temática 2026 y Botón de Inicio
game_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            background-color: #0b0f19;
            color: #00ffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 10px;
        }
        #ui-container {
            display: flex;
            justify-content: space-between;
            width: 400px;
            margin-bottom: 10px;
            align-items: center;
        }
        #score, #level {
            font-size: 16px;
            font-weight: bold;
            color: #00ffcc;
            text-shadow: 0 0 8px rgba(0,255,204,0.5);
        }
        #start-btn {
            background: linear-gradient(45deg, #00ffff, #0077ff);
            color: #0b0f19;
            border: none;
            padding: 8px 18px;
            font-weight: bold;
            font-size: 14px;
            border-radius: 20px;
            cursor: pointer;
            box-shadow: 0 0 12px rgba(0,255,255,0.6);
            transition: 0.2s;
        }
        #start-btn:hover {
            transform: scale(1.05);
            background: linear-gradient(45deg, #ffffff, #00ffff);
        }
        canvas {
            border: 2px solid #00ffff;
            background: radial-gradient(circle at center, #111e38 0%, #050811 100%);
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
            border-radius: 8px;
            outline: none;
        }
    </style>
</head>
<body>
    <div id="ui-container">
        <div id="score">Puntuación: 0</div>
        <button id="start-btn" onclick="initGame()">INICIAR VUELO</button>
        <div id="level">Nivel: 1</div>
    </div>
    
    <canvas id="gameCanvas" width="400" height="500" tabindex="1"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let score = 0;
        let level = 1;
        let isPlaying = false;
        let gameInterval;

        // Dron del jugador (Tecnología 2026)
        let drone = {
            x: 175,
            y: 410,
            width: 50,
            height: 35,
            speed: 7
        };

        let obstacles = [];
        let particles = [];
        let obstacleTimer = 0;
        let keys = {};

        window.addEventListener("keydown", (e) => { 
            if(["ArrowLeft","ArrowRight","KeyA","KeyD","Space"].includes(e.code)) {
                e.preventDefault(); 
            }
            keys[e.code] = true; 
        });
        window.addEventListener("keyup", (e) => { keys[e.code] = false; });

        function initGame() {
            score = 0;
            level = 1;
            obstacles = [];
            particles = [];
            drone.x = 175;
            obstacleTimer = 0;
            isPlaying = true;
            document.getElementById("start-btn").style.display = "none";
            canvas.focus();
            
            if(gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(updateAndDraw, 1000 / 60); // 60 FPS fluidos
        }

        function spawnObstacle() {
            let width = 35 + Math.random() * 25;
            let x = Math.random() * (canvas.width - width);
            let speed = 4 + level * 0.8; // Aumenta la velocidad según el nivel del 2026
            obstacles.push({ x: x, y: -45, width: width, height: 25, speed: speed });
        }

        function createExplosion(x, y) {
            for(let i = 0; i < 25; i++) {
                particles.push({
                    x: x,
                    y: y,
                    vx: (Math.random() - 0.5) * 8,
                    vy: (Math.random() - 0.5) * 8,
                    life: 30,
                    color: Math.random() > 0.5 ? '#00ffff' : '#ff0055'
                });
            }
        }

        function updateAndDraw() {
            if (!isPlaying) return;

            // --- LÓGICA DE MOVIMIENTO ---
            if ((keys["ArrowLeft"] || keys["KeyA"]) && drone.x > 0) {
                drone.x -= drone.speed;
            }
            if ((keys["ArrowRight"] || keys["KeyD"]) && drone.x + drone.width < canvas.width) {
                drone.x += drone.speed;
            }

            // Generador de obstáculos dinámico
            obstacleTimer++;
            let spawnRate = Math.max(25, 55 - (level * 5));
            if (obstacleTimer > spawnRate) {
                spawnObstacle();
                obstacleTimer = 0;
            }

            // Actualizar obstáculos (Satélites / Ciber-amenazas)
            for (let i = obstacles.length - 1; i >= 0; i--) {
                let obs = obstacles[i];
                obs.y += obs.speed;

                // Colisión con el dron
                if (
                    drone.x < obs.x + obs.width &&
                    drone.x + drone.width > obs.x &&
                    drone.y < obs.y + obs.height &&
                    drone.y + drone.height > obs.y
                ) {
                    isPlaying = false;
                    createExplosion(drone.x + drone.width/2, drone.y + drone.height/2);
                    setTimeout(() => {
                        alert("⚠️ ¡Colisión detectada! Sistema de vuelo interrumpido. Puntuación final: " + score);
                        document.getElementById("start-btn").style.display = "block";
                        document.getElementById("start-btn").innerText = "VOLVER A INTENTAR";
                    }, 100);
                }

                // Puntuación y eliminación
                if (obs.y > canvas.height) {
                    obstacles.splice(i, 1);
                    score += 15;
                    // Subir de nivel cada 100 puntos
                    level = Math.floor(score / 100) + 1;
                }
            }

            // --- RENDERIZADO GRÁFICO (Estilo Neón 2026) ---
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Fondo con rejilla cibernética sutil
            ctx.strokeStyle = "rgba(0, 255, 255, 0.04)";
            ctx.lineWidth = 1;
            for(let i = 0; i < canvas.width; i += 40) {
                ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height); ctx.stroke();
            }

            // Dibujar Dron Tecnológico 2026
            ctx.shadowBlur = 12;
            ctx.shadowColor = "#00ffff";
            ctx.fillStyle = "#00ffff";
            // Chasis central
            ctx.fillRect(drone.x + 10, drone.y + 10, 30, 15);
            // Propulsores laterales neón
            ctx.fillStyle = "#ff0055";
            ctx.fillRect(drone.x, drone.y + 5, 10, 8);
            ctx.fillRect(drone.x + 40, drone.y + 5, 10, 8);
            // Núcleo de energía central
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(drone.x + 20, drone.y + 13, 10, 9);
            ctx.shadowBlur = 0; // Reset sombra

            // Dibujar Obstáculos (Satélites / Ciber-bloques)
            ctx.shadowBlur = 10;
            ctx.shadowColor = "#ff0055";
            ctx.fillStyle = "#ff0055";
            obstacles.forEach(obs => {
                ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
                // Detalles internos del satélite
                ctx.fillStyle = "#ffffff";
                ctx.fillRect(obs.x + 5, obs.y + 5, obs.width - 10, 4);
                ctx.fillStyle = "#ff0055";
            });
            ctx.shadowBlur = 0;

            // Actualizar HUD de textos
            document.getElementById("score").innerText = "Puntuación: " + score;
            document.getElementById("level").innerText = "Nivel: " + level;
        }

        // Renderizado estático inicial antes de empezar
        function drawStatic() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#00ffff";
            ctx.font = "16px sans-serif";
            ctx.textAlign = "center";
            ctx.fillText("Presiona 'INICIAR VUELO' para comenzar", canvas.width / 2, canvas.height / 2);
        }
        drawStatic();
    </script>
</body>
</html>
"""

# Renderizar en Streamlit
components.html(game_code, height=580)
