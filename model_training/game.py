import pandas as pd
import logging
from dataclasses import dataclass, field
from datetime import datetime
import time
import random
import uuid

# from player import Player
# from board import Board
from model_training.player import Player
from model_training.board import Board


@dataclass
class GameData:
    game_id: str
    player_one_id: str
    player_two_id: str
    first_mover_id: str
    winner_id: str = ''
    moves: list[int] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime = None

    @property
    def turns(self) -> int:
        return len(self.moves)

    def to_dict(self) -> dict:
        return {
            'game_id': self.game_id,
            'player_one_id': self.player_one_id,
            'player_two_id': self.player_two_id,
            'winner_id': self.winner_id,
            'first_mover_id': self.first_mover_id,
            'moves': self.moves,
            'turns': self.turns,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() 
        }



class Game:
    def __init__(self,p1:Player,p2:Player):
        self.p1 = p1
        self.p2 = p2
        self.is_over = False
        self.board = Board()
        self.current_player = p1
        self.game_data = GameData(player_one_id=p1.player_id,player_two_id=p2.player_id,game_id=self.get_game_id(),first_mover_id=p1.player_id)


    def play_turn(self):

        col_chosen = self.current_player.get_move(self.board)
        self.board.make_move(col_chosen,self.current_player.token)      
        self.game_data.moves.append(col_chosen)
        self.switch_player()
        
    
    def switch_player(self):
        self.current_player = self.p1 if self.current_player == self.p2 else self.p2
    
    
    def check_for_win(self) -> bool:

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
            self.game_data.winner_id = winner.player_id
            self.game_data.end_time = datetime.now()
            return True
        
        # Check for tie
        if self.board.is_full():
            self.is_over = True
            self.game_data.winner_id = 'Tie'
            self.game_data.end_time = datetime.now()            
            return True
        
        return False
    
    def get_game_id(self) -> str:
        # Get current timestamp with microsecond precision
        timestamp = int(time.time() * 1_000_000)
        
        # Generate a random number
        random_num = random.randint(0, 999999)
        
        # Get a portion of a UUID
        uuid_part = uuid.uuid4().hex[:8]
        
        # Combine all parts
        unique_id = f"{timestamp:015d}-{random_num:06d}-{uuid_part}"
        
        return unique_id