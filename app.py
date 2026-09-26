import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Cyber Fighter 2026 - Streamlit",
    page_icon="🥋",
    layout="centered"
)

st.title("🥋 Cyber Fighter 2026: Ultra Combat")
st.write("Controles avanzados. **P1:** Moverse (A/D), Saltar (W), Agacharse (S), Golpear (F), Defender/Bloquear (E). **P2:** Moverse (Flechas), Saltar (Arriba), Agacharse (Abajo), Golpear (L), Defender/Bloquear (Shift Derecho).")

# Código HTML, CSS y JS con luchadores detallados, agacharse y defensa
game_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            background-color: #030309;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 10px;
        }
        #hud-container {
            display: flex;
            justify-content: space-between;
            width: 580px;
            margin-bottom: 10px;
            font-weight: bold;
            font-size: 14px;
        }
        .player-hud {
            display: flex;
            flex-direction: column;
            width: 260px;
        }
        .health-bar {
            width: 100%;
            height: 22px;
            background: #1e1b4b;
            border: 2px solid #00ffff;
            border-radius: 6px;
            overflow: hidden;
            box-shadow: 0 0 10px rgba(0,255,255,0.3);
            margin-top: 4px;
        }
        .health-fill-p1 {
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, #ef4444, #f97316);
            transition: width 0.1s;
        }
        .health-fill-p2 {
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, #3b82f6, #06b6d4);
            transition: width 0.1s;
        }
        #start-btn {
            background: linear-gradient(45deg, #00ffff, #3b82f6);
            color: #030309;
            border: none;
            padding: 10px 28px;
            font-weight: bold;
            font-size: 15px;
            border-radius: 25px;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(0,255,255,0.7);
            margin-bottom: 12px;
            transition: 0.2s;
        }
        #start-btn:hover {
            transform: scale(1.05);
            background: linear-gradient(45deg, #ffffff, #00ffff);
        }
        canvas {
            border: 2px solid #00ffff;
            background: radial-gradient(circle at center, #1e1b4b 0%, #050510 100%);
            box-shadow: 0 0 40px rgba(0, 255, 255, 0.35);
            border-radius: 10px;
            outline: none;
        }
    </style>
</head>
<body>

    <button id="start-btn" onclick="initGame()">🥋 INICIAR COMBATE PROFESIONAL</button>

    <div id="hud-container">
        <div class="player-hud" style="color: #f97316;">
            <span>PLAYER 1 [ CIBER-RED ] (Defensa: E)</span>
            <div class="health-bar"><div id="hp1" class="health-fill-p1"></div></div>
        </div>
        <div class="player-hud" style="color: #06b6d4; text-align: right;">
            <span>PLAYER 2 [ CIBER-BLUE ] (Defensa: Shift)</span>
            <div class="health-bar"><div id="hp2" class="health-fill-p2"></div></div>
        </div>
    </div>
    
    <canvas id="gameCanvas" width="580" height="380" tabindex="1"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let isPlaying = false;
        let gameInterval;
        let keys = {};
        let particles = [];

        // Jugador 1
        let p1 = {
            x: 100,
            y: 240,
            width: 36,
            height: 80,
            color: "#f97316",
            speed: 5,
            hp: 100,
            vy: 0,
            isJumping: false,
            isCrouching: false,
            isBlocking: false,
            isPunching: false,
            direction: 1
        };

        // Jugador 2
        let p2 = {
            x: 440,
            y: 240,
            width: 36,
            height: 80,
            color: "#06b6d4",
            speed: 5,
            hp: 100,
            vy: 0,
            isJumping: false,
            isCrouching: false,
            isBlocking: false,
            isPunching: false,
            direction: -1
        };

        window.addEventListener("keydown", (e) => {
            if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight","KeyW","KeyS","KeyA","KeyD","KeyF","KeyL","KeyE","ShiftRight","Space"].includes(e.code)) {
                e.preventDefault();
            }
            keys[e.code] = true;

            if(e.code === "KeyF" && isPlaying) attack(p1, p2, "#f97316");
            if(e.code === "KeyL" && isPlaying) attack(p2, p1, "#06b6d4");
        });

        window.addEventListener("keyup", (e) => {
            keys[e.code] = false;
        });

        function initGame() {
            p1.x = 100; p1.y = 240; p1.hp = 100; p1.vy = 0; p1.isJumping = false; p1.isCrouching = false;
            p2.x = 440; p2.y = 240; p2.hp = 100; p2.vy = 0; p2.isJumping = false; p2.isCrouching = false;
            particles = [];
            isPlaying = true;
            document.getElementById("start-btn").style.display = "none";
            canvas.focus();

            if(gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(updateAndDraw, 1000 / 60);
        }

        function attack(attacker, defender, color) {
            attacker.isPunching = true;
            setTimeout(() => { attacker.isPunching = false; }, 140);

            let dist = Math.abs((attacker.x + attacker.width/2) - (defender.x + defender.width/2));
            let sameHeight = Math.abs(attacker.y - defender.y) < 55;

            if (dist < 70 && sameHeight) {
                if (defender.isBlocking) {
                    // Si está defendiendo, no recibe daño y salen chispas de bloqueo
                    for(let i=0; i<8; i++) {
                        particles.push({
                            x: defender.x + defender.width/2, y: defender.y + 35,
                            vx: (Math.random() - 0.5) * 6, vy: (Math.random() - 0.5) * 6,
                            life: 15, color: "#38bdf8"
                        });
                    }
                } else {
                    defender.hp -= 10;
                    if (defender.hp < 0) defender.hp = 0;
                    updateHUD();

                    for(let i=0; i<12; i++) {
                        particles.push({
                            x: defender.x + defender.width/2, y: defender.y + 35,
                            vx: (Math.random() - 0.5) * 8, vy: (Math.random() - 0.5) * 8,
                            life: 20, color: color
                        });
                    }

                    if (defender.hp === 0) {
                        isPlaying = false;
                        let winner = attacker === p1 ? "🏆 ¡PLAYER 1 GANA EL COMBATE!" : "🏆 ¡PLAYER 2 GANA EL COMBATE!";
                        setTimeout(() => {
                            alert(winner);
                            document.getElementById("start-btn").style.display = "block";
                            document.getElementById("start-btn").innerText = "🔄 REVANCHA";
                        }, 150);
                    }
                }
            }
        }

        function updateHUD() {
            document.getElementById("hp1").style.width = p1.hp + "%";
            document.getElementById("hp2").style.width = p2.hp + "%";
        }

        function updateAndDraw() {
            if (!isPlaying) return;

            // --- CONTROLES P1 ---
            p1.isCrouching = keys["KeyS"] && !p1.isJumping;
            p1.isBlocking = keys["KeyE"] && !p1.isCrouching;
            
            if (keys["KeyA"] && p1.x > 15) { p1.x -= p1.speed; p1.direction = -1; }
            if (keys["KeyD"] && p1.x < p2.x - 30) { p1.x += p1.speed; p1.direction = 1; }
            if (keys["KeyW"] && !p1.isJumping && !p1.isCrouching) {
                p1.vy = -13;
                p1.isJumping = true;
            }

            // --- CONTROLES P2 ---
            p2.isCrouching = keys["ArrowDown"] && !p2.isJumping;
            p2.isBlocking = keys["ShiftRight"] && !p2.isCrouching;

            if (keys["ArrowLeft"] && p2.x > p1.x + 30) { p2.x -= p2.speed; p2.direction = -1; }
            if (keys["ArrowRight"] && p2.x < canvas.width - 50) { p2.x += p2.speed; p2.direction = 1; }
            if (keys["ArrowUp"] && !p2.isJumping && !p2.isCrouching) {
                p2.vy = -13;
                p2.isJumping = true;
            }

            // Gravedad P1
            p1.vy += 0.65; p1.y += p1.vy;
            let floorY = p1.isCrouching ? 270 : 240;
            if (p1.y > floorY) { p1.y = floorY; p1.vy = 0; p1.isJumping = false; }

            // Gravedad P2
            p2.vy += 0.65; p2.y += p2.vy;
            let floorY2 = p2.isCrouching ? 270 : 240;
            if (p2.y > floorY2) { p2.y = floorY2; p2.vy = 0; p2.isJumping = false; }

            // --- RENDERIZADO GRÁFICO REALISTA ---
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Fondo y Suelo
            ctx.strokeStyle = "rgba(0, 255, 255, 0.05)";
            for(let i = 0; i < canvas.width; i += 45) {
                ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height); ctx.stroke();
            }

            ctx.fillStyle = "#0f172a";
            ctx.fillRect(0, 320, canvas.width, 60);
            ctx.strokeStyle = "#00ffff";
            ctx.lineWidth = 3;
            ctx.shadowBlur = 15;
            ctx.shadowColor = "#00ffff";
            ctx.beginPath(); ctx.moveTo(0, 320); ctx.lineTo(canvas.width, 320); ctx.stroke();
            ctx.shadowBlur = 0;

            // --- FUNCIÓN PARA DIBUJAR LUCHADOR CON CABEZA, TORSO, BRAZOS Y PIERNAS ---
            function drawFighter(p) {
                ctx.save();
                ctx.shadowBlur = p.isBlocking ? 20 : 10;
                ctx.shadowColor = p.isBlocking ? "#38bdf8" : p.color;

                let h = p.isCrouching ? 50 : p.height;
                let yOffset = p.isCrouching ? 30 : 0;

                // 1. Cabeza
                ctx.fillStyle = "#e2e8f0";
                ctx.fillRect(p.x + 6, p.y + yOffset, 24, 20);
                // Visor / Ojos
                ctx.fillStyle = p.color;
                ctx.fillRect(p.x + (p.direction === 1 ? 18 : 6), p.y + yOffset + 6, 10, 5);

                // 2. Torso (Armadura)
                ctx.fillStyle = p.color;
                ctx.fillRect(p.x + 4, p.y + yOffset + 20, 28, 30);

                // 3. Escudo de Defensa (si está bloqueando)
                if (p.isBlocking) {
                    ctx.strokeStyle = "#38bdf8";
                    ctx.lineWidth = 4;
                    ctx.beginPath();
                    let shieldX = p.direction === 1 ? p.x - 5 : p.x + p.width - 15;
                    ctx.arc(shieldX + 10, p.y + yOffset + 35, 28, 0, Math.PI * 2);
                    ctx.stroke();
                }

                // 4. Brazos / Puños
                ctx.fillStyle = "#cbd5e1";
                if (p.isPunching) {
                    let punchX = p.direction === 1 ? p.x + p.width : p.x - 22;
                    ctx.fillRect(punchX, p.y + yOffset + 26, 22, 10);
                } else {
                    ctx.fillRect(p.x + (p.direction === 1 ? 28 : -10), p.y + yOffset + 24, 18, 10);
                }

                // 5. Piernas separadas
                ctx.fillStyle = "#1e293b";
                if (p.isCrouching) {
                    ctx.fillRect(p.x + 6, p.y + yOffset + 50, 10, 10);
                    ctx.fillRect(p.x + 20, p.y + yOffset + 50, 10, 10);
                } else {
                    ctx.fillRect(p.x + 6, p.y + yOffset + 50, 10, 30);
                    ctx.fillRect(p.x + 20, p.y + yOffset + 50, 10, 30);
                }

                ctx.restore();
            }

            drawFighter(p1);
            drawFighter(p2);

            // Partículas de impacto
            for (let i = particles.length - 1; i >= 0; i--) {
                let pt = particles[i];
                pt.x += pt.vx; pt.y += pt.vy; pt.life--;
                ctx.fillStyle = pt.color;
                ctx.fillRect(pt.x, pt.y, 4, 4);
                if (pt.life <= 0) particles.splice(i, 1);
            }
        }
    </script>
</body>
</html>
"""

# Renderizar en Streamlit
components.html(game_code, height=520)
