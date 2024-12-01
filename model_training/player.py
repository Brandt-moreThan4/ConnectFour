# import tensorflow as tf
from pathlib import Path

from model_training.board import Board
from model_training.mcts import monte_carlo_tree_search

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_FOLDER = PROJECT_ROOT / 'model_training' / 'models'

class Player:
    def __init__(self, name: str, token: int) -> None:
        self.name = name
        self.token = token # Should be unique. Represented by 1 or 2

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name

    def get_move(self, board: Board) -> int:
        move = self._get_move(board)
        return int(move)
    
    def _get_move(self, board: Board):
        raise NotImplementedError
    
    @property
    def player_id(self) -> str:
        raise NotImplementedError
    

class RandomNaivePlayer(Player):
    
    @property
    def player_id(self) -> str:
        return 'random_naive'

    def _get_move(self, board: Board) -> int:
        return board.get_random_move()

class RandomNotStupidPlayer(Player):

    @property
    def player_id(self) -> str:
        return 'random_not_stupid'

    def _get_move(self, board: Board) -> int:
        obvious_move = board.check_for_obvious_move(self.token)
        if obvious_move is not None:
            return obvious_move
        else:
            return board.get_random_move()
    

class MonteCarloPlayer(Player):
    def __init__(self, name: str, token: int, simulations: int) -> None:
        super().__init__(name, token)
        self.simulations = simulations
    
    @property
    def player_id(self) -> str:
        return f'monte_carlo_{self.simulations}'
    
    def _get_move(self, board: Board) -> int:
        move = board.check_for_obvious_move(self.token)
        if move is None:
            move = monte_carlo_tree_search(board, perspective_token=self.token,itermax=self.simulations)
        return move
    

class Mod_2(Player):
    def __init__(self, name: str, token: int) -> None:
        super().__init__(name, token)
        self._load_model('mod_2.keras')
    
    @property
    def player_id(self) -> str:
        return 'mod_2'
    
    def _get_move(self, board: Board) -> int:
        move = board.check_for_obvious_move(self.token)

        if move is not None:
            return move

        # Otherwise we need to use the model to predict the best move
        # Look at available moves
        # Use the model to predict reward associated with each move
        # Choose the move with the highest reward
        available_moves = board.get_playable_cols()
        predicted_rewards = []
        for move in available_moves:
            new_board = board.get_copy()
            new_board.make_move(move, self.token)
            # Get the board grid in the format expected by the model
            board_state = new_board.convert_to_plus_minus(turn_token=self.token)
            board_state_tensor = board_state.reshape(1, 6, 7, 1)
            predicted_reward = self.model.predict(board_state_tensor)[0][0]
            predicted_rewards.append(predicted_reward)
        
        best_move = available_moves[predicted_rewards.index(max(predicted_rewards))]
        return best_move
    
    def _load_model(self, mod_name: str):
        mod_name = MODELS_FOLDER / mod_name
        # self.model = tf.keras.models.load_model(mod_name)
