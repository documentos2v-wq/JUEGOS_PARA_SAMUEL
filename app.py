import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Street Combat 2026 - Streamlit",
    page_icon="🥊",
    layout="centered"
)

st.title("🥊 Street Combat Arena 2026")
st.write("Juego de pelea clásico 1v1. **Jugador 1 (Rojo):** W/A/D para mover/saltar, **F** para golpear. **Jugador 2 (Azul):** Flechas para mover/saltar, **L** para golpear.")

# Código HTML, CSS y JS del juego de pelea
game_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {
            background-color: #0b0f19;
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
            width: 500px;
            margin-bottom: 8px;
            font-weight: bold;
            font-size: 14px;
        }
        .health-bar {
            width: 200px;
            height: 20px;
            background: #334155;
            border: 2px solid #fff;
            border-radius: 4px;
            overflow: hidden;
            display: inline-block;
            vertical-align: middle;
        }
        .health-fill-p1 {
            width: 100%;
            height: 100%;
            background: #ef4444;
            transition: width 0.1s;
        }
        .health-fill-p2 {
            width: 100%;
            height: 100%;
            background: #3b82f6;
            transition: width 0.1s;
        }
        #start-btn {
            background: linear-gradient(45deg, #ef4444, #f59e0b);
            color: #fff;
            border: none;
            padding: 8px 22px;
            font-weight: bold;
            font-size: 15px;
            border-radius: 20px;
            cursor: pointer;
            box-shadow: 0 0 15px rgba(239,68,68,0.6);
            margin-bottom: 10px;
            transition: 0.2s;
        }
        #start-btn:hover {
            transform: scale(1.05);
        }
        canvas {
            border: 3px solid #f59e0b;
            background: linear-gradient(to bottom, #1e1b4b, #0f172a);
            box-shadow: 0 0 30px rgba(245, 158, 11, 0.3);
            border-radius: 8px;
            outline: none;
        }
    </style>
</head>
<body>

    <button id="start-btn" onclick="initGame()">¡INICIAR COMBATE!</button>

    <div id="hud-container">
        <div>P1 (Rojo): <div class="health-bar"><div id="hp1" class="health-fill-p1"></div></div></div>
        <div>P2 (Azul): <div class="health-bar"><div id="hp2" class="health-fill-p2"></div></div></div>
    </div>
    
    <canvas id="gameCanvas" width="500" height="350" tabindex="1"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        let isPlaying = false;
        let gameInterval;
        let keys = {};

        // Jugador 1
        let p1 = {
            x: 80,
            y: 240,
            width: 40,
            height: 70,
            color: "#ef4444",
            speed: 5,
            hp: 100,
            isJumping: false,
            vy: 0,
            isPunching: false,
            direction: 1 // 1 derecha, -1 izquierda
        };

        // Jugador 2
        let p2 = {
            x: 380,
            y: 240,
            width: 40,
            height: 70,
            color: "#3b82f6",
            speed: 5,
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

            // Golpes directos
            if(e.code === "KeyF" && isPlaying) attack(p1, p2);
            if(e.code === "KeyL" && isPlaying) attack(p2, p1);
        });

        window.addEventListener("keyup", (e) => {
            keys[e.code] = false;
        });

        function initGame() {
            p1.x = 80; p1.y = 240; p1.hp = 100; p1.vy = 0; p1.isJumping = false;
            p2.x = 380; p2.y = 240; p2.hp = 100; p2.vy = 0; p2.isJumping = false;
            isPlaying = true;
            document.getElementById("start-btn").style.display = "none";
            canvas.focus();

            if(gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(updateAndDraw, 1000 / 60);
        }

        function attack(attacker, defender) {
            attacker.isPunching = true;
            setTimeout(() => { attacker.isPunching = false; }, 150);

            // Rango de golpe
            let dist = Math.abs((attacker.x + attacker.width/2) - (defender.x + defender.width/2));
            let sameHeight = Math.abs(attacker.y - defender.y) < 40;

            if (dist < 65 && sameHeight) {
                defender.hp -= 10;
                if (defender.hp < 0) defender.hp = 0;
                updateHUD();

                if (defender.hp === 0) {
                    isPlaying = false;
                    let winner = attacker === p1 ? "¡Jugador 1 (Rojo) GANA!" : "¡Jugador 2 (Azul) GANA!";
                    setTimeout(() => {
                        alert("🏆 " + winner);
                        document.getElementById("start-btn").style.display = "block";
                        document.getElementById("start-btn").innerText = "REVANCHA";
                    }, 100);
                }
            }
        }

        function updateHUD() {
            document.getElementById("hp1").style.width = p1.hp + "%";
            document.getElementById("hp2").style.width = p2.hp + "%";
        }

        function updateAndDraw() {
            if (!isPlaying) return;

            // --- CONTROLES JUGADOR 1 (W, A, D, F) ---
            if (keys["KeyA"] && p1.x > 10) { p1.x -= p1.speed; p1.direction = -1; }
            if (keys["KeyD"] && p1.x < p2.x - 20) { p1.x += p1.speed; p1.direction = 1; }
            if (keys["KeyW"] && !p1.isJumping) {
                p1.vy = -12;
                p1.isJumping = true;
            }

            // --- CONTROLES JUGADOR 2 (Flechas, L) ---
            if (keys["ArrowLeft"] && p2.x > p1.x + 20) { p2.x -= p2.speed; p2.direction = -1; }
            if (keys["ArrowRight"] && p2.x < canvas.width - 50) { p2.x += p2.speed; p2.direction = 1; }
            if (keys["ArrowUp"] && !p2.isJumping) {
                p2.vy = -12;
                p2.isJumping = true;
            }

            // Gravedad P1
            p1.vy += 0.6;
            p1.y += p1.vy;
            if (p1.y > 240) { p1.y = 240; p1.vy = 0; p1.isJumping = false; }

            // Gravedad P2
            p2.vy += 0.6;
            p2.y += p2.vy;
            if (p2.y > 240) { p2.y = 240; p2.vy = 0; p2.isJumping = false; }

            // --- RENDERIZADO DEL ESCENARIO DE PELEA ---
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Suelo de la arena
            ctx.fillStyle = "#334155";
            ctx.fillRect(0, 310, canvas.width, 40);
            ctx.fillStyle = "#f59e0b";
            ctx.fillRect(0, 310, canvas.width, 5);

            // Dibujar Jugador 1 (Rojo)
            ctx.fillStyle = p1.color;
            ctx.fillRect(p1.x, p1.y, p1.width, p1.height);
            // Cabeza P1
            ctx.fillStyle = "#fca5a5";
            ctx.fillRect(p1.x + 8, p1.y - 15, 24, 20);
            // Puño si está atacando
            if (p1.isPunching) {
                ctx.fillStyle = "#ef4444";
                let punchX = p1.direction === 1 ? p1.x + p1.width : p1.x - 20;
                ctx.fillRect(punchX, p1.y + 20, 20, 12);
            }

            // Dibujar Jugador 2 (Azul)
            ctx.fillStyle = p2.color;
            ctx.fillRect(p2.x, p2.y, p2.width, p2.height);
            // Cabeza P2
            ctx.fillStyle = "#93c5fd";
            ctx.fillRect(p2.x + 8, p2.y - 15, 24, 20);
            // Puño si está atacando
            if (p2.isPunching) {
                ctx.fillStyle = "#3b82f6";
                let punchX2 = p2.direction === 1 ? p2.x + p2.width : p2.x - 20;
                ctx.fillRect(punchX2, p2.y + 20, 20, 12);
            }
        }
    </script>
</body>
</html>
"""

# Renderizar en Streamlit
components.html(game_code, height=480)
