# Project Master File

## Project Structure

```
├── .gitignore
├── .vscode
│   └── launch.json
├── Pipfile
├── Pipfile.lock
├── README.md
├── archive
│   └── connect_four.py
├── backend
│   ├── __pycache__
│   │   ├── app.cpython-312.pyc
│   │   └── bot_logic.cpython-312.pyc
│   ├── app.py
│   ├── bot_logic.py
│   └── requirements.txt
├── frontend
│   ├── index.html
│   ├── old
│   │   ├── future_script.js
│   │   └── script_v1.js
│   ├── script.js
│   └── style.css
├── model_training
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── board.cpython-312.pyc
│   │   ├── game.cpython-312.pyc
│   │   ├── player.cpython-312.pyc
│   │   └── simulation_params.cpython-312.pyc
│   ├── board.py
│   ├── constants.py
│   ├── data
│   │   └── simulation_data.csv
│   ├── engine.py
│   ├── game.py
│   ├── player.py
│   └── utils.py
├── simulation.log
├── test.py
└── utils.py
```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\README.md

```md

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\test.py

```py
# import sys
# import os
# from pathlib import Path
import pandas as pd

# from model_training import Board, Player

print('Started')

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\utils.py

```py
import os

def get_folder_tree(folder_path, exclusions=None, indent=''):
    if exclusions is None:
        exclusions = []

    tree_structure = ""
    try:
        # Get a list of all items in the current directory
        items = os.listdir(folder_path)
    except PermissionError:
        tree_structure += f"{indent}[Permission Denied]\n"
        return tree_structure

    # Loop through each item in the folder
    for index, item in enumerate(sorted(items)):
        # Skip any item in the exclusions list
        if item in exclusions:
            continue

        # Construct the full item path
        item_path = os.path.join(folder_path, item)
        # Build the tree structure string
        connector = '├── ' if index < len(items) - 1 else '└── '
        tree_structure += f"{indent}{connector}{item}\n"

        # If the item is a directory, recursively get its contents
        if os.path.isdir(item_path):
            new_indent = indent + ('│   ' if index < len(items) - 1 else '    ')
            tree_structure += get_folder_tree(item_path, exclusions, new_indent)

    return tree_structure

def create_master_markdown(folder_path, output_file='master_project_document.md',exclusions=None):
    if exclusions is None:
        exclusions = []

    # Create the master Markdown content
    markdown_content = "# Project Master File\n\n"
    markdown_content += "## Project Structure\n\n"
    markdown_content += "```\n"
    markdown_content += get_folder_tree(folder_path, exclusions)
    markdown_content += "```\n\n"

    # Traverse the folder to add each code file's content
    for root, _, files in os.walk(folder_path):
        # Skip excluded directories
        if any(exclusion in root for exclusion in exclusions):
            continue
        for file in files:
            # Skip excluded files
            if file in exclusions:
                continue

            # Get the full file path
            file_path = os.path.join(root, file)

            # Only include text/code files (you can add more extensions as needed)
            if file.endswith(('.py', '.js', '.html', '.css', '.md', '.java', '.txt', '.sh')):
                markdown_content += f"## {file_path}\n\n"
                markdown_content += "```" + file.split('.')[-1] + "\n"
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        markdown_content += f.read()
                except Exception as e:
                    markdown_content += f"Error reading file: {e}"
                markdown_content += "\n```\n\n"

    # Write the content to a master Markdown file
    with open(output_file, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)



# Example usage:
FOLDER = r'C:\Users\User\OneDrive\Desktop\Code\ConnectFour'
EXCLUSIONS = ['.git', 'node_modules']  # Add any other folder/file names you want to exclude

create_master_markdown(FOLDER, exclusions=EXCLUSIONS)

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\archive\connect_four.py

