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