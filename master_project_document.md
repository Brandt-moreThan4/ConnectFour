# Project Master File

## Project Structure

```
├── .gitignore
├── .vscode
│   └── launch.json
├── Pipfile
├── Pipfile.lock
├── README.md
├── analysis
│   ├── archive
│   │   ├── simulation_analysis_v1.ipynb
│   │   └── simulation_analysis_vc.ipynb
│   └── simulation_analysis_arena_vc.ipynb
├── archive
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
├── master_project_document.md
├── model_training
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── board.cpython-312.pyc
│   │   ├── engine.cpython-312.pyc
│   │   ├── game.cpython-312.pyc
│   │   ├── player.cpython-312.pyc
│   │   └── simulation_params.cpython-312.pyc
│   ├── board.py
│   ├── data
│   │   ├── master_db.json
│   │   ├── old
│   │   │   ├── arena_simulation.json
│   │   │   ├── arena_simulation2.json
│   │   │   ├── arena_simulation3.json
│   │   │   ├── arena_simulation4.json
│   │   │   ├── simulation_data.csv
│   │   │   ├── simulation_data_1_r1_r2.json
│   │   │   ├── simulation_data_monte_carlo_100.json
│   │   │   └── simulation_data_testing.json
│   │   ├── simulation5.json
│   │   └── stable
│   │       ├── arena_simulation4.json
│   │       ├── combined.json
│   │       ├── master_db.json
│   │       └── master_db_1.json
│   ├── engine.py
│   ├── game.py
│   ├── mod_1.ipynb
│   ├── models
│   ├── player.py
│   ├── utils.py
│   └── visualizer.ipynb
├── simulation.log
├── test.py
└── utils.py
```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\master_project_document.md

```md
# Project Master File

## Project Structure

```
├── __init__.py
├── __pycache__
│   ├── __init__.cpython-312.pyc
│   ├── board.cpython-312.pyc
│   ├── game.cpython-312.pyc
│   ├── player.cpython-312.pyc
│   └── simulation_params.cpython-312.pyc
├── board.py
├── constants.py
├── data
│   ├── old
│   │   └── simulation_data.csv
│   ├── simulation_data.json
│   ├── simulation_data_testing.json
│   └── stable
│       └── simulation_data_1_r1_r2.json
├── engine.py
├── game.py
├── player.py
└── utils.py
```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\board.py

```py
import numpy as np
import random
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

    def check_winner(self, token: int) -> bool:
        """Efficiently checks if a player with the given token has a winning line (4 in a row)."""

        for row in range(6):
            for col in range(7):
                # Skip if the current cell is not occupied by the token
                if self.grid[row, col] != token:
                    continue

                # Check horizontal (only if there are enough columns to the right)
                if col <= 3 and all(self.grid[row, col + i] == token for i in range(4)):
                    return True

                # Check vertical (only if there are enough rows below)
                if row <= 2 and all(self.grid[row + i, col] == token for i in range(4)):
                    return True

                # Check diagonal (bottom-left to top-right)
                if row <= 2 and col <= 3 and all(self.grid[row + i, col + i] == token for i in range(4)):
                    return True

                # Check diagonal (bottom-right to top-left)
                if row <= 2 and col >= 3 and all(self.grid[row + i, col - i] == token for i in range(4)):
                    return True

        return False


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
    
    def is_tie(self) -> bool:
        '''Check if the game is a tie.'''
        return self.is_full() and not self.check_any_winner()
    
    def get_random_move(self) -> int:
        '''Return a random column from the columns that are still playable.'''

        return np.random.choice(self.get_playable_cols())
    
    def make_move(self, column:int, token:int) -> None:
        '''Make the specified move on the board.'''

        if self.is_call_full(column):
            raise ValueError('This column is already full. You cannot make a move here.')

        # Find the first empty row in the column when looking from the bottom up.
        is_empty = self.grid[:,column] == 0
        row = np.where(is_empty)[0]
        row = row[-1]
        self.grid[row,column] = token
    
    def is_call_full(self,column:int) -> bool:
        '''Check if the column is full.'''
        return self.grid[0,column] != 0
    
    def get_playable_cols(self) -> list[int]:
        '''Return a list of columns that are not full.'''
        return np.where(self.grid[0] == 0)[0]
    
    def game_over(self) -> bool:
        '''Check if the game is over.'''
        return self.check_any_winner() or self.is_full()
    
    def get_copy(self) -> 'Board':
        '''Return a copy of the board so that we don't modify the original board.'''
        board = Board()
        board.grid = self.grid.copy()
        return board
    
    def check_for_obvious_move(self,token:int) -> Union[int,None]:
        '''Check if there is an obvious move to make. (A single move that will result in a win.)'''
        for col in self.get_playable_cols():
            board = self.get_copy()
            board.make_move(col,token)
            if board.check_winner(token):
                return col
        return None
    
    def check_for_obvious_move(self, token: int) -> Union[int, None]:
        """Check if there is an obvious move to make (a single move that will result in a win)
        or if there is an opponent's move to block."""

        # Check if there is a winning move for the current player
        for col in self.get_playable_cols():
            board = self.get_copy()
            board.make_move(col, token)
            if board.check_winner(token):
                return col  # Return the winning move

        # Check if there is a move that needs to be blocked (opponent's winning move)
        opponent_token = 2 if token == 1 else 1
        for col in self.get_playable_cols():
            board = self.get_copy()
            board.make_move(col, opponent_token)
            if board.check_winner(opponent_token):
                return col  # Return the blocking move

        # No obvious move found
        return None




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
    

