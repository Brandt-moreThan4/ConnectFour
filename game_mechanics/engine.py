import pandas as pd
import logging
import json
import random
from typing import Union
from pathlib import Path

from game_mechanics import player
from game_mechanics.game import Game, GameData
from game_mechanics.board import Board


# Big bank of players that may be needed in simulations
stupid_player = player.RandomNaivePlayer('Stupid',token=None)
not_stupid_player = player.RandomNotStupidPlayer('Not Stupid',token=None)
monty_50 = player.MonteCarloPlayer('Monty50',token=None,simulations=50)
monty_100 = player.MonteCarloPlayer('Monty100',token=None,simulations=100)
monty_200 = player.MonteCarloPlayer('Monty200',token=None,simulations=200)
monty_500 = player.MonteCarloPlayer('Monty500',token=None,simulations=500)
monty_1000 = player.MonteCarloPlayer('Monty1000',token=None,simulations=1000)
monty_150 = player.MonteCarloPlayer('Monty150',token=None,simulations=150)
monty_200 = player.MonteCarloPlayer('Monty149',token=None,simulations=200)
monty_51 = player.MonteCarloPlayer('Monty51',token=None,simulations=51) 
mod_2 = player.Mod_2('Mod_2',token=None)


def setup_logging() -> None:
    '''Set up logging for the simulation which will log to a file and the terminal.'''
    LOG_FILE = 'simulation.log'
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filemode='w')

    # Add a handler to log to the terminal as well
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(console_handler)


class DataBase:

    def __init__(self,master_file:str='data/master_db.json') -> None:
        self.master_file = master_file
        self.load()
        
    def load(self) -> pd.DataFrame:
        path = Path(self.master_file)
        if not path.exists():
            logging.info(f'No database found at {self.master_file}. Creating new database')
            self.data = []
            self.save()

        with open(self.master_file,'r') as f:
            data = json.load(f)
        self.data:list = data

    def save(self,file_path:str=None) -> None:
        file = file_path if file_path else self.master_file
        with open(file,'w') as f:
            json.dump(self.data,f,indent=4)
    
    def add_data(self,new_data:list[dict],save:bool=True) -> None:
        self.data.extend(new_data)
        if save:
            self.save()
    
    def __repr__(self):
        return f'DataBase({self.master_file}) - {len(self.data)} records'

    def __str__(self):
        return f'DataBase({self.master_file}) - {len(self.data)} records'


def play_game(p1:player.Player,p2:player.Player) -> Game:

    # Make sure the players have their tokens set
    p1.token = Board.TOKEN_1
    p2.token = Board.TOKEN_2

    game = Game(p1=p1,p2=p2)

    while not game.is_over:
        game.play_turn()
        game.check_for_win()

    return game

def run_simulations(p1:player.Player,p2:player.Player,sim_count:int=100,randomize_order:bool=True) -> list[GameData]:
    all_game_data = []
    for i in range(sim_count):
        if randomize_order:
            p1,p2 = random.sample([p1,p2],2)

        game = play_game(p1,p2)
        all_game_data.append(game.game_data)
        # logging.info(f'Simulation {i+1} done')
    return all_game_data


def evaluate_player(player:player.Player, opponent:player.Player, sim_count:int=30) -> dict:
    ''' Evaluate a player against an opponent. '''

    data = run_simulations(player,opponent,sim_count)

    df = pd.DataFrame([game_data.to_dict() for game_data in data])
    win_rates = df['winner_id'].value_counts(normalize=True)

    return {
        'win_rate':win_rates.get(player.player_id,0),
        'loss_rate':win_rates.get(opponent.player_id,0),
        'tie_rate':win_rates.get('Tie',0),
    }


def run_simulation_arena(arena_players:list[player.Player],simulation_count:int, data_db:DataBase=None,checkpoints=500) -> None:

    all_game_data = []
    for i in range(simulation_count):

        player_1, player_2 = random.sample(arena_players,2)
        game = play_game(player_1,player_2)

        all_game_data.append(game.game_data.to_dict())
        logging.info(f'Simulation {i+1} done')

        if i % checkpoints == 0 and data_db is not None:
            logging.info(f'Checkpoint Reached: {i} simulations done')
            data_db.add_data(all_game_data)
            all_game_data = []

    if data_db is not None:
        data_db.add_data(all_game_data)     
    
    return all_game_data
        

if __name__ == '__main__':
    setup_logging()
    DATA_FILE = 'data/master_db.json'
    # DATA_FILE = 'model_training/data/combined_toy.json'   
    database = DataBase(DATA_FILE) 
    NUMBER_OF_GAMES = 50_000
    CHECK_POINTS = 100

    players = [monty_100,monty_1000]
    players = [monty_50,monty_100]
    players = [monty_50,monty_150]
    players = [monty_50,monty_51,monty_100,monty_150,monty_200,monty_500,monty_1000]    
    # players = [monty_50,mod_2]

    # run_simulation_arena(players,NUMBER_OF_GAMES,data_db=database,checkpoints=CHECK_POINTS)
    # run_simulation_arena(players,simulation_count=10)
    # data = run_simulations(monty_50,monty_100,sim_count=10)
    # stats = simulation_stats(data)
    # eval = evaluate_player(monty_50,monty_150,sim_count=10)

    print('All done!')