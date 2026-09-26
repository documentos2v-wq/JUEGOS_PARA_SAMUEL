import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Space Combat 2026 - Streamlit",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Space Combat 2026: Escuadrón Estelar")
st.write("Selecciona tu nave, despega con el botón de inicio, muévete con total libertad y presiona la **Barra Espaciadora** para disparar y destruir los asteroides.")

# Código HTML, CSS y JS con selección de naves, disparos y asteroides
game_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            background-color: #050510;
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
            background: rgba(15, 23, 42, 0.9);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #00ffff;
        }
        .ship-options {
            display: flex;
            gap: 15px;
            margin: 10px 0;
        }
        .ship-card {
            background: #1e293b;
            border: 2px solid #334155;
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            text-align: center;
            transition: 0.2s;
            width: 110px;
        }
        .ship-card:hover, .ship-card.selected {
            border-color: #00ffff;
            background: #0f172a;
            box-shadow: 0 0 10px rgba(0,255,255,0.4);
        }
        .ship-card img, .ship-preview {
            font-size: 28px;
            margin-bottom: 5px;
        }
        #ui-container {
            display: flex;
            justify-content: space-between;
            width: 440px;
            margin-bottom: 8px;
            align-items: center;
        }
        #score, #level, #lives {
            font-size: 15px;
            font-weight: bold;
            color: #00ffcc;
        }
        #start-btn {
            background: linear-gradient(45deg, #00ffff, #0077ff);
            color: #050510;
            border: none;
            padding: 8px 20px;
            font-weight: bold;
            font-size: 14px;
            border-radius: 20px;
            cursor: pointer;
            box-shadow: 0 0 12px rgba(0,255,255,0.6);
        }
        #start-btn:hover {
            transform: scale(1.05);
        }
        canvas {
            border: 2px solid #00ffff;
            background: radial-gradient(circle at center, #0f172a 0%, #020617 100%);
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
            border-radius: 8px;
            outline: none;
        }
    </style>
</head>
<body>

    <!-- MENÚ DE SELECCIÓN DE NAVE -->
    <div id="menu-container">
        <h3>SELECCIONA TU NAVE</h3>
        <div class="ship-options">
            <div class="ship-card selected" onclick="selectShip(0)" id="ship0">
                <div class="ship-preview">🛸</div>
                <div style="font-size:13px; font-weight:bold;">Vanguard</div>
                <div style="font-size:11px; color:#94a3b8;">Equilibrada</div>
            </div>
            <div class="ship-card" onclick="selectShip(1)" id="ship1">
                <div class="ship-preview">🚀</div>
                <div style="font-size:13px; font-weight:bold;">Interceptor</div>
                <div style="font-size:11px; color:#94a3b8;">Rápida</div>
            </div>
            <div class="ship-card" onclick="selectShip(2)" id="ship2">
                <div class="ship-preview">🛰️</div>
                <div style="font-size:13px; font-weight:bold;">Titan</div>
                <div style="font-size:11px; color:#94a3b8;">Resistente</div>
            </div>
        </div>
        <button id="start-btn" onclick="initGame()">¡DESPEGAR MISION!</button>
    </div>

    <div id="ui-container" style="display:none;" id="hud">
        <div id="score">Puntuación: 0</div>
        <div id="lives">Vidas: ❤️❤️❤️</div>
        <div id="level">Nivel: 1</div>
    </div>
    
    <canvas id="gameCanvas" width="440" height="560" tabindex="1" style="display:none;"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let score = 0;
        let level = 1;
        let lives = 3;
        let isPlaying = false;
        let gameInterval;
        let selectedShipType = 0; // 0: Vanguard, 1: Interceptor, 2: Titan

        // Configuración de la nave del jugador
        let ship = {
            x: 195,
            y: 450,
            width: 45,
            height: 45,
            speed: 6,
            color: "#00ffff"
        };

        let asteroids = [];
        let bullets = [];
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

            if(type === 0) { ship.speed = 6; ship.color = "#00ffff"; }
            else if(type === 1) { ship.speed = 8; ship.color = "#a855f7"; }
            else if(type === 2) { ship.speed = 4.5; ship.color = "#f97316"; }
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
            asteroids = [];
            bullets = [];
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
            let radius = 18 + Math.random() * 16;
            let x = Math.random() * (canvas.width - radius * 2) + radius;
            let speed = 2.5 + level * 0.5 + Math.random() * 1.5;
            asteroids.push({
                x: x,
                y: -50,
                radius: radius,
                speed: speed,
                rotation: Math.random() * Math.PI,
                rotSpeed: (Math.random() - 0.5) * 0.05,
                hp: Math.ceil(radius / 15) // Los más grandes requieren más disparos
            });
        }

        function createExplosion(x, y, color) {
            for(let i = 0; i < 25; i++) {
                particles.push({
                    x: x,
                    y: y,
                    vx: (Math.random() - 0.5) * 7,
                    vy: (Math.random() - 0.5) * 7,
                    life: 30,
                    color: color
                });
            }
        }

        function updateAndDraw() {
            if (!isPlaying) return;

            // --- CONTROLES DE MOVIMIENTO LIBRE (4 EJES) ---
            if ((keys["ArrowLeft"] || keys["KeyA"]) && ship.x > 10) ship.x -= ship.speed;
            if ((keys["ArrowRight"] || keys["KeyD"]) && ship.x + ship.width < canvas.width - 10) ship.x += ship.speed;
            if ((keys["ArrowUp"] || keys["KeyW"]) && ship.y > 10) ship.y -= ship.speed;
            if ((keys["ArrowDown"] || keys["KeyS"]) && ship.y + ship.height < canvas.height - 10) ship.y += ship.speed;

            // --- SISTEMA DE DISPARO (Barra Espaciadora) ---
            if (shootCooldown > 0) shootCooldown--;
            if (keys["Space"] && shootCooldown === 0) {
                bullets.push({ x: ship.x + ship.width / 2 - 2, y: ship.y, width: 4, height: 12, speed: 10 });
                shootCooldown = 12; // Cadencia de disparo
            }

            // Mover Balas
            for (let i = bullets.length - 1; i >= 0; i--) {
                let b = bullets[i];
                b.y -= b.speed;
                if (b.y < 0) bullets.splice(i, 1);
            }

            // Generador de Asteroide
            obstacleTimer++;
            let spawnRate = Math.max(25, 50 - (level * 4));
            if (obstacleTimer > spawnRate) {
                spawnAsteroid();
                obstacleTimer = 0;
            }

            // Actualizar Asteroide y Colisiones
            for (let i = asteroids.length - 1; i >= 0; i--) {
                let ast = asteroids[i];
                ast.y += ast.speed;
                ast.rotation += ast.rotSpeed;

                // Colisión Bala <-> Asteroide
                for (let j = bullets.length - 1; j >= 0; j--) {
                    let b = bullets[j];
                    let dist = Math.hypot(b.x - ast.x, b.y - ast.y);
                    if (dist < ast.radius) {
                        bullets.splice(j, 1);
                        ast.hp--;
                        if (ast.hp <= 0) {
                            createExplosion(ast.x, ast.y, "#fdba74");
                            score += 25;
                            level = Math.floor(score / 120) + 1;
                            asteroids.splice(i, 1);
                            break;
                        }
                    }
                }

                if (!asteroids[i]) continue;

                // Colisión Nave <-> Asteroide
                let shipCenterX = ship.x + ship.width / 2;
                let shipCenterY = ship.y + ship.height / 2;
                let collisionDist = Math.hypot(shipCenterX - ast.x, shipCenterY - ast.y);

                if (collisionDist < ast.radius + 15) {
                    createExplosion(shipCenterX, shipCenterY, "#ef4444");
                    asteroids.splice(i, 1);
                    lives--;
                    if (lives <= 0) {
                        isPlaying = false;
                        setTimeout(() => {
                            alert("💥 ¡Nave destruida! Fin de la misión. Puntuación: " + score);
                            document.getElementById("menu-container").style.display = "flex";
                            document.getElementById("ui-container").style.display = "none";
                            canvas.style.display = "none";
                        }, 100);
                    }
                }

                // Asteroide fuera de pantalla
                if (ast.y > canvas.height + 50) {
                    asteroids.splice(i, 1);
                    score += 5;
                }
            }

            // --- RENDERIZADO GRÁFICO ---
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Estrellas de fondo
            ctx.fillStyle = "rgba(255,255,255,0.15)";
            ctx.fillRect(50, (Date.now()/12)%canvas.height, 2, 2);
            ctx.fillRect(200, (Date.now()/8)%canvas.height, 3, 3);
            ctx.fillRect(350, (Date.now()/15)%canvas.height, 2, 2);

            // Dibujar Balas Láser
            ctx.fillStyle = "#38bdf8";
            ctx.shadowBlur = 8;
            ctx.shadowColor = "#38bdf8";
            bullets.forEach(b => ctx.fillRect(b.x, b.y, b.width, b.height));
            ctx.shadowBlur = 0;

            // Dibujar Naves según selección
            ctx.save();
            let sx = ship.x;
            let sy = ship.y;
            ctx.fillStyle = ship.color;
            ctx.shadowBlur = 10;
            ctx.shadowColor = ship.color;

            if (selectedShipType === 0) { // Vanguard (Caza estelar clásico)
                ctx.beginPath();
                ctx.moveTo(sx + 22, sy);
                ctx.lineTo(sx + 45, sy + 35);
                ctx.lineTo(sx + 30, sy + 28);
                ctx.lineTo(sx + 22, sy + 40);
                ctx.lineTo(sx + 15, sy + 28);
                ctx.lineTo(sx, sy + 35);
                ctx.closePath();
                ctx.fill();
            } else if (selectedShipType === 1) { // Interceptor (Estilo veloz agudo)
                ctx.beginPath();
                ctx.moveTo(sx + 22, sy - 5);
                ctx.lineTo(sx + 42, sy + 40);
                ctx.lineTo(sx + 22, sy + 30);
                ctx.lineTo(sx, sy + 40);
                ctx.closePath();
                ctx.fill();
            } else { // Titan (Nave pesada y robusta)
                ctx.fillRect(sx + 8, sy + 5, 28, 35);
                ctx.fillStyle = "#cbd5e1";
                ctx.fillRect(sx, sy + 15, 44, 12);
            }
            ctx.restore();

            // Dibujar Asteroides en rotación
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
        }
    </script>
</body>
</html>
"""

# Renderizar en Streamlit
components.html(game_code, height=650)
