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