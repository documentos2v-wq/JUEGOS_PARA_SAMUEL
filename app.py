import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Space Combat 2026 - Streamlit",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Space Combat 2026: Galaxy Odyssey")
st.write("Selecciona tu nave de alta visibilidad, destruye asteroides con la **Barra Espaciadora** y recoge las recompensas flotantes para mejorar tu poder de fuego y recuperar vidas.")

# Código HTML, CSS y JS con naves mejoradas y sistema de recompensas
game_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            background-color: #030309;
            color: #00ffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 10px;
        }
        #menu-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 10px;
            background: rgba(10, 15, 30, 0.95);
            padding: 15px;
            border-radius: 12px;
            border: 2px solid #00ffff;
            box-shadow: 0 0 20px rgba(0,255,255,0.3);
        }
        .ship-options {
            display: flex;
            gap: 15px;
            margin: 12px 0;
        }
        .ship-card {
            background: #111827;
            border: 2px solid #374151;
            padding: 12px;
            border-radius: 8px;
            cursor: pointer;
            text-align: center;
            transition: 0.2s;
            width: 115px;
        }
        .ship-card:hover, .ship-card.selected {
            border-color: #00ffff;
            background: #1f2937;
            box-shadow: 0 0 15px rgba(0,255,255,0.5);
            transform: translateY(-2px);
        }
        .ship-preview {
            font-size: 30px;
            margin-bottom: 5px;
        }
        #ui-container {
            display: flex;
            justify-content: space-between;
            width: 440px;
            margin-bottom: 8px;
            align-items: center;
        }
        #score, #level, #lives, #power {
            font-size: 14px;
            font-weight: bold;
            color: #00ffcc;
            text-shadow: 0 0 5px rgba(0,255,204,0.4);
        }
        #start-btn {
            background: linear-gradient(45deg, #00ffff, #0077ff);
            color: #030309;
            border: none;
            padding: 9px 22px;
            font-weight: bold;
            font-size: 15px;
            border-radius: 20px;
            cursor: pointer;
            box-shadow: 0 0 15px rgba(0,255,255,0.7);
            transition: 0.2s;
        }
        #start-btn:hover {
            transform: scale(1.05);
            background: linear-gradient(45deg, #ffffff, #00ffff);
        }
        canvas {
            border: 2px solid #00ffff;
            background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.25);
            border-radius: 8px;
            outline: none;
        }
    </style>
