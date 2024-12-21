import random
from pathlib import Path
import sys


from game_mechanics.board import Board
from game_mechanics import player


TOKEN_MAP = {'red':1,'black':2}

AVAILABLE_PLAYERS = {
    'random_naive': player.RandomNaivePlayer('Random',token=None),
    'random_not_stupid': player.RandomNotStupidPlayer('Random Not Stupid',token=None),
    'monty_50':player.MonteCarloPlayer('Monty 50',token=None, simulations=50),
    'monty_100':player.MonteCarloPlayer('Monty 100',token=None, simulations=100),
    'monty_200':player.MonteCarloPlayer('Monty 200',token=None, simulations=200),
    'monty_500':player.MonteCarloPlayer('Monty 500',token=None, simulations=500),
}




def get_bot_move(data:dict) -> int | None:
    
    # Grab the data from the JSON payload
    board_data = data['board']
    player_tag = data['player']
    bot_id = data['bot_id']


    # Create the board object & the bot player from the game mechanics
    board = Board.from_lists(board_data)
    bot_player = create_player(player_tag, bot_id)


    if board.is_full():
        return None  # No moves available (game might be over)
        # Hoonestly don't think this is necessary anymore. I think the frontend should handle this.
    else:
        col_to_play = int(bot_player.get_move(board))
        return col_to_play
    

def create_player(player_id:str, bot_id:str) -> player.Player:
    player = AVAILABLE_PLAYERS[bot_id]
    player.token = TOKEN_MAP[player_id]

    return player

