import numpy as np
import random
# from player import Player
from typing import Union
import matplotlib.pyplot as plt

# Feels sloppy?
TOKEN_MAP = {'red':1,'yellow':2,'black':2}
ROWS, COLUMNS = 6,7

class Board:

    TOKEN_1 = 1
    TOKEN_2 = 2

    def __init__(self) -> None:
        self.grid = np.zeros((ROWS, COLUMNS), dtype=int)
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
        
        # Set the appropriate turn token
        board.turn_token = 2 if board.turn % 2 == 0 else 1

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
        self.turn_token = self.switch_token(token)
    
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
        n_rows, n_cols = ROWS, COLUMNS

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



    def convert_to_plus_minus(self,perspective=None) -> np.ndarray:
        """
        Convert the board grid to a 2D numpy array with:
        +1 for the current player's token,
        -1 for the opponent's token,
        0 for empty cells.
        """

        if perspective is None:
            perspective = self.turn_token

        # Map the tokens directly in a single step
        token_map = {perspective: 1, self.switch_token(perspective): -1, 0: 0}
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

    @staticmethod
    def switch_token(token:int) -> int:
        '''Switch the token from 1 to 2 and vice versa.'''
        return Board.TOKEN_1 if token == Board.TOKEN_2 else Board.TOKEN_2    




    

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

