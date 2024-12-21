import random
from pathlib import Path
import sys


from game_mechanics.board import Board
from game_mechanics import player


AVAILABLE_PLAYERS = {
    'random_naive': player.RandomNaivePlayer('Random',token=None),
    'random_not_stupid': player.RandomNotStupidPlayer('Random Not Stupid',token=None),
    'monty_50':player.MonteCarloPlayer('Monty 50',token=None, simulations=50),
    'monty_100':player.MonteCarloPlayer('Monty 100',token=None, simulations=100),
    'monty_200':player.MonteCarloPlayer('Monty 200',token=None, simulations=200),
    'monty_500':player.MonteCarloPlayer('Monty 500',token=None, simulations=500),
}



def get_bot_move(board_data) -> int | None:
    

    board = Board.from_lists(board_data)
    # bot_player = player.RandomNotStupidPlayer('bot', 2)
    bot_player = player.MonteCarloPlayer('bot', 2, 100)

    # Randomly select a column for now
    if board.is_full():
        return None  # No moves available (game might be over)
    else:
        col_to_play = int(bot_player.get_move(board))
        return col_to_play
    
