# Project Master File

## Project Structure

```
├── index.html
├── script.js
└── style.css
```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\frontend\index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connect 4 Game</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Connect 4</h1>
    <h2 class="subheader">A Brandt Green Production</h2>     
    <div id="board">
        <!-- Dynamically creating a 6x7 board -->
        <div class="cell" data-row="0" data-col="0"></div>
        <div class="cell" data-row="0" data-col="1"></div>
        <div class="cell" data-row="0" data-col="2"></div>
        <div class="cell" data-row="0" data-col="3"></div>
        <div class="cell" data-row="0" data-col="4"></div>
        <div class="cell" data-row="0" data-col="5"></div>
        <div class="cell" data-row="0" data-col="6"></div>
        <!-- Add rows 1 through 5 here -->
        <div class="cell" data-row="1" data-col="0"></div>
        <div class="cell" data-row="1" data-col="1"></div>
        <div class="cell" data-row="1" data-col="2"></div>
        <div class="cell" data-row="1" data-col="3"></div>
        <div class="cell" data-row="1" data-col="4"></div>
        <div class="cell" data-row="1" data-col="5"></div>
        <div class="cell" data-row="1" data-col="6"></div>
        <div class="cell" data-row="2" data-col="0"></div>
        <div class="cell" data-row="2" data-col="1"></div>
        <div class="cell" data-row="2" data-col="2"></div>
        <div class="cell" data-row="2" data-col="3"></div>
        <div class="cell" data-row="2" data-col="4"></div>
        <div class="cell" data-row="2" data-col="5"></div>
        <div class="cell" data-row="2" data-col="6"></div>
        <div class="cell" data-row="3" data-col="0"></div>
        <div class="cell" data-row="3" data-col="1"></div>
        <div class="cell" data-row="3" data-col="2"></div>
        <div class="cell" data-row="3" data-col="3"></div>
        <div class="cell" data-row="3" data-col="4"></div>
        <div class="cell" data-row="3" data-col="5"></div>
        <div class="cell" data-row="3" data-col="6"></div>
        <div class="cell" data-row="4" data-col="0"></div>
        <div class="cell" data-row="4" data-col="1"></div>
        <div class="cell" data-row="4" data-col="2"></div>
        <div class="cell" data-row="4" data-col="3"></div>
        <div class="cell" data-row="4" data-col="4"></div>
        <div class="cell" data-row="4" data-col="5"></div>
        <div class="cell" data-row="4" data-col="6"></div>
        <div class="cell" data-row="5" data-col="0"></div>
        <div class="cell" data-row="5" data-col="1"></div>
        <div class="cell" data-row="5" data-col="2"></div>
        <div class="cell" data-row="5" data-col="3"></div>
        <div class="cell" data-row="5" data-col="4"></div>
        <div class="cell" data-row="5" data-col="5"></div>
        <div class="cell" data-row="5" data-col="6"></div>
    </div>
    <p id="status"></p>
    <button id="reset" onclick="window.location.reload()">Reset Game</button>
    <script src="script.js"></script>
</body>
</html>

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\frontend\script.js

```js
const columns = 7;
const rows = 6;
let currentPlayer = 'red';
let board = Array(rows).fill(null).map(() => Array(columns).fill(null));

// Display initial status
document.getElementById('status').textContent = `${currentPlayer.toUpperCase()}'s turn`;

// Attach click event listeners to all cells
const cells = document.querySelectorAll('.cell');
cells.forEach(cell => {
    cell.addEventListener('click', handleCellClick);
});

function handleCellClick(event) {
    // Only allow player moves if it's their turn
    if (currentPlayer !== 'red') return;

    const col = parseInt(event.target.dataset.col);

    // Find the lowest available row in the selected column
    for (let r = rows - 1; r >= 0; r--) {
        if (!board[r][col]) {
            // Update the board state
            board[r][col] = currentPlayer;

            // Find the cell element in the DOM using data attributes
            const cell = document.querySelector(`.cell[data-row='${r}'][data-col='${col}']`);
            cell.classList.add('taken', currentPlayer);

            // Check if the move results in a win
            if (checkWin(r, col)) {
                // document.getElementById('status').textContent = `${currentPlayer.toUpperCase()} wins!`;
                displayWinMessage(currentPlayer);
                disableBoard();
            } else {
                // Switch to the bot's turn
                currentPlayer = 'black';
                document.getElementById('status').textContent = `Bot's turn...`;

                // Call function to get the bot's move
                getBotMove(board);
            }
            break;
        }
    }
}

function displayWinMessage(winner) {
    const statusElement = document.getElementById('status');
    statusElement.textContent = `🎉 !${winner.toUpperCase()} WINS! 🎉`;

    // Add vibrant styling
    statusElement.style.color = winner === 'red' ? 'red' : 'black';
    statusElement.style.fontSize = '2rem';
    statusElement.style.fontWeight = 'bold';
    statusElement.style.textShadow = `0 0 10px ${winner === 'red' ? 'red' : 'black'}, 
                                      0 0 20px ${winner === 'red' ? 'red' : 'black'}`;

    // Add flashing animation
    statusElement.classList.add('win-flash');
}


