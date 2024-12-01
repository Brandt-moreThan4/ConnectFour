const columns = 7;
const rows = 6;
let currentPlayer = 'red';
let board = Array(rows).fill(null).map(() => Array(columns).fill(null));
let player1Type = 'human';
let player2Type = 'human';

// Display initial status
document.getElementById('status').textContent = `Select game settings to start.`;

// Attach event listener to the "Start Game" button
document.getElementById('start-game').addEventListener('click', () => {
    // Get selected player types
    player1Type = document.getElementById('player1').value;
    player2Type = document.getElementById('player2').value;

    // Enable the game board
    document.getElementById('board').classList.remove('disabled');

    // Hide the settings section
    document.getElementById('settings').style.display = 'none';

    // Display initial status
    document.getElementById('status').textContent = `${currentPlayer.toUpperCase()}'s turn`;
});

// Attach click event listeners to all cells
const cells = document.querySelectorAll('.cell');
cells.forEach(cell => {
    cell.addEventListener('click', handleCellClick);
});

function handleCellClick(event) {
    // Only allow player moves if the board is active
    if (document.getElementById('board').classList.contains('disabled')) return;

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
                displayWinMessage(currentPlayer);
                disableBoard();
            } else {
                switchTurns();
            }
            break;
        }
    }
}

function switchTurns() {
    if (currentPlayer === 'red') {
        currentPlayer = 'black';
        document.getElementById('status').textContent = `BLACK's turn`;

        if (player2Type !== 'human') {
            // Call bot logic for Player 2
            getBotMove(board, 'black', player2Type);
        }
    } else {
        currentPlayer = 'red';
        document.getElementById('status').textContent = `RED's turn`;

        if (player1Type !== 'human') {
            // Call bot logic for Player 1
            getBotMove(board, 'red', player1Type);
        }
    }
}

async function getBotMove(board, player, difficulty) {
    try {
        // Simulate bot behavior or call an API
        const response = await fetch('api/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                board: board,
                player: player,
                difficulty: difficulty,
            }),
        });

        const data = await response.json();
        const botCol = data.column;

        // Handle the bot's move
        if (botCol !== null) {
            for (let r = rows - 1; r >= 0; r--) {
                if (!board[r][botCol]) {
                    board[r][botCol] = player;

                    const cell = document.querySelector(`.cell[data-row='${r}'][data-col='${botCol}']`);
                    cell.classList.add('taken', player);

                    if (checkWin(r, botCol)) {
                        displayWinMessage(player);
                        disableBoard();
                    } else {
                        switchTurns();
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

function displayWinMessage(winner) {
    const statusElement = document.getElementById('status');
    statusElement.textContent = `🎉 ${winner.toUpperCase()} WINS! 🎉`;

    statusElement.style.color = winner === 'red' ? 'red' : 'black';
    statusElement.style.fontSize = '2rem';
    statusElement.style.fontWeight = 'bold';
    statusElement.style.textShadow = `0 0 10px ${winner === 'red' ? 'red' : 'black'}, 
                                      0 0 20px ${winner === 'red' ? 'red' : 'black'}`;
    statusElement.classList.add('win-flash');
}

function disableBoard() {
    cells.forEach(cell => cell.removeEventListener('click', handleCellClick));
}

function checkWin(row, col) {
    function count(directionRow, directionCol) {
        let r = row + directionRow;
        let c = col + directionCol;
        let count = 0;
        const positions = [[row, col]];

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

    const directions = [
        [0, 1],
        [1, 0],
        [1, 1],
        [1, -1],
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

function highlightWinningCells(winningCells) {
    winningCells.forEach(([r, c]) => {
        const cell = document.querySelector(`.cell[data-row='${r}'][data-col='${c}']`);
        if (cell) {
            cell.classList.add('winning-cell');
        }
    });
}

function resetGame() {
    board = Array(rows).fill(null).map(() => Array(columns).fill(null));
    currentPlayer = 'red';
    document.getElementById('status').textContent = 'Select game settings to start.';
    document.getElementById('settings').style.display = 'block';
    document.getElementById('board').classList.add('disabled');
    cells.forEach(cell => {
        cell.className = 'cell';
        cell.addEventListener('click', handleCellClick);
    });
}
