console.log('Script loaded'); // Add this to the top of script.js


const columns = 7;
const rows = 6;
let currentPlayer = 'red';
let board = [];

// Create the game board
const boardElement = document.getElementById('board');
function createBoard() {
    board = Array(rows).fill(null).map(() => Array(columns).fill(null));
    boardElement.innerHTML = '';
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < columns; c++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.row = r;
            cell.dataset.col = c;
            cell.addEventListener('click', handleCellClick);
            boardElement.appendChild(cell);
        }
    }
}

function handleCellClick(event) {
    const col = parseInt(event.target.dataset.col);
    for (let r = rows - 1; r >= 0; r--) {
        if (!board[r][col]) {
            board[r][col] = currentPlayer;
            const cell = document.querySelector(`.cell[data-row='${r}'][data-col='${col}']`);
            cell.classList.add('taken', currentPlayer);
            if (checkWin(r, col)) {
                document.getElementById('status').textContent = `${currentPlayer.toUpperCase()} wins!`;
                disableBoard();
            } else {
                currentPlayer = currentPlayer === 'red' ? 'yellow' : 'red';
                document.getElementById('status').textContent = `${currentPlayer.toUpperCase()}'s turn`;
            }
            break;
        }
    }
}

function disableBoard() {
    const cells = document.querySelectorAll('.cell');
    cells.forEach(cell => cell.removeEventListener('click', handleCellClick));
}

function checkWin(row, col) {
    function count(directionRow, directionCol) {
        let r = row + directionRow;
        let c = col + directionCol;
        let count = 0;
        while (
            r >= 0 &&
            r < rows &&
            c >= 0 &&
            c < columns &&
            board[r][c] === currentPlayer
        ) {
            count++;
            r += directionRow;
            c += directionCol;
        }
        return count;
    }

    return (
        count(0, 1) + count(0, -1) >= 3 || // Horizontal
        count(1, 0) + count(-1, 0) >= 3 || // Vertical
        count(1, 1) + count(-1, -1) >= 3 || // Diagonal \
        count(1, -1) + count(-1, 1) >= 3   // Diagonal /
    );
}

createBoard();
document.getElementById('status').textContent = `${currentPlayer.toUpperCase()}'s turn`;
