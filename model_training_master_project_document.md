# Project Master File

## Project Structure

```
├── __init__.py
├── board.py
├── engine.py
├── game.py
├── models
│   └── mod_2.keras
├── player.py
└── utils.py
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



    def convert_to_plus_minus(self,turn_token=None) -> np.ndarray:
        """
        Convert the board grid to a 2D numpy array with:
        +1 for the current player's token,
        -1 for the opponent's token,
        0 for empty cells.
        """

        if turn_token is None:
            turn_token = self.turn_token

        # Map the tokens directly in a single step
        token_map = {turn_token: 1, switch_token(turn_token): -1, 0: 0}
        vectorized_map = np.vectorize(token_map.get)  # Efficient mapping
        new_grid = vectorized_map(self.grid)
        return new_grid

    @staticmethod
    def make_boards_from_moves(moves:list) -> list['Board']:
        '''Create a list of Board objects based on a list of moves.'''

        boards = [Board.from_turn_sequence(moves[:i]) for i in range(1, len(moves)+1)]
        # Add on the initial empty board
        boards = [Board()] + boards
        return boards


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

    # board.display_board()
    new_grid = board.convert_to_plus_minus()

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

from model_training import player
from model_training.game import Game, GameData
from model_training.board import Board
# from game import Game, GameData
# from board import Board
# import player

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

mod_2 = player.Mod_2('Mod_2',token=None)


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




def run_simulation_arena(arena_players:list[player.Player],simulation_count:int, data_db:DataBase=None,checkpoints=500) -> None:

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
    players = [monty_50,monty_150]
    players = [monty_50,monty_51,monty_100,monty_150,monty_200,monty_500,monty_1000]    
    players = [monty_50,mod_2]

    # run_simulation_arena(players,NUMBER_OF_GAMES,data_db=database,checkpoints=CHECK_POINTS)
    run_simulation_arena(players,simulation_count=10)


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

# from player import Player
# from board import Board
from model_training.player import Player
from model_training.board import Board


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
# import tensorflow as tf
from pathlib import Path
# from board import Board, simulate_game, monte_carlo_tree_search
# from .board import Board, simulate_game, monte_carlo_tree_search
from model_training.board import Board, simulate_game, monte_carlo_tree_search

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_FOLDER = PROJECT_ROOT / 'model_training' / 'models'

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
    

class Mod_2(Player):
    def __init__(self, name: str, token: int) -> None:
        super().__init__(name, token)
        self._load_model('mod_2.keras')
    
    @property
    def player_id(self) -> str:
        return 'mod_2'
    
    def _get_move(self, board: Board) -> int:
        move = board.check_for_obvious_move(self.token)

        if move is not None:
            return move

        # Otherwise we need to use the model to predict the best move
        # Look at available moves
        # Use the model to predict reward associated with each move
        # Choose the move with the highest reward
        available_moves = board.get_playable_cols()
        predicted_rewards = []
        for move in available_moves:
            new_board = board.get_copy()
            new_board.make_move(move, self.token)
            # Get the board grid in the format expected by the model
            board_state = new_board.convert_to_plus_minus(turn_token=self.token)
            board_state_tensor = board_state.reshape(1, 6, 7, 1)
            predicted_reward = self.model.predict(board_state_tensor)[0][0]
            predicted_rewards.append(predicted_reward)
        
        best_move = available_moves[predicted_rewards.index(max(predicted_rewards))]
        return best_move
    
    def _load_model(self, mod_name: str):
        mod_name = MODELS_FOLDER / mod_name
        # self.model = tf.keras.models.load_model(mod_name)

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\utils.py

```py

```

## C:\Users\User\OneDrive\Desktop\Code\ConnectFour\model_training\__init__.py

```py
# print('Model Training Package Initialized')
from .board import Board
from .player import Player

# from board import Board
# from player import Player

# from model_training import board
# from model_training import player
```

