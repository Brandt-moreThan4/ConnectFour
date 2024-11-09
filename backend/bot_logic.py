import random

def get_bot_move(board):
    # Generate a list of available columns (not full)
    columns = len(board[0])
    # If the top row of the board is None, the column is not full
    available_cols = [col for col in range(columns) if board[0][col] is None]

    # Randomly select a column for now
    if available_cols:
        return random.choice(available_cols)
    else:
        return None  # No moves available (game might be over)