```py
# import pandas as pd
# from matplotlib.style import available
import numpy as np
import seaborn as sns; sns.set_theme()
import matplotlib.pyplot as plt
# rng = np.random.default_rng()

diag_matrix_lr = np.identity(4)
diag_matrix_rl = np.fliplr(np.identity(4))

def create_empty_grid() -> np.array:
    return np.zeros(shape=(6,7))


BLACK_NUMBER = 1
RED_NUMBER = 2


def get_black_grid(grid) -> np.array:
    return grid == BLACK_NUMBER

def get_red_grid(grid:np.array):
    return grid == RED_NUMBER

def get_color_grid(grid,color:str):
    if color == 'Black':
        return grid == BLACK_NUMBER
    elif color == 'Red':
        return grid == RED_NUMBER
    else:
        raise('Dumbass, that is not a valid color')



def is_horizontal_victory(color_grid) -> bool:
    # Top to bottom, left to right search
    for row in range(6):
        for col in range(4):
            if sum(color_grid[row,col:(col+4)]) == 4:
                return True
    return False


def is_vertical_victory(color_grid) -> bool:
    for row in range(3):
        for col in range(7):
            if sum(color_grid[row:(row+4),col]) == 4:
                return True
    return False


def is_diagonal_victory(color_grid:np.array):
    for row in range(3):
        for col in range(4):
            if  np.multiply(diag_matrix_lr,color_grid[row:(row+4),col:(col+4)]).sum() == 4 or np.multiply(diag_matrix_rl,color_grid[row:(row+4),col:(col+4)]).sum() == 4 :
                return True
    return False


def is_connect_four(color_grid:np.array):
    """"""

    if is_horizontal_victory(color_grid) or is_vertical_victory(color_grid) or is_diagonal_victory(color_grid):
        return True
    else:
        return False


def get_available_row_index(grid:np.array,column:int) -> int:
    for row in range(5,-1,-1):
        if grid[row,column] == 0:
            return row
    return None

def get_available_cols(grid):
    available_cols = []
    for col in range(7):
        if grid[0,col] == 0:
            available_cols.append(col)    
    return available_cols


class Player:

    def __init__(self) -> None:
        self.decision_maker = None
    
    def make_decision(self,grid:np.matrix) -> int:
        """Returns the column to play in."""
        col = np.random.choice(7)
        available_cols =  get_available_cols(grid)
        while col not in available_cols:
            col = np.random.choice(7)

        return col


class Game:

    def __init__(self,black_player=None,red_player=None):
        self.grid = None
        self.player_turn = 'Black'
        self.actions_dict = {'Black':[],'Red':[]}
        self.game_on = None
        self.black_player = black_player
        self.red_player = red_player


    def update_grid(self,row,col:int):
        """Place the appropriate row"""
        if self.player_turn == 'Black':
            checker_number = BLACK_NUMBER
        else:
            checker_number = RED_NUMBER

        
        self.grid[row,col] = checker_number


    def start_game(self):

        self.game_on = True
        self.grid = create_empty_grid()


    def play_turn(self,col:int):

        if col not in range(7):
            raise Exception('Not a valid column index')

        row = get_available_row_index(self.grid,col)

        if row is None:
            raise Exception('Dumbass. Bad Column input')

        self.update_grid(row,col)

        if self.player_turn == 'Black':
            self.actions_dict['Black'].append(col)
        elif self.player_turn == 'Red':
            self.actions_dict['Red'].append(col)

        reward = 0

        if is_connect_four(get_color_grid(self.grid,self.player_turn)):
            print(f'Hot damn. {self.player_turn} won.')
            self.game_on = False
            reward = 1 if self.player_turn == 'Black' else -1

        self.player_turn = "Red" if self.player_turn == 'Black' else "Black"

        return reward


    # def play_game(self):
    #     print("Begin!!\n")

    #     while True:
    #         print(f"It's {self.player_turn}'s turn:")
    #         print(self.grid)

    #         while True:
    #             col_choice = input('Select column choice as an integer from 1-7.')
    #             col_choice = int(col_choice)

    #             row_index = self.get_available_row_index(column=col_choice-1) 
    #             if row_index is None:
    #                 print(f'Sorry, column "{col_choice}" is not a valid column. Please choose again.')
    #             else:
    #                 self.update_grid(row_index,col_choice-1)
    #                 break

    #         if is_connect_four(get_color_grid(self.grid,self.player_turn)):
    #             print(f'Hot damn. {self.player_turn} won.')
    #             break


    #         self.player_turn = "Red" if self.player_turn == 'Black' else "Black"



    
if __name__ == '__main__':
    

    black = Player()
    red = Player()
    game = Game(black_player=black, red_player=red)
    game.start_game()
    print(game.grid)
    game_counts = 3

    rewards = []
    actions = []

    for i in range(game_counts):

        while game.game_on == True:
            

            if game.player_turn == "Black":
                col = black.make_decision(game.grid)
            else:
                col = red.make_decision(game.grid)
            
            reward =  game.play_turn(col)
            plt.clf()
            sns.heatmap(game.grid)
            plt.show()
            print(game.grid)
            actions = game.actions_dict.copy()

        rewards.append(reward)





# game.play_game()



print('done')
```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\backend\app.py

