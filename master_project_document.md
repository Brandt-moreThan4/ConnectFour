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