class Node:
    def __init__(self, state: Board, parent=None):
        self.state = state  # Board state
        self.parent = parent  # Parent node
        self.children = []  # List of child nodes
        self.visits = 0  # Visit count
        self.value = 0  # Accumulated value (e.g., win/loss)

    def is_fully_expanded(self) -> bool:
        '''Check if all possible moves have been expanded. This is the case when the number of children is equal
          to the number of playable columns.'''
        
        return len(self.children) == len(self.state.get_playable_cols())
    
    @property
    def col_choice(self) -> int:
        '''Return the column choice that led to this node. (what column is different from this node and its parent)'''
        if self.parent is None:
            return None
 
        parent_grid = self.parent.state.grid
        current_grid = self.state.grid

        diff = current_grid - parent_grid
        col_choice = int(np.where(diff != 0)[1][0])
        return col_choice
    
    def __repr__(self) -> str:
        return f'Col({self.col_choice})'
    
    def __str__(self) -> str:
        return f'Col({self.col_choice})'

    def best_child(self, exploration_weight=1.4):
        choices_weights = [
            (child.value / (child.visits + 1)) + exploration_weight * np.sqrt(np.log(self.visits + 1) / (child.visits + 1))
            for child in self.children
        ]
        return self.children[np.argmax(choices_weights)]




def mcts(root_state: Board,perspective_token:int , itermax=50, exploration_weight=1.4) -> int:
    root = Node(root_state)

    for sim in range(itermax):
        node = root
        # Selection
        while node.is_fully_expanded() and node.children:
            node = node.best_child(exploration_weight)
            lol = node.col_choice
        
        # Expansion
        if not node.is_fully_expanded():
            possible_moves = node.state.get_playable_cols()
            for move in possible_moves:
                new_state = node.state.get_copy()
                new_state.make_move(move, 1 if node.state.grid.sum() % 2 == 0 else 2)
                child_node = Node(new_state, parent=node)
                node.children.append(child_node)
            node = random.choice(node.children)

        # Simulation
        result = simulate_game(node.state, perspective_token)

        # Backpropagation
        while node is not None:
            node.visits += 1
            node.value += result
            node = node.parent

    # Return the move leading to the best node. 
    best_move_node = root.best_child(exploration_weight=0)

    best_move_col = best_move_node.col_choice

    return best_move_col



def simulate_game(board_state:Board,perspective_token:int) -> int:

    # We want to implement a Monte Carlo simulation to determine the best move to make.
    board = board_state.get_copy()

    other_token = 2 if perspective_token == 1 else 1

    turn_token = perspective_token
    
    while board.game_over() == False:

        obvious_move = board.check_for_obvious_move(turn_token)
        if obvious_move is not None:
            move = obvious_move
        else:
            move = board.get_random_move()

        # Make the move
        board.make_move(move,turn_token)

        # Switch the turn token
        turn_token = 1 if turn_token == 2 else 2

    
    if board.check_winner(perspective_token):
        return 1
    elif board.check_winner(other_token):
        return -1
    else:
        return 0 # Tie


    

if __name__ == '__main__':
    # Test the functionality of Monte Carlo Tree Search
    board = Board()
    board.make_move(0,1)
    board.make_move(1,2)
    board.make_move(1,1)
    board.make_move(2,2)
    board.make_move(2,1)

    # Now we can test out the MCTS algorithm
    best_move = mcts(board,1,itermax=100)

    print(f'The best move to make is column {best_move}')
    print(board)