```py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
import time

from bot_logic import get_bot_move


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes by default

@app.route('/api/move', methods=['POST'])
def get_move():
    """
    Handle requests from the frontend to get the bot's move.
    Expects a JSON payload with the current board state.
    """
    data = request.json
    board = data.get('board')  # Get the current board state from the request

    if board is None:
        return jsonify({"error": "Board state not provided"}), 400

    # Call the function to determine the bot's move
    col = get_bot_move(board)

    # It's unnerving if the bot plays so quickly
    time.sleep(1)

    # Return the bot's chosen column as a JSON response
    return jsonify({"column": col})

if __name__ == '__main__':
    app.run(debug=True)

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\backend\bot_logic.py

```py
import random
from pathlib import Path
import sys


PARENT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(PARENT_DIR))

from model_training.board import Board
from model_training.player import RandomPlayer


def get_bot_move(board) -> int | None:
    
    # Generate a list of available columns (not full)
    columns = len(board[0])

    # If the top row of the board is None, the column is not full
    available_cols = [col for col in range(7) if board[0][col] is None]

    # Randomly select a column for now
    if available_cols:
        return random.choice(available_cols)
    else:
        return None  # No moves available (game might be over)


def get_bot_move(board_data) -> int | None:
    

    board = Board.from_lists(board_data)
    bot_player = RandomPlayer('bot', 2)

    # Randomly select a column for now
    if board.is_full():
        return None  # No moves available (game might be over)
    else:
        col_to_play = int(bot_player.get_move(board))
        return col_to_play


# Convert the board from a list of strings to our Board object
def convert_board(board_state:list[str]):
    pass