</head>
<body>

    <!-- MENÚ DE SELECCIÓN DE NAVE VISIBLE Y ATRACTIVA -->
    <div id="menu-container">
        <h3 style="margin-top:0; color:#38bdf8;">SELECCIONA TU NAVE DE COMBATE</h3>
        <div class="ship-options">
            <div class="ship-card selected" onclick="selectShip(0)" id="ship0">
                <div class="ship-preview">🛸</div>
                <div style="font-size:13px; font-weight:bold; color:#fff;">Vanguard</div>
                <div style="font-size:11px; color:#38bdf8;">Equilibrada</div>
            </div>
            <div class="ship-card" onclick="selectShip(1)" id="ship1">
                <div class="ship-preview">🚀</div>
                <div style="font-size:13px; font-weight:bold; color:#fff;">Interceptor</div>
                <div style="font-size:11px; color:#c084fc;">Ultra Rápida</div>
            </div>
            <div class="ship-card" onclick="selectShip(2)" id="ship2">
                <div class="ship-preview">🛰️</div>
                <div style="font-size:13px; font-weight:bold; color:#fff;">Titanium</div>
                <div style="font-size:11px; color:#fb923c;">Alta Resistencia</div>
            </div>
        </div>
        <button id="start-btn" onclick="initGame()">¡INICIAR COMBATE ESPACIAL!</button>
    </div>

    <div id="ui-container" style="display:none;">
        <div id="score">Puntuación: 0</div>
        <div id="lives">Vidas: ❤️❤️❤️</div>
        <div id="power">Láser: Normal</div>
        <div id="level">Nivel: 1</div>
    </div>
    
    <canvas id="gameCanvas" width="440" height="560" tabindex="1" style="display:none;"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let score = 0;
        let level = 1;
        let lives = 3;
        let powerLevel = 1; // 1: Normal, 2: Doble Láser, 3: Triple Láser Supremo
        let isPlaying = false;
        let gameInterval;
        let selectedShipType = 0;

        let ship = {
            x: 195,
            y: 450,
            width: 46,
            height: 48,
            speed: 6,
            color: "#00ffff"
        };

        let asteroids = [];
        let bullets = [];
        let rewards = [];
        let particles = [];
        let obstacleTimer = 0;
        let keys = {};
        let shootCooldown = 0;

        function selectShip(type) {
            selectedShipType = type;
            document.querySelectorAll('.ship-card').forEach((card, idx) => {
                if(idx === type) card.classList.add('selected');
                else card.classList.remove('selected');
            });

            if(type === 0) { ship.speed = 6.5; ship.color = "#00ffff"; }
            else if(type === 1) { ship.speed = 8.5; ship.color = "#a855f7"; }
            else if(type === 2) { ship.speed = 4.8; ship.color = "#f97316"; }
        }

        window.addEventListener("keydown", (e) => { 
            if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight","KeyW","KeyS","KeyA","KeyD","Space"].includes(e.code)) {
                e.preventDefault(); 
            }
            keys[e.code] = true; 
        });
        window.addEventListener("keyup", (e) => { keys[e.code] = false; });

        function initGame() {
            document.getElementById("menu-container").style.display = "none";
            document.getElementById("ui-container").style.display = "flex";
            canvas.style.display = "block";

            score = 0;
            level = 1;
            lives = 3;
            powerLevel = 1;
            asteroids = [];
            bullets = [];
            rewards = [];
            particles = [];
            ship.x = 195;
            ship.y = 450;
            obstacleTimer = 0;
            isPlaying = true;
            canvas.focus();
            
            if(gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(updateAndDraw, 1000 / 60);
        }

        function spawnAsteroid() {
            let radius = 18 + Math.random() * 18;
            let x = Math.random() * (canvas.width - radius * 2) + radius;
            let speed = 2.5 + level * 0.5 + Math.random() * 1.5;
            asteroids.push({
                x: x,
                y: -50,
                radius: radius,
                speed: speed,
                rotation: Math.random() * Math.PI,
                rotSpeed: (Math.random() - 0.5) * 0.04,
                hp: Math.ceil(radius / 14)
            });
        }

        function createReward(x, y) {
            // 35% de probabilidad de soltar recompensa al romper un asteroide
            if (Math.random() < 0.35) {
                let types = ['life', 'power', 'score'];
                let chosenType = types[Math.floor(Math.random() * types.length)];
                rewards.push({
                    x: x,
                    y: y,
                    type: chosenType,
                    radius: 12,
                    speed: 2.2
                });
            }
        }

        function createExplosion(x, y, color) {
            for(let i = 0; i < 22; i++) {
                particles.push({
                    x: x, y: y,
                    vx: (Math.random() - 0.5) * 6,
                    vy: (Math.random() - 0.5) * 6,
                    life: 25,
                    color: color
                });
            }
        }

        function updateAndDraw() {
            if (!isPlaying) return;

            // Movimiento libre en 4 direcciones
            if ((keys["ArrowLeft"] || keys["KeyA"]) && ship.x > 10) ship.x -= ship.speed;
            if ((keys["ArrowRight"] || keys["KeyD"]) && ship.x + ship.width < canvas.width - 10) ship.x += ship.speed;
            if ((keys["ArrowUp"] || keys["KeyW"]) && ship.y > 10) ship.y -= ship.speed;
            if ((keys["ArrowDown"] || keys["KeyS"]) && ship.y + ship.height < canvas.height - 10) ship.y += ship.speed;

            // Sistema de disparo avanzado con la barra espaciadora
            if (shootCooldown > 0) shootCooldown--;
            if (keys["Space"] && shootCooldown === 0) {
                if (powerLevel === 1) {
                    bullets.push({ x: ship.x + ship.width / 2 - 2, y: ship.y, width: 4, height: 14, speed: 11 });
                } else if (powerLevel === 2) {
                    bullets.push({ x: ship.x + 8, y: ship.y, width: 4, height: 14, speed: 11 });
                    bullets.push({ x: ship.x + ship.width - 12, y: ship.y, width: 4, height: 14, speed: 11 });
                } else {
                    bullets.push({ x: ship.x + ship.width / 2 - 2, y: ship.y, width: 4, height: 14, speed: 11 });
                    bullets.push({ x: ship.x + 4, y: ship.y + 10, width: 4, height: 14, speed: 11 });
                    bullets.push({ x: ship.x + ship.width - 8, y: ship.y + 10, width: 4, height: 14, speed: 11 });
                }
                shootCooldown = 10;
            }

            // Mover balas
            for (let i = bullets.length - 1; i >= 0; i--) {
                let b = bullets[i];
                b.y -= b.speed;
                if (b.y < 0) bullets.splice(i, 1);
            }

            // Mover y recoger recompensas
            for (let i = rewards.length - 1; i >= 0; i--) {
                let r = rewards[i];
                r.y += r.speed;

                // Colisión nave con recompensa
                let shipCenterX = ship.x + ship.width / 2;
                let shipCenterY = ship.y + ship.height / 2;
                let distToReward = Math.hypot(shipCenterX - r.x, shipCenterY - r.y);

                if (distToReward < r.radius + 20) {
                    if (r.type === 'life') {
                        if (lives < 5) lives++;
                    } else if (r.type === 'power') {
                        if (powerLevel < 3) powerLevel++;
                    } else if (r.type === 'score') {
                        score += 75;
                    }
                    rewards.splice(i, 1);
                    continue;
                }

                if (r.y > canvas.height + 20) rewards.splice(i, 1);
            }

            // Generador de asteroides
            obstacleTimer++;
            let spawnRate = Math.max(25, 48 - (level * 4));
            if (obstacleTimer > spawnRate) {
                spawnAsteroid();
                obstacleTimer = 0;
            }

            // Actualizar asteroides y colisiones
            for (let i = asteroids.length - 1; i >= 0; i--) {
                let ast = asteroids[i];
                ast.y += ast.speed;
                ast.rotation += ast.rotSpeed;

                // Colisión bala con asteroide
                for (let j = bullets.length - 1; j >= 0; j--) {
                    let b = bullets[j];
                    let dist = Math.hypot(b.x - ast.x, b.y - ast.y);
                    if (dist < ast.radius) {
                        bullets.splice(j, 1);
                        ast.hp--;
                        if (ast.hp <= 0) {
                            createExplosion(ast.x, ast.y, "#fdba74");
                            createReward(ast.x, ast.y);
                            score += 30;
                            level = Math.floor(score / 150) + 1;
                            asteroids.splice(i, 1);
                            break;
                        }
                    }
                }

                if (!asteroids[i]) continue;

                // Colisión nave con asteroide
                let shipCenterX = ship.x + ship.width / 2;
                let shipCenterY = ship.y + ship.height / 2;
                let collisionDist = Math.hypot(shipCenterX - ast.x, shipCenterY - ast.y);

                if (collisionDist < ast.radius + 16) {
                    createExplosion(shipCenterX, shipCenterY, "#ef4444");
                    asteroids.splice(i, 1);
                    lives--;
                    powerLevel = 1; // Pierde potencia al chocar
                    if (lives <= 0) {
                        isPlaying = false;
                        setTimeout(() => {
                            alert("💥 ¡Nave destruida! Fin de la misión. Puntuación final: " + score);
                            document.getElementById("menu-container").style.display = "flex";
                            document.getElementById("ui-container").style.display = "none";
                            canvas.style.display = "none";
                        }, 100);
                    }
                }

                if (ast.y > canvas.height + 50) {
                    asteroids.splice(i, 1);
                    score += 10;
                }
            }

            // --- RENDERIZADO VISIBLE Y ESTÉTICO ---
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Fondo estelar dinámico
            ctx.fillStyle = "rgba(255,255,255,0.2)";
            ctx.fillRect(80, (Date.now()/10)%canvas.height, 2, 2);
            ctx.fillRect(240, (Date.now()/7)%canvas.height, 3, 3);
            ctx.fillRect(370, (Date.now()/12)%canvas.height, 2, 2);

            // Dibujar Balas Láser brillantes
            ctx.fillStyle = powerLevel === 3 ? "#00ffcc" : "#38bdf8";
            ctx.shadowBlur = 10;
            ctx.shadowColor = ctx.fillStyle;
            bullets.forEach(b => ctx.fillRect(b.x, b.y, b.width, b.height));
            ctx.shadowBlur = 0;

            // Dibujar Recompensas Flotantes
            rewards.forEach(r => {
                ctx.save();
                ctx.translate(r.x, r.y);
                ctx.shadowBlur = 12;
                if (r.type === 'life') {
                    ctx.fillStyle = "#ef4444";
                    ctx.shadowColor = "#ef4444";
                    ctx.font = "20px sans-serif";
                    ctx.fillText("❤️", -10, 8);
                } else if (r.type === 'power') {
                    ctx.fillStyle = "#eab308";
                    ctx.shadowColor = "#eab308";
                    ctx.font = "20px sans-serif";
                    ctx.fillText("⚡", -10, 8);
                } else {
                    ctx.fillStyle = "#38bdf8";
                    ctx.shadowColor = "#38bdf8";
                    ctx.font = "20px sans-serif";
                    ctx.fillText("💎", -10, 8);
                }
                ctx.restore();
            });

            // --- DIBUJAR NAVE CON ALTA VISIBILIDAD Y DETALLE ---
            ctx.save();
            let sx = ship.x;
            let sy = ship.y;

            // Propulsores con brillo de plasma
            ctx.fillStyle = "#38bdf8";
            ctx.shadowBlur = 15;
            ctx.shadowColor = "#38bdf8";
            ctx.fillRect(sx + 12, sy + 44, 6, 8);
            ctx.fillRect(sx + 28, sy + 44, 6, 8);

            // Alas aerodinámicas con luces de neón
            ctx.fillStyle = ship.color;
            ctx.beginPath();
            ctx.moveTo(sx + 23, sy + 5);
            ctx.lineTo(sx - 4, sy + 38);
            ctx.lineTo(sx + 12, sy + 42);
            ctx.lineTo(sx + 23, sy + 28);
            ctx.fill();

            ctx.beginPath();
            ctx.moveTo(sx + 23, sy + 5);
            ctx.lineTo(sx + 50, sy + 38);
            ctx.lineTo(sx + 34, sy + 42);
            ctx.lineTo(sx + 23, sy + 28);
            ctx.fill();

            // Fuselaje principal metálico brillante
            ctx.fillStyle = "#f1f5f9";
            ctx.beginPath();
            ctx.moveTo(sx + 23, sy); // Nariz frontal
            ctx.lineTo(sx + 35, sy + 18);
            ctx.lineTo(sx + 35, sy + 44);
            ctx.lineTo(sx + 23, sy + 50); // Cola
            ctx.lineTo(sx + 11, sy + 44);
            ctx.lineTo(sx + 11, sy + 18);
            ctx.closePath();
            ctx.fill();

            // Cabina de cristal de alta visibilidad
            ctx.fillStyle = "#0284c7";
            ctx.shadowBlur = 8;
            ctx.shadowColor = "#0284c7";
            ctx.beginPath();
            ctx.ellipse(sx + 23, sy + 20, 5, 10, 0, 0, Math.PI * 2);
            ctx.fill();

            ctx.restore();

            // Dibujar Asteroides espaciales rotativos
            asteroids.forEach(ast => {
                ctx.save();
                ctx.translate(ast.x, ast.y);
                ctx.rotate(ast.rotation);
                ctx.fillStyle = "#b45309";
                ctx.strokeStyle = "#78350f";
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.arc(0, 0, ast.radius, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();
                ctx.restore();
            });

            // Partículas
            for (let i = particles.length - 1; i >= 0; i--) {
                let p = particles[i];
                p.x += p.vx; p.y += p.vy; p.life--;
                ctx.fillStyle = p.color;
                ctx.fillRect(p.x, p.y, 3, 3);
                if (p.life <= 0) particles.splice(i, 1);
            }

            // Actualizar HUD
            document.getElementById("score").innerText = "Puntuación: " + score;
            document.getElementById("level").innerText = "Nivel: " + level;
            let hearts = "";
            for(let h=0; h<lives; h++) hearts += "❤️";
            document.getElementById("lives").innerText = "Vidas: " + hearts;
            
            let powerText = "Normal";
            if(powerLevel === 2) powerText = "Doble ⚡";
            if(powerLevel === 3) powerText = "Supremo ⚡⚡";
            document.getElementById("power").innerText = "Láser: " + powerText;
        }
    </script>
</body>
</html>
"""

# Renderizar en Streamlit
components.html(game_code, height=650)