```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\constants.py

```py
NUMBER_OF_GAMES = 100

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\engine.py

```py
import pandas as pd
import logging
import json
from datetime import datetime
import time
import random
import uuid

# import constants as constants
from game import Game
from player import  RandomPlayer1, RandomPlayer2
import player


CHECK_POINTS = 2000

def setup_logging() -> None:
    '''Set up logging for the simulation which will log to a file and the terminal.'''
    LOG_FILE = 'simulation.log'
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filemode='w')

    # Add a handler to log to the terminal as well
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    # logging.getLogger().addHandler(console_handler)


def get_game_id() -> str:
    # Get current timestamp with microsecond precision
    timestamp = int(time.time() * 1_000_000)
    
    # Generate a random number
    random_num = random.randint(0, 999999)
    
    # Get a portion of a UUID
    uuid_part = uuid.uuid4().hex[:8]
    
    # Combine all parts
    unique_id = f"{timestamp:015d}-{random_num:06d}-{uuid_part}"
    
    return unique_id


def run_simulations(output_file:str,simulation_count:int) -> None:

    all_game_data = []
    for i in range(simulation_count):
        # logging.info(f'Simulation {i+1} started')

        # player_a = RandomPlayer1('Player 1',token=1)
        player_a = player.MonteCarloPlayer('Player 1',token=1,simulations=100)
        player_b = RandomPlayer2('Player 2',token=2)
        game_id = get_game_id()

        # Alternate the starting player
        if i % 2 == 0:
            game = Game(p1=player_a, p2= player_b, game_id=game_id)
        else:
            game = Game(p1=player_b, p2=player_a, game_id=game_id)
        while not game.is_over:
            game.play_turn()
            game.check_for_win()

        all_game_data.append(game.game_data.to_dict())
        logging.info(f'Simulation {i+1} done')

        if i % CHECK_POINTS == 0:
            logging.info(f'Checkpoint: {i} simulations done')
            with open(output_file,'w') as f:
                json.dump(all_game_data,f)

    with open(output_file,'w') as f:
        json.dump(all_game_data,f)

if __name__ == '__main__':
    DATA_FILE = 'model_training/data/simulation_data_testing.json'
    NUMBER_OF_GAMES = 10
    setup_logging()
    run_simulations(output_file=DATA_FILE,simulation_count=NUMBER_OF_GAMES)

    # print('!!! Simulation Done!!!')

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\game.py

```py
import pandas as pd
import logging
from dataclasses import dataclass, field
from datetime import datetime

from player import Player
from board import Board


@dataclass
class GameData:
    game_id: str
    player_one_id: str
    player_two_id: str
    winner_id: str = ''
    moves: list[int] = field(default_factory=list)

    @property
    def turns(self) -> int:
        return len(self.moves)

    def to_dict(self) -> dict:
        return {
            'game_id': self.game_id,
            'player_one_id': self.player_one_id,
            'player_two_id': self.player_two_id,
            'winner_id': self.winner_id,
            'moves': self.moves,
            'turns': self.turns
        }



class Game:
    def __init__(self,p1:Player,p2:Player,game_id:str):
        self.p1 = p1
        self.p2 = p2
        self.is_over = False
        self.board = Board()
        self.current_player = p1
        self.game_data = GameData(player_one_id=p1.player_id,player_two_id=p2.player_id,game_id=game_id)


    def play_turn(self):

        col_chosen = self.current_player.get_move(self.board)
        self.board.make_move(col_chosen,self.current_player.token)      
        self.game_data.moves.append(col_chosen)
        self.switch_player()
        
    
    def switch_player(self):
        self.current_player = self.p1 if self.current_player == self.p2 else self.p2
    
    
    def check_for_win(self) -> bool:

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
            self.game_data.winner_id = winner.player_id
            return True
        
        # Check for tie
        if self.board.is_full():
            self.is_over = True
            self.game_data.winner_id = 'Tie'
            return True
        
        return False
```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\player.py

```py
from board import Board, simulate_game, mcts


class Player:
    def __init__(self, name: str, token: int) -> None:
        self.name = name
        self.token = token # Should be unique. Represented by 1 or 2

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name

    def get_move(self, board: Board) -> int:
        move = self._get_move(board)
        return int(move)
    
    def _get_move(self, board: Board):
        raise NotImplementedError
    
    @property
    def player_id(self) -> str:
        raise NotImplementedError
    

