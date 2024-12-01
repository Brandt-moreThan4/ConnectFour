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
    <div id="board">
        <!-- Manually creating a 6x7 board (6 rows, 7 columns) -->
        <!-- Row 1 -->
        <div class="cell" data-row="0" data-col="0"></div>
        <div class="cell" data-row="0" data-col="1"></div>
        <div class="cell" data-row="0" data-col="2"></div>
        <div class="cell" data-row="0" data-col="3"></div>
        <div class="cell" data-row="0" data-col="4"></div>
        <div class="cell" data-row="0" data-col="5"></div>
        <div class="cell" data-row="0" data-col="6"></div>
        <!-- Row 2 -->
        <div class="cell" data-row="1" data-col="0"></div>
        <div class="cell" data-row="1" data-col="1"></div>
        <div class="cell" data-row="1" data-col="2"></div>
        <div class="cell" data-row="1" data-col="3"></div>
        <div class="cell" data-row="1" data-col="4"></div>
        <div class="cell" data-row="1" data-col="5"></div>
        <div class="cell" data-row="1" data-col="6"></div>
        <!-- Row 3 -->
        <div class="cell" data-row="2" data-col="0"></div>
        <div class="cell" data-row="2" data-col="1"></div>
        <div class="cell" data-row="2" data-col="2"></div>
        <div class="cell" data-row="2" data-col="3"></div>
        <div class="cell" data-row="2" data-col="4"></div>
        <div class="cell" data-row="2" data-col="5"></div>
        <div class="cell" data-row="2" data-col="6"></div>
        <!-- Row 4 -->
        <div class="cell" data-row="3" data-col="0"></div>
        <div class="cell" data-row="3" data-col="1"></div>
        <div class="cell" data-row="3" data-col="2"></div>
        <div class="cell" data-row="3" data-col="3"></div>
        <div class="cell" data-row="3" data-col="4"></div>
        <div class="cell" data-row="3" data-col="5"></div>
        <div class="cell" data-row="3" data-col="6"></div>
        <!-- Row 5 -->
        <div class="cell" data-row="4" data-col="0"></div>
        <div class="cell" data-row="4" data-col="1"></div>
        <div class="cell" data-row="4" data-col="2"></div>
        <div class="cell" data-row="4" data-col="3"></div>
        <div class="cell" data-row="4" data-col="4"></div>
        <div class="cell" data-row="4" data-col="5"></div>
        <div class="cell" data-row="4" data-col="6"></div>
        <!-- Row 6 -->
        <div class="cell" data-row="5" data-col="0"></div>
        <div class="cell" data-row="5" data-col="1"></div>
        <div class="cell" data-row="5" data-col="2"></div>
        <div class="cell" data-row="5" data-col="3"></div>
        <div class="cell" data-row="5" data-col="4"></div>
        <div class="cell" data-row="5" data-col="5"></div>
        <div class="cell" data-row="5" data-col="6"></div>
    </div>
    <p id="status"></p>
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
                document.getElementById('status').textContent = `${currentPlayer.toUpperCase()} wins!`;
                disableBoard();
            } else {
                // Switch to the bot's turn
                currentPlayer = 'yellow';
                document.getElementById('status').textContent = `Bot's turn...`;

                // Call function to get the bot's move
                getBotMove(board);
            }
            break;
        }
    }
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
                        document.getElementById('status').textContent = `${currentPlayer.toUpperCase()} wins!`;
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

        // Continue counting while within board bounds and pieces match the current player
        while (
            r >= 0 &&
            r < rows &&
            c >= 0 &&
            c < columns &&
            board[r][c] === currentPlayer
        ) {
            count++;
            r += directionRow; // Move in the specified row direction
            c += directionCol; // Move in the specified column direction
        }
        return count; // Return the count of matching pieces
    }

    // Check for four-in-a-row in various directions
    return (
        count(0, 1) + count(0, -1) >= 3 || // Horizontal check (left + right)
        count(1, 0) + count(-1, 0) >= 3 || // Vertical check (up + down)
        count(1, 1) + count(-1, -1) >= 3 || // Diagonal \ (bottom-left to top-right)
        count(1, -1) + count(-1, 1) >= 3   // Diagonal / (bottom-right to top-left)
    );
}

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\frontend\style.css

```css
body {
    font-family: Arial, sans-serif;
    text-align: center;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
}

h1 {
    margin-top: 20px;
}

#board {
    display: grid;
    grid-template-columns: repeat(7, 50px); /* 7 columns */
    grid-gap: 5px;
    margin: 20px auto;
    max-width: 400px;
    border: 2px solid #000;
}

.cell {
    width: 50px;
    height: 50px;
    background-color: #f1f1f1;
    border: 1px solid #ccc;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

.cell.taken {
    cursor: not-allowed;
}

.cell.red {
    background-color: red;
}

.cell.yellow {
    background-color: yellow;
}

#status {
    margin-top: 15px;
    font-size: 18px;
}

```

