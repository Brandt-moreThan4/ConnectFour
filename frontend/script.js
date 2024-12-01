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
