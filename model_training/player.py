from .board import Board

class Player:
    def __init__(self, name: str,token:int) -> None:
        self.name = name
        # self.color = color
        self.token = token

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name

    def get_move(self, board:Board) -> int:
        raise NotImplementedError
    

class RandomPlayer(Player):
    def get_move(self, board:Board) -> int:
        return board.get_random_move()