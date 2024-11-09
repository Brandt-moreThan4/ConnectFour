from player import Player
from board import Board


class Game:
    def __init__(self,p1:Player,p2:Player):
        self.p1 = p1
        self.p2 = p2
        self.is_over = False
        self.board = Board()

    def play_turn(self):
        raise NotImplementedError
        