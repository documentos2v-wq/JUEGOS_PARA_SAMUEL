import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Flight 2026 - Streamlit",
    page_icon="✈️",
    layout="centered"
)

st.title("✈️ Sky Flight Simulator 2026")
st.write("Toma el control total del avión comercial con movimiento libre en **ambas direcciones** (arriba, abajo, izquierda y derecha). ¡Esquiva los meteoritos!")

# Código HTML, CSS y JS con avión detallado y movimiento en 4 direcciones
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
            width: 420px;
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
            background: linear-gradient(to bottom, #050b14, #111e38);
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
    
    <canvas id="gameCanvas" width="420" height="550" tabindex="1"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let score = 0;
        let level = 1;
        let isPlaying = false;
        let gameInterval;

        // Avión realista con movimiento en 4 direcciones
        let plane = {
            x: 185,
            y: 440,
            width: 50,
            height: 55,
            speed: 6
        };

        let obstacles = [];
        let particles = [];
        let obstacleTimer = 0;
        let keys = {};

        window.addEventListener("keydown", (e) => { 
            if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight","KeyW","KeyS","KeyA","KeyD","Space"].includes(e.code)) {
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
            plane.x = 185;
            plane.y = 440;
            obstacleTimer = 0;
            isPlaying = true;
            document.getElementById("start-btn").style.display = "none";
            canvas.focus();
            
            if(gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(updateAndDraw, 1000 / 60);
        }

        function spawnObstacle() {
            let width = 40 + Math.random() * 30;
            let x = Math.random() * (canvas.width - width);
            let speed = 3.5 + level * 0.7;
            obstacles.push({ x: x, y: -50, width: width, height: 30, speed: speed });
        }

        function createExplosion(x, y) {
            for(let i = 0; i < 30; i++) {
                particles.push({
                    x: x,
                    y: y,
                    vx: (Math.random() - 0.5) * 9,
                    vy: (Math.random() - 0.5) * 9,
                    life: 35,
                    color: Math.random() > 0.4 ? '#ff3300' : '#ffcc00'
                });
            }
        }

        function updateAndDraw() {
            if (!isPlaying) return;

            // --- MOVIMIENTO LIBRE EN AMBAS DIRECCIONES (4 EJES) ---
            // Horizontal (Izquierda / Derecha)
            if ((keys["ArrowLeft"] || keys["KeyA"]) && plane.x > 0) {
                plane.x -= plane.speed;
            }
            if ((keys["ArrowRight"] || keys["KeyD"]) && plane.x + plane.width < canvas.width) {
                plane.x += plane.speed;
            }
            // Vertical (Arriba / Abajo)
            if ((keys["ArrowUp"] || keys["KeyW"]) && plane.y > 10) {
                plane.y -= plane.speed;
            }
            if ((keys["ArrowDown"] || keys["KeyS"]) && plane.y + plane.height < canvas.height - 10) {
                plane.y += plane.speed;
            }

            // Generador de obstáculos
            obstacleTimer++;
            let spawnRate = Math.max(25, 55 - (level * 5));
            if (obstacleTimer > spawnRate) {
                spawnObstacle();
                obstacleTimer = 0;
            }

            // Actualizar obstáculos
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
                    isPlaying = false;
                    createExplosion(plane.x + plane.width/2, plane.y + plane.height/2);
                    setTimeout(() => {
                        alert("💥 ¡Impacto! Vuelo accidentado. Puntuación final: " + score);
                        document.getElementById("start-btn").style.display = "block";
                        document.getElementById("start-btn").innerText = "VOLVER A INTENTAR";
                    }, 100);
                }

                // Puntuación
                if (obs.y > canvas.height) {
                    obstacles.splice(i, 1);
                    score += 15;
                    level = Math.floor(score / 100) + 1;
                }
            }

            // --- RENDERIZADO GRÁFICO ---
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Nubes de fondo en movimiento estético
            ctx.fillStyle = "rgba(255, 255, 255, 0.03)";
            ctx.fillRect(40, (Date.now() / 15) % canvas.height, 60, 20);
            ctx.fillRect(300, (Date.now() / 10) % canvas.height, 80, 25);

            // --- DIBUJAR UN AVIÓN REALISTA ---
            ctx.save();
            let px = plane.x;
            let py = plane.y;

            // Estela de turbina trasera
            ctx.fillStyle = "rgba(0, 150, 255, 0.5)";
            ctx.fillRect(px + 21, py + 48, 8, 12);

            // Alas principales
            ctx.fillStyle = "#cbd5e1";
            ctx.beginPath();
            ctx.moveTo(px + 25, py + 15);
            ctx.lineTo(px - 10, py + 35);
            ctx.lineTo(px + 5, py + 42);
            ctx.lineTo(px + 25, py + 30);
            ctx.fill();

            ctx.beginPath();
            ctx.moveTo(px + 25, py + 15);
            ctx.lineTo(px + 60, py + 35);
            ctx.lineTo(px + 45, py + 42);
            ctx.lineTo(px + 25, py + 30);
            ctx.fill();

            // Fuselaje central aerodinámico
            ctx.fillStyle = "#f8fafc";
            ctx.beginPath();
            ctx.moveTo(px + 25, py); // Nariz
            ctx.lineTo(px + 38, py + 18);
            ctx.lineTo(px + 38, py + 48);
            ctx.lineTo(px + 25, py + 55); // Cola
            ctx.lineTo(px + 12, py + 48);
            ctx.lineTo(px + 12, py + 18);
            ctx.closePath();
            ctx.fill();

            // Cabina (Ventana de la tripulación)
            ctx.fillStyle = "#0284c7";
            ctx.beginPath();
            ctx.ellipse(px + 25, py + 16, 4, 8, 0, 0, Math.PI * 2);
            ctx.fill();

            // Alerón trasero
            ctx.fillStyle = "#94a3b8";
            ctx.fillRect(px + 18, py + 48, 14, 5);

            ctx.restore();

            // --- DIBUJAR OBSTÁCULOS (Meteoritos espaciales) ---
            obstacles.forEach(obs => {
                ctx.fillStyle = "#ef4444";
                ctx.beginPath();
                ctx.arc(obs.x + obs.width / 2, obs.y + obs.height / 2, obs.width / 2, 0, Math.PI * 2);
                ctx.fill();
                // Detalles del meteorito
                ctx.fillStyle = "#b91c1c";
                ctx.fillRect(obs.x + 8, obs.y + 8, 8, 8);
            });

            // Partículas de explosión
            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                p.x += p.vx;
                p.y += p.vy;
                p.life--;
                ctx.fillStyle = p.color;
                ctx.fillRect(p.x, p.y, 4, 4);
                if (p.life <= 0) particles.splice(i, 1);
            }

            // Actualizar interfaz HUD
            document.getElementById("score").innerText = "Puntuación: " + score;
            document.getElementById("level").innerText = "Nivel: " + level;
        }

        function drawStatic() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#00ffff";
            ctx.font = "15px sans-serif";
            ctx.textAlign = "center";
            ctx.fillText("Haz clic en 'INICIAR VUELO' para despegar", canvas.width / 2, canvas.height / 2);
        }
        drawStatic();
    </script>
</body>
</html>
"""

# Renderizar en Streamlit
components.html(game_code, height=620)