class RandomPlayer1(Player):

    @property
    def player_id(self) -> str:
        return 'random_move_1'

    def _get_move(self, board: Board) -> int:
        return board.get_random_move()
    
class RandomPlayer2(Player):
    
    @property
    def player_id(self) -> str:
        return 'random_move_2'

    def _get_move(self, board: Board) -> int:
        return board.get_random_move()
    

class MonteCarloPlayer(Player):
    def __init__(self, name: str, token: int, simulations: int) -> None:
        super().__init__(name, token)
        self.simulations = simulations
    
    @property
    def player_id(self) -> str:
        return f'monte_carlo_{self.simulations}'
    
    def _get_move(self, board: Board) -> int:
        # Simulate moves
        
        best_move = mcts(board, perspective_token=self.token,itermax= self.simulations)
        return best_move
```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\utils.py

```py

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\__init__.py

```py
from .board import Board
from .player import Player


```


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
import json
from pathlib import Path

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


def combine_jsons(folder_path, output_file='combined.json', exclusions:list=None):
    if exclusions is None:
        exclusions = []

    combined_data = []
    for root, _, files in os.walk(folder_path):
        # Skip excluded directories
        if any(exclusion in root for exclusion in exclusions):
            continue
        for file in files:
            # Skip excluded files
            if file in exclusions:
                continue
            if any(exclusion in file for exclusion in exclusions):
                continue

            # Get the full file path
            file_path = os.path.join(root, file)

            # Only include JSON files
            if file.endswith('.json'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # combined_data.append(data)
                        combined_data.extend(data)
                except Exception as e:
                    print(f"Error reading file: {e}")

    # Write the combined data to a single JSON file
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(combined_data, json_file, indent=4)


if __name__ == "__main__":


    # Example usage:
    FOLDER = r'C:\Users\User\OneDrive\Desktop\Code\ConnectFour'
    # FOLDER = r'C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training'
    EXCLUSIONS = ['.git', 'node_modules','ipynb']  # Add any other folder/file names you want to exclude

    create_master_markdown(FOLDER, exclusions=EXCLUSIONS)

    # # Combine all JSON files in the folder and subfolders
    # DATA_FOLDER = Path(FOLDER) / 'data'
    # DATA_Exclusions = ['stable','old']
    # combine_jsons(DATA_FOLDER, output_file=DATA_FOLDER / 'combined.json', exclusions=DATA_Exclusions)
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
from model_training import player


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
    # bot_player = player.RandomNotStupidPlayer('bot', 2)
    bot_player = player.MonteCarloPlayer('bot', 2, 1000)

    # Randomly select a column for now
    if board.is_full():
        return None  # No moves available (game might be over)
    else:
        col_to_play = int(bot_player.get_move(board))
        return col_to_play


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
import random
# from player import Player
from typing import Union
import matplotlib.pyplot as plt

# Feels sloppy?
TOKEN_MAP = {'red':1,'yellow':2}

class Board:

    TOKEN_1 = 1
    TOKEN_2 = 2

    def __init__(self) -> None:
        self.grid = np.zeros((6,7))
        self.turn_token = self.TOKEN_1

    def __str__(self) -> str:
        return str(self.grid)

    def __repr__(self) -> str:
        return str(self.grid)

    def check_winner(self, token: int) -> bool:
        """Check to see if the provided token has won the game. Start in the top left and move right and down."""

        for row in range(6):
            for col in range(7):
                # Skip if the current cell is not occupied by the token
                if self.grid[row, col] != token:
                    continue

                # Check horizontal (only if there are enough columns to the right)
                if col <= 3 and all(self.grid[row, col + i] == token for i in range(4)):
                    return True

                # Check vertical (only if there are enough rows below)
                if row <= 2 and all(self.grid[row + i, col] == token for i in range(4)):
                    return True

                # Check diagonal (bottom-left to top-right)
                if row <= 2 and col <= 3 and all(self.grid[row + i, col + i] == token for i in range(4)):
                    return True

                # Check diagonal (bottom-right to top-left)
                if row <= 2 and col >= 3 and all(self.grid[row + i, col - i] == token for i in range(4)):
                    return True

        return False


    def check_any_winner(self) -> bool:
        '''Check if either player has won the game.'''
        return self.check_winner(self.TOKEN_1) or self.check_winner(self.TOKEN_2)

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


    @staticmethod
    def from_turn_sequence(turn_sequence:list[int]) -> 'Board':
        '''Convert a list of turn sequences into a Board object.'''
        board = Board()
        for turn in turn_sequence:
            board.make_move(turn,board.turn_token)
        return board
    

    def is_full(self) -> bool:
        '''Check if the board is full.'''
        return np.all(self.grid != 0)
    
    def is_tie(self) -> bool:
        '''Check if the game is a tie.'''
        return self.is_full() and not self.check_any_winner()
    
    def get_random_move(self) -> int:
        '''Return a random column from the columns that are still playable.'''

        return np.random.choice(self.get_playable_cols())
    
    def make_move(self, column:int, token:int) -> None:
        '''Make the specified move on the board.'''

        if self.is_call_full(column):
            raise ValueError('This column is already full. You cannot make a move here.')

        # Find the first empty row in the column when looking from the bottom up.
        empty_rows = np.where(self.grid[:,column] == 0)[0]
        lowest_empty_row = empty_rows[-1]
        self.grid[lowest_empty_row,column] = token
        self.turn_token = switch_token(token)
    
    def is_call_full(self,column:int) -> bool:
        '''Check if the column is full.'''
        return self.grid[0,column] != 0
    
    def get_playable_cols(self) -> list[int]:
        '''Return a list of columns that are not full.'''
        return np.where(self.grid[0] == 0)[0]
    
    def game_over(self) -> bool:
        '''Check if the game is over.'''
        return self.check_any_winner() or self.is_full()
    
    def get_copy(self) -> 'Board':
        '''Return a copy of the board so that we don't modify the original board.'''
        board = Board()
        board.grid = self.grid.copy()
        board.turn_token = self.turn_token
        return board
    
    @property
    def turn(self) -> str:
        '''Return the number of the current turn. Starting at 1 means it will be # of tokens played + 1.'''
        tokens_played = np.sum(self.grid != 0)
        return tokens_played + 1
    
    
    def check_for_obvious_move(self, token: int) -> Union[int, None]:
        """Check if there is an obvious move to make (a single move that will result in a win)
        or if there is an opponent's move to block."""

        # Check if there is a winning move for the current player
        for col in self.get_playable_cols():
            board = self.get_copy()
            board.make_move(col, token)
            if board.check_winner(token):
                return col  # Return the winning move

        # Check if there is a move that needs to be blocked (opponent's winning move)
        opponent_token = 2 if token == 1 else 1
        for col in self.get_playable_cols():
            board = self.get_copy()
            board.make_move(col, opponent_token)
            if board.check_winner(opponent_token):
                return col  # Return the blocking move

        # No obvious move found
        return None



    def display_board(self, player1_color='red', player2_color='yellow', empty_color='white', line_color='black', background_color='white'):
        """
        Visualize each Connect 4 game state as a separate plot with grid lines.

        Args:
        - states (list of np.ndarray): A list of 7x6 numpy arrays representing the game states.
        - player1_color (str): Color for player 1 discs.
        - player2_color (str): Color for player 2 discs.
        - empty_color (str): Color for empty slots.
        - line_color (str): Color for the grid lines.
        """
        n_rows, n_cols = (6,7)

        fig, ax = plt.subplots(figsize=(n_cols, n_rows * 0.6))

        fig.patch.set_facecolor(background_color)
        
        # Set the background color of the axes
        ax.set_facecolor(background_color)
            
        # Draw the Connect 4 grid
        for row in range(n_rows):
            for col in range(n_cols):
                value = self.grid[row, col]
                if value == 0:  # Empty slot
                    color = empty_color
                elif value == 1:  # Player 1
                    color = player1_color
                elif value == 2:  # Player 2
                    color = player2_color
                else:
                    raise ValueError("Invalid grid value: must be 0, 1, or 2.")
                
                # # Draw a circle for the slot
                ax.add_patch(plt.Circle((col + 0.5, n_rows - row - 0.5), 0.4, color=color))

        # Add grid lines
        for row in range(n_rows + 1):
            ax.hlines(row, 0, n_cols, colors=line_color, linewidth=0.5)  # Horizontal lines
        for col in range(n_cols + 1):
            ax.vlines(col, 0, n_rows, colors=line_color, linewidth=0.5)  # Vertical lines

        # Set grid limits and remove axes
        ax.set_xlim(0, n_cols)
        ax.set_ylim(0, n_rows)
        ax.set_aspect('equal')
        ax.axis('off')

        # # Set a title for each grid
        ax.set_title(f"Game State {self.turn}", fontsize=14)

        # Show the plot
        plt.show()
        # return fig, ax





class Node:
    def __init__(self, state: Board, parent=None):
        self.state = state  # Board state
        self.parent:Node = parent  # Parent node
        self.children:list[Node] = []  # List of child nodes
        self.visits = 0  # Visit count
        self.value = 0  # Accumulated value (e.g., win/loss)

    def is_fully_expanded(self) -> bool:
        '''Check if all possible moves have been expanded. This is the case when the number of children is equal
          to the number of playable columns.'''
        
        return len(self.children) == len(self.state.get_playable_cols())
    
    @property
    def col_choice(self) -> int:
        '''Return the column choice that led to this node. (what column is different from this node and its parent)'''
        if self.parent is None:
            return None
 
        parent_grid = self.parent.state.grid
        current_grid = self.state.grid

        diff = current_grid - parent_grid
        col_choice = int(np.where(diff != 0)[1][0])
        return col_choice
    
    def __repr__(self) -> str:
        # Show some stats about the node
        return f'Col({self.col_choice}) - V: {self.visits} - W: {self.value} - D: {self.depth}'
    
    def __str__(self) -> str:
        return f'Col({self.col_choice})'
    
    def calc_ucb(self, exploration_weight=1.4) -> float:
        '''Calculate the Upper Confidence Bound (UCB) for the node.'''

        if self.visits == 0:
            return float('inf')
        
        avg_reward = self.value / self.visits
        exploration_term = np.sqrt(np.log(self.parent.visits) / self.visits)

        ucb = avg_reward + exploration_weight * exploration_term
        return ucb

    def best_child(self, exploration_weight=1.4) -> 'Node':
        '''Select the child node with the best UCB value. '''


        child_ucbs = [child.calc_ucb(exploration_weight) for child in self.children]
        # Could prolly break ties randomly instead of always choosing the first one

        return self.children[np.argmax(child_ucbs)]
    
    @property
    def depth(self) -> int:
        '''Return the depth of the node in the tree.'''
        if self.parent is None:
            return 0
        return 1 + self.parent.depth


def switch_token(token:int) -> int:
    '''Switch the token from 1 to 2 and vice versa.'''
    return Board.TOKEN_1 if token == Board.TOKEN_2 else Board.TOKEN_2    


# Updated mcts function with token counting logic
def monte_carlo_tree_search(root_state: Board, perspective_token: int, itermax=100, exploration_weight=1.4) -> int:
    # Initialize the root node of the search tree with the provided board state
    root = Node(root_state)

    # Perform a specified number of simulations (iterations)
    for sim in range(itermax):
        node = root  # Start at the root node for each simulation

        # Selection Phase:
        # Traverse the tree, selecting child nodes based on their exploration-exploitation balance.
        # This continues until we reach a node that is not fully expanded or a leaf node.
        while node.is_fully_expanded() and node.children:
            node = node.best_child(exploration_weight)

        # Expansion Phase:
        # If the selected node is not fully expanded, add one or more child nodes corresponding to possible moves.
        if not node.is_fully_expanded():
            possible_moves = node.state.get_playable_cols()  # Get available moves (playable columns)
            for move in possible_moves:
                new_state = node.state.get_copy()  # Create a copy of the current board state
                new_state.make_move(move, new_state.turn_token)  # Make the move on the new state
                child_node = Node(new_state, parent=node)  # Create a new node with the updated state
                node.children.append(child_node)  # Add the new node as a child
            node = random.choice(node.children)  # Choose one of the newly added child nodes for simulation

        # Simulation Phase:
        # Simulate a random game from the current node's state until the game ends (win/loss/tie).
        result = simulate_game(node.state, perspective_token)

        # Backpropagation Phase:
        # Propagate the simulation result up the tree, updating visit counts and node values.
        while node is not None:
            node.visits += 1  # Increment the visit count for the node
            node.value += result  # Update the accumulated value (e.g., win/loss score)
            node = node.parent  # Move up to the parent node

    # After all simulations, select the child node with the best win rate (exploitation only)
    best_move_node = root.best_child(exploration_weight=0)

    # Extract the column choice that corresponds to the best move found
    best_move_col = best_move_node.col_choice

    return best_move_col  # Return the column that leads to the best move




def simulate_game(board_state:Board,perspective_token:int) -> int:

    # We want to implement a Monte Carlo simulation to determine the best move to make.
    board = board_state.get_copy()

    other_token = switch_token(perspective_token)

    turn_token = perspective_token
    
    while board.game_over() == False:

        obvious_move = board.check_for_obvious_move(turn_token)
        if obvious_move is not None:
            move = obvious_move
        else:
            move = board.get_random_move()

        # Make the move
        board.make_move(move,turn_token)

        # Switch the turn token
        turn_token = switch_token(turn_token)

    # Check for win, loss or tie and distribute points accordingly
    if board.check_winner(perspective_token):
        return 1
    elif board.check_winner(other_token):
        return -1
    else:
        return 0 


    

if __name__ == '__main__':
    # Test the functionality of Monte Carlo Tree Search
    board = Board()
    board.make_move(0,1)
    board.make_move(1,2)
    board.make_move(1,1)
    board.make_move(2,2)
    board.make_move(2,1)
    board.make_move(3,2)

    board.display_board()

    # Now we can test out the MCTS algorithm
    # best_move = monte_carlo_tree_search(board,1,itermax=100)

    # print(f'The best move to make is column {best_move}')
    print(board)


```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\engine.py

```py
import pandas as pd
import logging
import json
import random

from pathlib import Path

# import constants as constants
from game import Game, GameData
from board import Board
import player

# Big bank of players that may be needed
stupid_player = player.RandomNaivePlayer('Stupid',token=None)
not_stupid_player = player.RandomNotStupidPlayer('Not Stupid',token=None)
monty_50 = player.MonteCarloPlayer('Monty50',token=None,simulations=50)
monty_100 = player.MonteCarloPlayer('Monty100',token=None,simulations=100)
monty_200 = player.MonteCarloPlayer('Monty200',token=None,simulations=200)
monty_500 = player.MonteCarloPlayer('Monty500',token=None,simulations=500)
monty_1000 = player.MonteCarloPlayer('Monty1000',token=None,simulations=1000)
monty_150 = player.MonteCarloPlayer('Monty150',token=None,simulations=150)
monty_200 = player.MonteCarloPlayer('Monty149',token=None,simulations=200)
monty_51 = player.MonteCarloPlayer('Monty51',token=None,simulations=51) 


def setup_logging() -> None:
    '''Set up logging for the simulation which will log to a file and the terminal.'''
    LOG_FILE = 'simulation.log'
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filemode='w')

    # Add a handler to log to the terminal as well
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(console_handler)


