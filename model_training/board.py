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