async function getBotMove(board) {
    try {
        // Make a request to the backend to get the bot's move
        const response = await fetch('api/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                board: board,
                player: 'bot', // Optional, if needed by your backend logic
            }),
        });

        const data = await response.json();
        const botCol = data.column;

        // Handle the bot's move
        if (botCol !== null) {
            for (let r = rows - 1; r >= 0; r--) {
                if (!board[r][botCol]) {
                    // Update the board state
                    board[r][botCol] = currentPlayer;

                    // Find the cell element in the DOM
                    const cell = document.querySelector(`.cell[data-row='${r}'][data-col='${botCol}']`);
                    cell.classList.add('taken', currentPlayer);

                    // Check if the bot's move results in a win
                    if (checkWin(r, botCol)) {
                        // document.getElementById('status').textContent = `${currentPlayer.toUpperCase()} wins!`;
                        displayWinMessage(currentPlayer);
                        disableBoard();
                    } else {
                        // Switch back to the player's turn
                        currentPlayer = 'red';
                        document.getElementById('status').textContent = `${currentPlayer.toUpperCase()}'s turn`;
                    }
                    break;
                }
            }
        }
    } catch (error) {
        console.error('Error getting bot move:', error);
        document.getElementById('status').textContent = 'Error getting bot move. Try again.';
    }
}

function disableBoard() {
    cells.forEach(cell => cell.removeEventListener('click', handleCellClick));
}


function checkWin(row, col) {
    // Helper function to count consecutive pieces in a specified direction
    function count(directionRow, directionCol) {
        let r = row + directionRow;
        let c = col + directionCol;
        let count = 0;
        const positions = [[row, col]];

        // Continue counting while within board bounds and pieces match the current player
        while (
            r >= 0 &&
            r < rows &&
            c >= 0 &&
            c < columns &&
            board[r][c] === currentPlayer
        ) {
            count++;
            positions.push([r, c]);
            r += directionRow;
            c += directionCol;
        }
        return { count, positions };
    }

    // Check for four-in-a-row in various directions
    const directions = [
        [0, 1],  // Horizontal right
        [1, 0],  // Vertical down
        [1, 1],  // Diagonal \
        [1, -1]  // Diagonal /
    ];

    for (const [dRow, dCol] of directions) {
        const forward = count(dRow, dCol);
        const backward = count(-dRow, -dCol);

        if (forward.count + backward.count >= 3) {
            const winningCells = [...forward.positions, ...backward.positions.slice(1)];
            highlightWinningCells(winningCells);
            return true;
        }
    }

    return false;
}

// Highlight the winning cells
function highlightWinningCells(winningCells) {
    winningCells.forEach(([r, c]) => {
        const cell = document.querySelector(`.cell[data-row='${r}'][data-col='${c}']`);
        if (cell) {
            cell.classList.add('winning-cell');
        }
    });
}

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\frontend\style.css

```css
/* General Reset */
* {
    box-sizing: border-box;
}

/* General styling for the game */
body {
    font-family: Arial, sans-serif;
    text-align: center;
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #87CEFA, #FFB6C1); /* Gradient background */
}

h1 {
    font-family: 'Comic Sans MS', cursive, sans-serif;
    font-size: 3rem;
    color: #00008B;
    text-shadow: 2px 2px #FFD700; /* Gold shadow */
    margin-top: 20px;
}

/* Subheader styling */
.subheader {
    font-family: 'Arial', sans-serif;
    font-size: 1.2rem;
    font-weight: bold;
    font-style: italic;
    color: #555;
    margin-top: -10px;
    margin-bottom: 20px;
    text-shadow: 1px 1px #ddd;
}

/* Board styling */
#board {
    display: grid;
    grid-template-columns: repeat(7, 1fr); /* Flexible columns */
    grid-gap: 5px;
    margin: 30px auto;
    width: 95%; /* Dynamic width for responsiveness */
    max-width: 500px; /* Limit max width on larger screens */
    border: 4px solid #000;
    border-radius: 10px;
    background-color: #FFD700; /* Golden board */
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    padding: 5px;
}

/* Cell styling */
.cell {
    width: 100%; /* Scale dynamically with grid columns */
    height: 0; /* Use padding to create square cells */
    padding-bottom: 100%; /* Ensures square aspect ratio */
    background: radial-gradient(circle, #ffffff, #d3d3d3); /* Glossy effect */
    border: 1px solid #000;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: transform 0.2s, background 0.2s;
}

.cell:hover {
    transform: scale(1.1); /* Hover zoom-in effect */
    background: radial-gradient(circle, #d3d3d3, #ffffff); /* Reverse glossy effect */
}

.cell.red {
    background: radial-gradient(circle, #ff4d4d, #b30000); /* Red glossy */
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
}

.cell.yellow {
    background: radial-gradient(circle, #ffea4d, #c7a000); /* Yellow glossy */
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
}

.cell.black {
    background: radial-gradient(circle, #000000, #444444); /* Black glossy effect */
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.5);
}

/* Highlight winning cells */
.winning-cell {
    border: 4px solid blue;
    box-shadow: 0 0 10px blue, 0 0 20px blue, 0 0 30px blue;
    animation: pulse 1s infinite;
}

/* Pulsating effect for winning cells */
@keyframes pulse {
    0% {
        transform: scale(1);
        box-shadow: 0 0 10px blue, 0 0 20px blue, 0 0 30px blue;
    }
    50% {
        transform: scale(1.1);
        box-shadow: 0 0 20px blue, 0 0 30px blue, 0 0 40px blue;
    }
    100% {
        transform: scale(1);
        box-shadow: 0 0 10px blue, 0 0 20px blue, 0 0 30px blue;
    }
}

/* Reset button styling */
#reset {
    margin-top: 20px;
    padding: 10px 20px;
    font-size: 18px;
    font-weight: bold;
    color: #fff;
    background-color: #4CAF50;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

#reset:hover {
    background-color: #45a049;
}

/* Responsive Design for Small Screens */
@media (max-width: 600px) {
    h1 {
        font-size: 2rem;
    }

    .subheader {
        font-size: 1rem;
    }

    #board {
        width: 100%;
        max-width: none;
    }

    .cell {
        border-width: 0.5px;
    }
}

```

