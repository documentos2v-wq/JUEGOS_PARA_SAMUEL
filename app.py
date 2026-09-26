import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Cyber Arena 2026 - Streamlit",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ Cyber Arena 2026: Next-Gen Fighting")
st.write("Combate 1v1 de alta tecnología. **P1 (CIBER-RED):** W/A/D para mover/saltar, **F** para golpear. **P2 (CIBER-BLUE):** Flechas para mover/saltar, **L** para golpear.")

# Código HTML, CSS y JS con gráficos futuristas y efectos visuales 2026
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
            width: 560px;
            margin-bottom: 10px;
            font-weight: bold;
            font-size: 14px;
        }
        .player-hud {
            display: flex;
            flex-direction: column;
            width: 250px;
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
            padding: 10px 26px;
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

    <button id="start-btn" onclick="initGame()">⚡ INICIAR COMBATE CIBERNETICO</button>

    <div id="hud-container">
        <div class="player-hud" style="color: #f97316;">
            <span>PLAYER 1 [ CIBER-RED ]</span>
            <div class="health-bar"><div id="hp1" class="health-fill-p1"></div></div>
        </div>
        <div class="player-hud" style="color: #06b6d4; text-align: right;">
            <span>PLAYER 2 [ CIBER-BLUE ]</span>
            <div class="health-bar"><div id="hp2" class="health-fill-p2"></div></div>
        </div>
    </div>
    
    <canvas id="gameCanvas" width="560" height="380" tabindex="1"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let isPlaying = false;
        let gameInterval;
        let keys = {};
        let particles = [];
        let hitEffects = [];

        // Jugador 1
        let p1 = {
            x: 90,
            y: 250,
            width: 45,
            height: 75,
            color: "#f97316",
            speed: 5.5,
            hp: 100,
            isJumping: false,
            vy: 0,
            isPunching: false,
            direction: 1
        };

        // Jugador 2
        let p2 = {
            x: 420,
            y: 250,
            width: 45,
            height: 75,
            color: "#06b6d4",
            speed: 5.5,
            hp: 100,
            isJumping: false,
            vy: 0,
            isPunching: false,
            direction: -1
        };

        window.addEventListener("keydown", (e) => {
            if(["ArrowUp","ArrowDown","ArrowLeft","ArrowRight","KeyW","KeyS","KeyA","KeyD","KeyF","KeyL","Space"].includes(e.code)) {
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
            p1.x = 90; p1.y = 250; p1.hp = 100; p1.vy = 0; p1.isJumping = false;
            p2.x = 420; p2.y = 250; p2.hp = 100; p2.vy = 0; p2.isJumping = false;
            particles = [];
            hitEffects = [];
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
            let sameHeight = Math.abs(attacker.y - defender.y) < 50;

            if (dist < 75 && sameHeight) {
                defender.hp -= 12;
                if (defender.hp < 0) defender.hp = 0;
                updateHUD();

                // Crear ondas de impacto cibernéticas
                hitEffects.push({
                    x: (attacker.x + defender.x) / 2 + 20,
                    y: attacker.y + 30,
                    radius: 10,
                    alpha: 1,
                    color: color
                });

                // Partículas de chispa
                for(let i=0; i<15; i++) {
                    particles.push({
                        x: defender.x + defender.width/2,
                        y: defender.y + 30,
                        vx: (Math.random() - 0.5) * 8,
                        vy: (Math.random() - 0.5) * 8,
                        life: 20,
                        color: color
                    });
                }

                if (defender.hp === 0) {
                    isPlaying = false;
                    let winner = attacker === p1 ? "🏆 ¡PLAYER 1 (CIBER-RED) VICTORIA!" : "🏆 ¡PLAYER 2 (CIBER-BLUE) VICTORIA!";
                    setTimeout(() => {
                        alert(winner);
                        document.getElementById("start-btn").style.display = "block";
                        document.getElementById("start-btn").innerText = "🔄 NUEVA REVANCHA";
                    }, 150);
                }
            }
        }

        function updateHUD() {
            document.getElementById("hp1").style.width = p1.hp + "%";
            document.getElementById("hp2").style.width = p2.hp + "%";
        }

        function updateAndDraw() {
            if (!isPlaying) return;

            // Movimiento P1
            if (keys["KeyA"] && p1.x > 15) { p1.x -= p1.speed; p1.direction = -1; }
            if (keys["KeyD"] && p1.x < p2.x - 25) { p1.x += p1.speed; p1.direction = 1; }
            if (keys["KeyW"] && !p1.isJumping) {
                p1.vy = -13;
                p1.isJumping = true;
            }

            // Movimiento P2
            if (keys["ArrowLeft"] && p2.x > p1.x + 25) { p2.x -= p2.speed; p2.direction = -1; }
            if (keys["ArrowRight"] && p2.x < canvas.width - 60) { p2.x += p2.speed; p2.direction = 1; }
            if (keys["ArrowUp"] && !p2.isJumping) {
                p2.vy = -13;
                p2.isJumping = true;
            }

            // Gravedad
            p1.vy += 0.65; p1.y += p1.vy;
            if (p1.y > 250) { p1.y = 250; p1.vy = 0; p1.isJumping = false; }

            p2.vy += 0.65; p2.y += p2.vy;
            if (p2.y > 250) { p2.y = 250; p2.vy = 0; p2.isJumping = false; }

            // --- RENDERIZADO GRÁFICO AVANZADO 2026 ---
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Rejilla cibernética de fondo
            ctx.strokeStyle = "rgba(0, 255, 255, 0.05)";
            ctx.lineWidth = 1;
            for(let i = 0; i < canvas.width; i += 40) {
                ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, canvas.height); ctx.stroke();
            }

            // Suelo de neón
            ctx.fillStyle = "#0f172a";
            ctx.fillRect(0, 325, canvas.width, 55);
            ctx.strokeStyle = "#00ffff";
            ctx.lineWidth = 3;
            ctx.shadowBlur = 15;
            ctx.shadowColor = "#00ffff";
            ctx.beginPath(); ctx.moveTo(0, 325); ctx.lineTo(canvas.width, 325); ctx.stroke();
            ctx.shadowBlur = 0;

            // --- DIBUJAR LUCHADOR 1 (CIBER-RED HD) ---
            ctx.save();
            ctx.shadowBlur = 12;
            ctx.shadowColor = p1.color;
            ctx.fillStyle = p1.color;
            // Cuerpo acorazado
            ctx.fillRect(p1.x, p1.y + 15, p1.width, p1.height - 15);
            // Casco cibernético
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(p1.x + 5, p1.y, p1.width - 10, 18);
            ctx.fillStyle = "#ef4444";
            ctx.fillRect(p1.x + 10, p1.y + 5, p1.width - 20, 6); // Visor
            // Puño en ataque
            if (p1.isPunching) {
                ctx.fillStyle = "#ffedd5";
                let px = p1.direction === 1 ? p1.x + p1.width : p1.x - 22;
                ctx.fillRect(px, p1.y + 25, 22, 14);
            }
            ctx.restore();

            // --- DIBUJAR LUCHADOR 2 (CIBER-BLUE HD) ---
            ctx.save();
            ctx.shadowBlur = 12;
            ctx.shadowColor = p2.color;
            ctx.fillStyle = p2.color;
            // Cuerpo acorazado
            ctx.fillRect(p2.x, p2.y + 15, p2.width, p2.height - 15);
            // Casco cibernético
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(p2.x + 5, p2.y, p2.width - 10, 18);
            ctx.fillStyle = "#3b82f6";
            ctx.fillRect(p2.x + 10, p2.y + 5, p2.width - 20, 6); // Visor
            // Puño en ataque
            if (p2.isPunching) {
                ctx.fillStyle = "#e0f2fe";
                let px2 = p2.direction === 1 ? p2.x + p2.width : p2.x - 22;
                ctx.fillRect(px2, p2.y + 25, 22, 14);
            }
            ctx.restore();

            // Efectos de ondas de golpe
            for (let i = hitEffects.length - 1; i >= 0; i--) {
                let he = hitEffects[i];
                he.radius += 3;
                he.alpha -= 0.05;
                ctx.strokeStyle = he.color;
                ctx.lineWidth = 3;
                ctx.globalAlpha = he.alpha;
                ctx.beginPath();
                ctx.arc(he.x, he.y, he.radius, 0, Math.PI * 2);
                ctx.stroke();
                ctx.globalAlpha = 1.0;
                if (he.alpha <= 0) hitEffects.splice(i, 1);
            }

            // Partículas de combate
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