class DataBase:

    def __init__(self,master_file:str='model_training/data/master_db.json') -> None:
        self.master_file = master_file
        self.load()
        
    def load(self) -> pd.DataFrame:
        path = Path(self.master_file)
        if not path.exists():
            logging.info(f'No database found at {self.master_file}. Creating new database')
            self.data = []
            self.save()

        with open(self.master_file,'r') as f:
            data = json.load(f)
        self.data:list = data

    def save(self,file_path:str=None) -> None:
        file = file_path if file_path else self.master_file
        with open(file,'w') as f:
            json.dump(self.data,f,indent=4)
    
    def add_data(self,new_data:list[dict],save:bool=True) -> None:
        self.data.extend(new_data)
        if save:
            self.save()
    
    def __repr__(self):
        return f'DataBase({self.master_file}) - {len(self.data)} records'

    def __str__(self):
        return f'DataBase({self.master_file}) - {len(self.data)} records'


def run_simulation(p1:player.Player,p2:player.Player) -> Game:

    # Make sure the players have their tokens set
    p1.token = Board.TOKEN_1
    p2.token = Board.TOKEN_2

    game = Game(p1=p1,p2=p2)

    while not game.is_over:
        game.play_turn()
        game.check_for_win()

    return game

def run_simulations(p1:player.Player,p2:player.Player,sim_count:int=100,randomize_order:bool=True) -> list[GameData]:
    all_game_data = []
    for i in range(sim_count):
        if randomize_order:
            p1,p2 = random.sample([p1,p2],2)

        game = run_simulation(p1,p2)
        all_game_data.append(game.game_data)
        # logging.info(f'Simulation {i+1} done')
    return all_game_data

