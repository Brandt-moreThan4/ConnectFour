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



    def display_board(self, player1_color='red', player2_color='yellow', empty_color='white', line_color='black'):
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