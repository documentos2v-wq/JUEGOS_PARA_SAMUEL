import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Galaxy Combat 2026 - Streamlit",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Galaxy Combat 2026: Deep Space Odyssey")
st.write("Disfruta de gráficos de alta definición con naves detalladas, un fondo de galaxia realista en movimiento, sistema de disparos láser y recompensas flotantes.")

# Código HTML, CSS y JS con Galaxia de fondo y Naves HD detalladas
game_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            background-color: #020205;
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
            box-shadow: 0 0 20px rgba(0,255,255,0.4);
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
            box-shadow: 0 0 15px rgba(0,255,255,0.6);
            transform: translateY(-2px);
        }
        .ship-preview {
            font-size: 32px;
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
            color: #020205;
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
            background: #020510;
            box-shadow: 0 0 35px rgba(0, 255, 255, 0.3);
            border-radius: 8px;
            outline: none;
        }
    </style>
</head>
<body>

    <!-- MENÚ DE SELECCIÓN DE NAVE HD -->
    <div id="menu-container">
        <h3 style="margin-top:0; color:#38bdf8;">SELECCIONA TU NAVE DE COMBATE HD</h3>
        <div class="ship-options">
            <div class="ship-card selected" onclick="selectShip(0)" id="ship0">
                <div class="ship-preview">🛸</div>
                <div style="font-size:13px; font-weight:bold; color:#fff;">Vanguard HD</div>
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
                <div style="font-size:11px; color:#fb923c;">Alta Blindaje</div>
            </div>
        </div>
        <button id="start-btn" onclick="initGame()">¡DESPEGAR A LA GALAXIA!</button>
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
        let powerLevel = 1; 
        let isPlaying = false;
        let gameInterval;
        let selectedShipType = 0;

        let ship = {
            x: 195,
            y: 440,
            width: 50,
            height: 52,
            speed: 6.5
        };

        let asteroids = [];
        let bullets = [];
        let rewards = [];
        let particles = [];
        let galaxyOffset = 0;
        let obstacleTimer = 0;
        let keys = {};
        let shootCooldown = 0;

        function selectShip(type) {
            selectedShipType = type;
            document.querySelectorAll('.ship-card').forEach((card, idx) => {
                if(idx === type) card.classList.add('selected');
                else card.classList.remove('selected');
            });

            if(type === 0) ship.speed = 6.5;
            else if(type === 1) ship.speed = 8.5;
            else if(type === 2) ship.speed = 4.8;
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
            ship.y = 440;
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
            if (Math.random() < 0.35) {
                let types = ['life', 'power', 'score'];
                let chosenType = types[Math.floor(Math.random() * types.length)];
                rewards.push({ x: x, y: y, type: chosenType, radius: 12, speed: 2.2 });
            }
        }

        function createExplosion(x, y, color) {
            for(let i = 0; i < 24; i++) {
                particles.push({
                    x: x, y: y,
                    vx: (Math.random() - 0.5) * 7,
                    vy: (Math.random() - 0.5) * 7,
                    life: 28,
                    color: color
                });
            }
        }

        function updateAndDraw() {
            if (!isPlaying) return;

            // Movimiento en 4 ejes
            if ((keys["ArrowLeft"] || keys["KeyA"]) && ship.x > 10) ship.x -= ship.speed;
            if ((keys["ArrowRight"] || keys["KeyD"]) && ship.x + ship.width < canvas.width - 10) ship.x += ship.speed;
            if ((keys["ArrowUp"] || keys["KeyW"]) && ship.y > 10) ship.y -= ship.speed;
            if ((keys["ArrowDown"] || keys["KeyS"]) && ship.y + ship.height < canvas.height - 10) ship.y += ship.speed;

            // Disparos láser con barra espaciadora
            if (shootCooldown > 0) shootCooldown--;
            if (keys["Space"] && shootCooldown === 0) {
                if (powerLevel === 1) {
                    bullets.push({ x: ship.x + ship.width / 2 - 2, y: ship.y, width: 4, height: 14, speed: 12 });
                } else if (powerLevel === 2) {
                    bullets.push({ x: ship.x + 8, y: ship.y, width: 4, height: 14, speed: 12 });
                    bullets.push({ x: ship.x + ship.width - 12, y: ship.y, width: 4, height: 14, speed: 12 });
                } else {
                    bullets.push({ x: ship.x + ship.width / 2 - 2, y: ship.y, width: 4, height: 14, speed: 12 });
                    bullets.push({ x: ship.x + 4, y: ship.y + 10, width: 4, height: 14, speed: 12 });
                    bullets.push({ x: ship.x + ship.width - 8, y: ship.y + 10, width: 4, height: 14, speed: 12 });
                }
                shootCooldown = 9;
            }

            for (let i = bullets.length - 1; i >= 0; i--) {
                let b = bullets[i];
                b.y -= b.speed;
                if (b.y < 0) bullets.splice(i, 1);
            }

            for (let i = rewards.length - 1; i >= 0; i--) {
                let r = rewards[i];
                r.y += r.speed;
                let shipCenterX = ship.x + ship.width / 2;
                let shipCenterY = ship.y + ship.height / 2;
                if (Math.hypot(shipCenterX - r.x, shipCenterY - r.y) < r.radius + 20) {
                    if (r.type === 'life' && lives < 5) lives++;
                    else if (r.type === 'power' && powerLevel < 3) powerLevel++;
                    else if (r.type === 'score') score += 75;
                    rewards.splice(i, 1);
                    continue;
                }
                if (r.y > canvas.height + 20) rewards.splice(i, 1);
            }

            obstacleTimer++;
            let spawnRate = Math.max(25, 48 - (level * 4));
            if (obstacleTimer > spawnRate) {
                spawnAsteroid();
                obstacleTimer = 0;
            }

            for (let i = asteroids.length - 1; i >= 0; i--) {
                let ast = asteroids[i];
                ast.y += ast.speed;
                ast.rotation += ast.rotSpeed;

                for (let j = bullets.length - 1; j >= 0; j--) {
                    let b = bullets[j];
                    if (Math.hypot(b.x - ast.x, b.y - ast.y) < ast.radius) {
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

                let shipCenterX = ship.x + ship.width / 2;
                let shipCenterY = ship.y + ship.height / 2;
                if (Math.hypot(shipCenterX - ast.x, shipCenterY - ast.y) < ast.radius + 16) {
                    createExplosion(shipCenterX, shipCenterY, "#ef4444");
                    asteroids.splice(i, 1);
                    lives--;
                    powerLevel = 1;
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

            // --- RENDERIZADO VISUAL CON GALAXIA DE FONDO Y NAVE HD ---
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Dibujar Fondo de Galaxia en Movimiento
            galaxyOffset += 0.2;
            let gradient = ctx.createRadialGradient(canvas.width / 2, canvas.height / 2 + (galaxyOffset % 50), 20, canvas.width / 2, canvas.height / 2, 350);
            gradient.addColorStop(0, "rgba(76, 29, 149, 0.35)"); // Núcleo morado galáctico
            gradient.addColorStop(0.5, "rgba(14, 116, 144, 0.2)"); // Anillo cian
            gradient.addColorStop(1, "#020205"); // Oscuridad espacial exterior
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Estrellas de fondo estelares
            ctx.fillStyle = "rgba(255,255,255,0.3)";
            ctx.fillRect(60, (Date.now()/9)%canvas.height, 2, 2);
            ctx.fillRect(220, (Date.now()/6)%canvas.height, 3, 3);
            ctx.fillRect(380, (Date.now()/11)%canvas.height, 2, 2);

            // 2. Dibujar Balas Láser
            ctx.fillStyle = powerLevel === 3 ? "#00ffcc" : "#38bdf8";
            ctx.shadowBlur = 12;
            ctx.shadowColor = ctx.fillStyle;
            bullets.forEach(b => ctx.fillRect(b.x, b.y, b.width, b.height));
            ctx.shadowBlur = 0;

            // 3. Dibujar Recompensas
            rewards.forEach(r => {
                ctx.save();
                ctx.translate(r.x, r.y);
                ctx.shadowBlur = 12;
                ctx.font = "20px sans-serif";
                if (r.type === 'life') { ctx.shadowColor = "#ef4444"; ctx.fillText("❤️", -10, 8); }
                else if (r.type === 'power') { ctx.shadowColor = "#eab308"; ctx.fillText("⚡", -10, 8); }
                else { ctx.shadowColor = "#38bdf8"; ctx.fillText("💎", -10, 8); }
                ctx.restore();
            });

            // 4. --- NAVE HD ULTRA DETALLADA (Segun tu selección) ---
            ctx.save();
            let sx = ship.x;
            let sy = ship.y;

            // Estela de propulsión plasma brillante
            ctx.fillStyle = selectedShipType === 1 ? "#c084fc" : "#00ffff";
            ctx.shadowBlur = 18;
            ctx.shadowColor = ctx.fillStyle;
            ctx.fillRect(sx + 14, sy + 48, 6, 10);
            ctx.fillRect(sx + 30, sy + 48, 6, 10);

            if (selectedShipType === 0) {
                // VANGUARD HD (Caza aerodinámico estilizado)
                ctx.fillStyle = "#38bdf8"; // Alas principales
                ctx.beginPath();
                ctx.moveTo(sx + 25, sy + 4);
                ctx.lineTo(sx - 2, sy + 36);
                ctx.lineTo(sx + 14, sy + 44);
                ctx.lineTo(sx + 25, sy + 30);
                ctx.fill();

                ctx.beginPath();
                ctx.moveTo(sx + 25, sy + 4);
                ctx.lineTo(sx + 52, sy + 36);
                ctx.lineTo(sx + 36, sy + 44);
                ctx.lineTo(sx + 25, sy + 30);
                ctx.fill();

                // Fuselaje blindado plateado
                ctx.fillStyle = "#e2e8f0";
                ctx.beginPath();
                ctx.moveTo(sx + 25, sy);
                ctx.lineTo(sx + 36, sy + 15);
                ctx.lineTo(sx + 36, sy + 46);
                ctx.lineTo(sx + 25, sy + 52);
                ctx.lineTo(sx + 14, sy + 46);
                ctx.lineTo(sx + 14, sy + 15);
                ctx.closePath();
                ctx.fill();

                // Cabina de cristal azul neón
                ctx.fillStyle = "#0284c7";
                ctx.shadowBlur = 10;
                ctx.shadowColor = "#38bdf8";
                ctx.beginPath();
                ctx.ellipse(sx + 25, sy + 20, 5, 12, 0, 0, Math.PI * 2);
                ctx.fill();

            } else if (selectedShipType === 1) {
                // INTERCEPTOR (Nave veloz futurista violeta)
                ctx.fillStyle = "#c084fc";
                ctx.beginPath();
                ctx.moveTo(sx + 25, sy - 2);
                ctx.lineTo(sx + 2, sy + 42);
                ctx.lineTo(sx + 25, sy + 32);
                ctx.lineTo(sx + 48, sy + 42);
                ctx.closePath();
                ctx.fill();

                ctx.fillStyle = "#f3e8ff";
                ctx.beginPath();
                ctx.moveTo(sx + 25, sy + 4);
                ctx.lineTo(sx + 14, sy + 38);
                ctx.lineTo(sx + 25, sy + 46);
                ctx.lineTo(sx + 36, sy + 38);
                ctx.closePath();
                ctx.fill();

                ctx.fillStyle = "#38bdf8";
                ctx.shadowBlur = 10;
                ctx.shadowColor = "#c084fc";
                ctx.beginPath();
                ctx.ellipse(sx + 25, sy + 22, 4, 10, 0, 0, Math.PI * 2);
                ctx.fill();

            } else {
                // TITANIUM (Nave de asalto robusta dorada/naranja)
                ctx.fillStyle = "#ea580c";
                ctx.fillRect(sx + 6, sy + 10, 38, 36);

                ctx.fillStyle = "#fb923c";
                ctx.fillRect(sx, sy + 20, 50, 16);

                ctx.fillStyle = "#fef08a";
                ctx.shadowBlur = 10;
                ctx.shadowColor = "#f97316";
                ctx.fillRect(sx + 18, sy + 15, 14, 22);
            }

            ctx.restore();

            // 5. Dibujar Asteroides
            asteroids.forEach(ast => {
                ctx.save();
                ctx.translate(ast.x, ast.y);
                ctx.rotate(ast.rotation);
                ctx.fillStyle = "#9a3412";
                ctx.strokeStyle = "#431407";
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

            // HUD
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
