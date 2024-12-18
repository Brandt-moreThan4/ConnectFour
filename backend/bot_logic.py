import random
from pathlib import Path
import sys


from game_mechanics.board import Board
from game_mechanics import player


def get_bot_move(board) -> int | None:
    
    # Generate a list of available columns (not full)
    columns = len(board[0])

    # If the top row of the board is None, the column is not full
    available_cols = [col for col in range(7) if board[0][col] is None]

    # Randomly select a column for now
    if available_cols:
        return random.choice(available_cols)
    else:
        return None  # No moves available (game might be over)


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
    
# def get_bot_move(board_data) -> int | None:
    

#     board = Board.from_lists(board_data)
#     # bot_player = player.RandomNotStupidPlayer('bot', 2)
#     bot_player = player.Mod_2('bot', 2)

#     # Randomly select a column for now
#     if board.is_full():
#         return None  # No moves available (game might be over)
#     else:
#         col_to_play = bot_player.get_move(board)
#         return col_to_play