```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\backend\requirements.txt

```txt

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
        const response = await fetch('http://127.0.0.1:5000/api/move', {
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

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\frontend\old\future_script.js

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
        const response = await fetch('http://127.0.0.1:5000/api/move', {
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

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\frontend\old\script_v1.js

```js
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

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\board.py

```py
import numpy as np
# from player import Player
from typing import Union

# Feels sloppy?
TOKEN_MAP = {'red':1,'yellow':2}
VALID_TOKENS = [1,2]

class Board:
    def __init__(self) -> None:
        self.grid = np.zeros((6,7))
        self.token_1 = 1
        self.token_2 = 2

    def __str__(self) -> str:
        return str(self.grid)

    def __repr__(self) -> str:
        return str(self.grid)

    def check_winner(self,token:Union[int,str]) -> bool:
        '''Check if the current player has won the game. Is this super inefficient??? Feels like there is a more concise
        elegant way to do this.'''
        bool_grid = self.grid == token
        return is_connect_four(bool_grid)

    def check_any_winner(self) -> bool:
        '''Check if either player has won the game.'''
        return self.check_winner(self.token_1) or self.check_winner(self.token_2)

    @staticmethod
    def from_lists(board_data:list[list]) -> 'Board':
        '''Convert a list of strings to a Board object.'''
        board = Board()
        for row in range(6):
            for col in range(7):
                cell_value = board_data[row][col]
                if cell_value is not None:
                    board.grid[row,col] = TOKEN_MAP[cell_value]
        
        return board


    def is_full(self) -> bool:
        '''Check if the board is full.'''
        return np.all(self.grid != 0)
    
    def get_random_move(self) -> int:
        '''Return a random column from the columns that are still playable.'''

        # Get the columns that are still playable (check where the top row is still empty)
        playable_columns = np.where(self.grid[0] == 0)[0]
        return np.random.choice(playable_columns)
    
    def make_move(self, column:int, token:int) -> None:
        '''Make the specified move on the board.'''

        # Find the first empty row in the column when looking from the bottom up.
        is_empty = self.grid[:,column] == 0
        row = np.where(is_empty)[0]
        if len(row) == 0:
            raise ValueError('This column is already full. You cannot make a move here.')
        
        row = row[-1]
        self.grid[row,column] = token



diag_matrix_lr = np.identity(4)
diag_matrix_rl = np.fliplr(np.identity(4))


def is_horizontal_victory(bool_grid:np.ndarray) -> bool:
    # Top to bottom, left to right search
    for row in range(6):
        for col in range(4):
            if sum(bool_grid[row,col:(col+4)]) == 4:
                return True
    return False


def is_vertical_victory(color_grid:np.ndarray) -> bool:
    for row in range(3):
        for col in range(7):
            if sum(color_grid[row:(row+4),col]) == 4:
                return True
    return False


def is_diagonal_victory(color_grid:np.ndarray):

    for row in range(3):
        for col in range(4):
            if  np.multiply(diag_matrix_lr,color_grid[row:(row+4),col:(col+4)]).sum() == 4 or np.multiply(diag_matrix_rl,color_grid[row:(row+4),col:(col+4)]).sum() == 4 :
                return True
    return False


def is_connect_four(color_grid:np.ndarray) -> bool:
    """Returns true if this player has connect 4 anywhere."""

    if is_horizontal_victory(color_grid) or is_vertical_victory(color_grid) or is_diagonal_victory(color_grid):
        return True
    else:
        return False
```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\constants.py

```py
NUMBER_OF_GAMES = 100

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\engine.py

```py
import pandas as pd
import logging
import model_training.constants as constants
from game import Game
from player import Player, RandomPlayer


def setup_logging() -> None:
    '''Set up logging for the simulation which will log to a file and the terminal.'''
    LOG_FILE = 'simulation.log'
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Add a handler to log to the terminal as well
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(console_handler)




def run_simulations() -> None:
    logging.info('Simulation started')
    all_game_data = []
    for i in range(constants.NUMBER_OF_GAMES):
        logging.info(f'Simulation {i+1} started')

        # Initialize the game
        player_1 = RandomPlayer('Player 1',token=1)
        player_2 = RandomPlayer('Player 2',token=2)
        game = Game(player_1, player_2)
        while not game.is_over:
            # game.save_state()
            game.play_turn()
            game.check_for_win()
        if game.winner != 'Tie':
            logging.info(f'The winner of the game was {game.winner}!')
        game_data = game.get_data()
        game_data['game_id'] = i
        # game_data['winner'] = game.winner
        all_game_data.append(game_data)


        logging.info(f'Simulation {i+1} done')

    all_game_data = pd.concat(all_game_data)
    all_game_data.to_csv('model_training/data/simulation_data.csv',index=False)


if __name__ == '__main__':
    setup_logging()

    run_simulations()

    # print('!!! Simulation Done!!!')

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\game.py

```py
import pandas as pd
import logging

from player import Player
from board import Board


class Game:
    def __init__(self,p1:Player,p2:Player):
        self.p1 = p1
        self.p2 = p2
        self.is_over = False
        self.board = Board()
        self.current_player = p1
        self.turn = 0
        self.winner = None
        self.last_move:int = None
        self.game_data = []

    def play_turn(self):
        self.turn += 1
        col_chosen = self.current_player.get_move(self.board)
        # We want to save the state using the information we had here and what decision was made.
        self.save_state(col_chosen)
        self.board.make_move(col_chosen,self.current_player.token)
        self.switch_player()
        
    
    def switch_player(self):
        self.current_player = self.p1 if self.current_player == self.p2 else self.p2
    
    def save_state(self,col_chosen:int):
        # Things we want to save: turn, player turn, column chosen, board state

        # Convert the board state into a dictionary. x_0 represents the top left cell, x2 the cell to the right of that,
        # x_41 the bottom right cell.
        # Later I need to refactor this into a method in the board class. (And make the board posisble to instatntiate with a grid
        # in the dictionary format)

        grid = self.board.grid
        flat_grid = grid.flatten()
        cells = {f'x_{i}':flat_grid[i] for i in range(len(flat_grid))}
        data = {
            'turn': self.turn,
            'player_turn': self.current_player,
            'column_chosen': col_chosen}
        data = {**data,**cells}
        self.game_data.append(data)
    
    def get_data(self) -> pd.DataFrame:
        '''Return the game data in a pretty data frame. '''

        # # Add on a final row that shows the final board state?
        # final_board = self.board.grid
        # flat_grid = final_board.flatten()
        # cells = {f'x_{i}':flat_grid[i] for i in range(len(flat_grid))}
        # data = {
        #     'turn': self.turn,
        #     'player_turn': self.current_player,
        #     'column_chosen': self.last_move}


        # Add on the winner
        data = pd.DataFrame(self.game_data)
        data['winner'] = self.winner
        return data


    
    def check_for_win(self):

        # Check if the current player has won
        winner = None
        p1_win = self.board.check_winner(self.p1.token)
        p2_win = self.board.check_winner(self.p2.token)
        if p1_win:
            winner = self.p1
        elif p2_win:
            winner = self.p2


        if winner is not None:
            self.is_over = True
            self.winner = winner
            logging.info(f'{self.winner} has won the game on turn {self.turn}!')
            return True
        
        # Check for tie
        if self.board.is_full():
            self.is_over = True
            logging.info(f'The game is a tie on turn {self.turn}!')
            self.winner = 'Tie'
            return True
        
        return False
```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\player.py

```py
from .board import Board

class Player:
    def __init__(self, name: str,token:int) -> None:
        self.name = name
        # self.color = color
        self.token = token

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name

    def get_move(self, board:Board) -> int:
        raise NotImplementedError
    

class RandomPlayer(Player):
    def get_move(self, board:Board) -> int:
        return board.get_random_move()
```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\utils.py

```py

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\__init__.py

```py
from .board import Board
from .player import Player


```

