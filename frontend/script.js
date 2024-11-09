// Number of columns and rows for the Connect 4 board
const columns = 7; // Standard Connect 4 game has 7 columns
const rows = 6;    // Standard Connect 4 game has 6 rows

// Variable to track the current player, starting with 'red'
let currentPlayer = 'red';

// Initialize the board state as a 2D array filled with null values (empty cells)
let board = Array(rows).fill(null).map(() => Array(columns).fill(null));

// Display initial status message for the first player
document.getElementById('status').textContent = `${currentPlayer.toUpperCase()}'s turn`;

// Select all cells from the HTML and attach click event listeners
const cells = document.querySelectorAll('.cell');
cells.forEach(cell => {
    // When a cell is clicked, call the handleCellClick function
    cell.addEventListener('click', handleCellClick);
});

// Function to handle cell clicks (player moves)
function handleCellClick(event) {
    // Get the column index from the clicked cell's data attribute
    const col = parseInt(event.target.dataset.col);

    // Find the lowest available row in the selected column
    for (let r = rows - 1; r >= 0; r--) {
        // If the cell is empty (null), place the current player's piece
        if (!board[r][col]) {
            // Update the board state
            board[r][col] = currentPlayer;

            // Find the cell element in the DOM using its data attributes
            const cell = document.querySelector(`.cell[data-row='${r}'][data-col='${col}']`);
            // Add classes to visually represent the move (marking the cell as taken)
            cell.classList.add('taken', currentPlayer);

            // Check if the move results in a win
            if (checkWin(r, col)) {
                // If a win is detected, display a message and disable further moves
                document.getElementById('status').textContent = `${currentPlayer.toUpperCase()} wins!`;
                disableBoard();
            } else {
                // If no win, switch to the next player
                currentPlayer = currentPlayer === 'red' ? 'yellow' : 'red';
                // Update the status message to show the next player's turn
                document.getElementById('status').textContent = `${currentPlayer.toUpperCase()}'s turn`;
            }
            break; // Exit the loop once a move is made
        }
    }
}

// Function to disable further moves once a win is detected
function disableBoard() {
    // Select all cells and remove their click event listeners
    cells.forEach(cell => cell.removeEventListener('click', handleCellClick));
}

// Function to check if the current move results in a win
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
