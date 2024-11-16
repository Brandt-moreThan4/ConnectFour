from board import Board

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
    

class RandomPlayer1(Player):

    @property
    def player_id(self) -> str:
        return 'random_move_1'

    def _get_move(self, board: Board) -> int:
        return board.get_random_move()
    
class RandomPlayer2(Player):
    
    @property
    def player_id(self) -> str:
        return 'random_move_2'

    def _get_move(self, board: Board) -> int:
        return board.get_random_move()