def simulation_stats(all_game_data:list[GameData]):

    data_as_dicts = [game_data.to_dict() for game_data in all_game_data]
    stats = {}
    df = pd.DataFrame(data_as_dicts)




def run_simulation_arena(arena_players:list[player.Player],simulation_count:int,output_file:str=None, data_db:DataBase=None,checkpoints=500) -> None:

    all_game_data = []
    for i in range(simulation_count):

        player_1, player_2 = random.sample(arena_players,2)
        game = run_simulation(player_1,player_2)

        all_game_data.append(game.game_data.to_dict())
        logging.info(f'Simulation {i+1} done')

        if i % checkpoints == 0 and data_db is not None:
            logging.info(f'Checkpoint Reached: {i} simulations done')
            data_db.add_data(all_game_data)
            all_game_data = []

    if data_db is not None:
        data_db.add_data(all_game_data)     
        

if __name__ == '__main__':
    setup_logging()
    DATA_FILE = 'model_training/data/master_db.json'
    # DATA_FILE = 'model_training/data/combined_toy.json'   
    database = DataBase(DATA_FILE) 
    NUMBER_OF_GAMES = 50_000
    CHECK_POINTS = 100

    players = [monty_100,monty_1000]
    players = [monty_50,monty_100]
    run_simulation_arena(players,NUMBER_OF_GAMES,data_db=database,checkpoints=CHECK_POINTS)


