import numpy as np
import random

from model_training.board import Board



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

    other_token = Board.switch_token(perspective_token)

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
        turn_token = Board.switch_token(turn_token)

    # Check for win, loss or tie and distribute points accordingly
    if board.check_winner(perspective_token):
        return 1
    elif board.check_winner(other_token):
        return -1
    else:
        return 0 