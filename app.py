import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Dragon Ball Sudoku Z - Streamlit",
    page_icon="🐉",
    layout="centered"
)

st.title("🐉 Dragon Ball Sudoku: ¡Entrenamiento Mental de Kaiō-sama!")
st.write("Resuelve el Sudoku de 9x9 para dominar tu Ki. Llena las celdas vacías del 1 al 9 sin repetir números en filas, columnas ni bloques de 3x3.")

# Código HTML, CSS y JS del Sudoku con temática Dragon Ball
game_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <style>
        body {
            background-color: #0d1117;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 10px;
        }
        .container {
            background: linear-gradient(135deg, #1f2937, #111827);
            border: 3px solid #f59e0b;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 0 25px rgba(245, 158, 11, 0.4);
            text-align: center;
        }
        .header-info {
            display: flex;
            justify-content: space-between;
            font-size: 14px;
            font-weight: bold;
            color: #f59e0b;
            margin-bottom: 10px;
        }
        table {
            border-collapse: collapse;
            margin: 0 auto 15px auto;
            border: 3px solid #f59e0b;
        }
        td {
            border: 1px solid #4b5563;
            width: 38px;
            height: 38px;
            text-align: center;
        }
        /* Bordes gruesos para los bloques de 3x3 */
        tr:nth-child(3) td, tr:nth-child(6) td {
            border-bottom: 3px solid #f59e0b;
        }
        td:nth-child(3), td:nth-child(6) {
            border-right: 3px solid #f59e0b;
        }
        input.sudoku-cell {
            width: 100%;
            height: 100%;
            background: #1f2937;
            color: #38bdf8;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            border: none;
            outline: none;
        }
        input.sudoku-cell:focus {
            background: #374151;
            color: #f43f5e;
        }
        input.sudoku-cell.given {
            color: #fde047;
            background: #111827;
        }
        .btn-group {
            display: flex;
            gap: 10px;
            justify-content: center;
        }
        .db-btn {
            background: linear-gradient(45deg, #f59e0b, #ef4444);
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 13px;
            border-radius: 20px;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
            transition: 0.2s;
        }
        .db-btn:hover {
            transform: scale(1.05);
            background: linear-gradient(45deg, #fbbf24, #dc2626);
        }
        #message {
            margin-top: 10px;
            font-size: 14px;
            font-weight: bold;
            color: #38bdf8;
            min-height: 20px;
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="header-info">
            <div>Dificultad: Nivel Super Saiyan</div>
            <div id="status">Concentra tu Ki...</div>
        </div>

        <div id="sudoku-board"></div>

        <div class="btn-group">
            <button class="db-btn" onclick="checkSolution()">¡LIBERAR PODER (VERIFICAR)!</button>
            <button class="db-btn" onclick="resetBoard()">REINICIAR TABLERO</button>
        </div>

        <div id="message"></div>
    </div>

    <script>
        // Tablero de ejemplo válido para Sudoku (0 representa celdas vacías)
        const initialBoard = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ];

        let currentBoard = JSON.parse(JSON.stringify(initialBoard));

        function renderBoard() {
            const boardContainer = document.getElementById("sudoku-board");
            boardContainer.innerHTML = "";
            let table = document.createElement("table");

            for (let r = 0; r < 9; r++) {
                let row = document.createElement("tr");
                for (let c = 0; c < 9; c++) {
                    let cell = document.createElement("td");
                    let input = document.createElement("input");
                    input.type = "text";
                    input.maxLength = 1;
                    input.className = "sudoku-cell";

                    if (initialBoard[r][c] !== 0) {
                        input.value = initialBoard[r][c];
                        input.disabled = true;
                        input.classList.add("given");
                    } else {
                        input.value = currentBoard[r][c] !== 0 ? currentBoard[r][c] : "";
                        input.oninput = (e) => {
                            let val = parseInt(e.target.value);
                            if (isNaN(val) || val < 1 || val > 9) {
                                e.target.value = "";
                                currentBoard[r][c] = 0;
                            } else {
                                currentBoard[r][c] = val;
                            }
                        };
                    }
                    cell.appendChild(input);
                    row.appendChild(cell);
                }
                table.appendChild(row);
            }
            boardContainer.appendChild(table);
        }

        function checkSolution() {
            // Recoger valores actuales de los inputs
            const inputs = document.querySelectorAll(".sudoku-cell");
            let index = 0;
            let isComplete = true;

            for (let r = 0; r < 9; r++) {
                for (let c = 0; c < 9; c++) {
                    if (initialBoard[r][c] === 0) {
                        let val = parseInt(inputs[index].value);
                        if (isNaN(val)) {
                            isComplete = false;
                        }
                        currentBoard[r][c] = isNaN(val) ? 0 : val;
                    }
                    index++;
                }
            }

            let msg = document.getElementById("message");
            if (!isComplete) {
                msg.style.color = "#f43f5e";
                msg.innerText = "⚠️ ¡Aún quedan celdas vacías! ¡El entrenamiento no ha terminado!";
                return;
            }

            // Validar reglas básicas de filas, columnas y bloques
            if (isValidSudoku(currentBoard)) {
                msg.style.color = "#22c55e";
                msg.innerText = "🐉 ¡Increíble! ¡Has alcanzado el estado Super Saiyan Blue perfecto!";
            } else {
                msg.style.color = "#f43f5e";
                msg.innerText = "❌ ¡Hay errores en el flujo de Ki! Revisa los números repetidos.";
            }
        }

        function isValidSudoku(board) {
            for (let i = 0; i < 9; i++) {
                let rowSet = new Set();
                let colSet = new Set();
                let boxSet = new Set();

                for (let j = 0; j < 9; j++) {
                    // Fila
                    let rVal = board[i][j];
                    if (rVal !== 0) {
                        if (rowSet.has(rVal)) return false;
                        rowSet.add(rVal);
                    }
                    // Columna
                    let cVal = board[j][i];
                    if (cVal !== 0) {
                        if (colSet.has(cVal)) return false;
                        colSet.add(cVal);
                    }
                    // Bloque 3x3
                    let rowIndex = 3 * Math.floor(i / 3) + Math.floor(j / 3);
                    let colIndex = 3 * (i % 3) + (j % 3);
                    let bVal = board[rowIndex][colIndex];
                    if (bVal !== 0) {
                        if (boxSet.has(bVal)) return false;
                        boxSet.add(bVal);
                    }
                }
            }
            return true;
        }

        function resetBoard() {
            currentBoard = JSON.parse(JSON.stringify(initialBoard));
            document.getElementById("message.innerText") = "";
            renderBoard();
            document.getElementById("message").innerText = "🔄 Tablero reiniciado. ¡Vuelve a concentrarte!";
        }

        renderBoard();
    </script>
</body>
</html>
"""

# Renderizar en Streamlit
components.html(game_code, height=580)