```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\game.py

```py
import pandas as pd
import logging
from dataclasses import dataclass, field
from datetime import datetime
import time
import random
import uuid

from player import Player
from board import Board


@dataclass
class GameData:
    game_id: str
    player_one_id: str
    player_two_id: str
    first_mover_id: str
    winner_id: str = ''
    moves: list[int] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime = None

    @property
    def turns(self) -> int:
        return len(self.moves)

    def to_dict(self) -> dict:
        return {
            'game_id': self.game_id,
            'player_one_id': self.player_one_id,
            'player_two_id': self.player_two_id,
            'winner_id': self.winner_id,
            'first_mover_id': self.first_mover_id,
            'moves': self.moves,
            'turns': self.turns,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() 
        }



class Game:
    def __init__(self,p1:Player,p2:Player):
        self.p1 = p1
        self.p2 = p2
        self.is_over = False
        self.board = Board()
        self.current_player = p1
        self.game_data = GameData(player_one_id=p1.player_id,player_two_id=p2.player_id,game_id=self.get_game_id(),first_mover_id=p1.player_id)


    def play_turn(self):

        col_chosen = self.current_player.get_move(self.board)
        self.board.make_move(col_chosen,self.current_player.token)      
        self.game_data.moves.append(col_chosen)
        self.switch_player()
        
    
    def switch_player(self):
        self.current_player = self.p1 if self.current_player == self.p2 else self.p2
    
    
    def check_for_win(self) -> bool:

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
            self.game_data.winner_id = winner.player_id
            self.game_data.end_time = datetime.now()
            return True
        
        # Check for tie
        if self.board.is_full():
            self.is_over = True
            self.game_data.winner_id = 'Tie'
            self.game_data.end_time = datetime.now()            
            return True
        
        return False
    
    def get_game_id(self) -> str:
        # Get current timestamp with microsecond precision
        timestamp = int(time.time() * 1_000_000)
        
        # Generate a random number
        random_num = random.randint(0, 999999)
        
        # Get a portion of a UUID
        uuid_part = uuid.uuid4().hex[:8]
        
        # Combine all parts
        unique_id = f"{timestamp:015d}-{random_num:06d}-{uuid_part}"
        
        return unique_id
```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\player.py

```py
from board import Board, simulate_game, monte_carlo_tree_search
# from .board import Board, simulate_game, monte_carlo_tree_search


class Player:
    def __init__(self, name: str, token: int) -> None:
        self.name = name
        self.token = token # Should be unique. Represented by 1 or 2

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name

    def get_move(self, board: Board) -> int:
        move = self._get_move(board)
        return int(move)
    
    def _get_move(self, board: Board):
        raise NotImplementedError
    
    @property
    def player_id(self) -> str:
        raise NotImplementedError
    

class RandomNaivePlayer(Player):
    
    @property
    def player_id(self) -> str:
        return 'random_naive'

    def _get_move(self, board: Board) -> int:
        return board.get_random_move()

class RandomNotStupidPlayer(Player):

    @property
    def player_id(self) -> str:
        return 'random_not_stupid'

    def _get_move(self, board: Board) -> int:
        obvious_move = board.check_for_obvious_move(self.token)
        if obvious_move is not None:
            return obvious_move
        else:
            return board.get_random_move()
    

class MonteCarloPlayer(Player):
    def __init__(self, name: str, token: int, simulations: int) -> None:
        super().__init__(name, token)
        self.simulations = simulations
    
    @property
    def player_id(self) -> str:
        return f'monte_carlo_{self.simulations}'
    
    def _get_move(self, board: Board) -> int:
        move = board.check_for_obvious_move(self.token)
        if move is None:
            move = monte_carlo_tree_search(board, perspective_token=self.token,itermax=self.simulations)
        return move
```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\utils.py

```py

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\__init__.py

```py
from .board import Board
from .player import Player


```

