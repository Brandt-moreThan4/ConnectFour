import pandas as pd
import logging
import json
from datetime import datetime
import time
import random
import uuid

# import constants as constants
from game import Game
from board import Board
from player import  RandomNotStupidPlayer, RandomNaivePlayer
import player



def setup_logging() -> None:
    '''Set up logging for the simulation which will log to a file and the terminal.'''
    LOG_FILE = 'simulation.log'
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filemode='w')

    # Add a handler to log to the terminal as well
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(console_handler)



def run_simulation_arena(output_file:str,simulation_count:int,checkpoints=500) -> None:

    # stupid_player = player.RandomNaivePlayer('Stupid',token=None)
    # not_stupid_player = player.RandomNotStupidPlayer('Not Stupid',token=None)
    monty_50 = player.MonteCarloPlayer('Monty50',token=None,simulations=50)
    # monty_100 = player.MonteCarloPlayer('Monty100',token=None,simulations=100)
    # monty_200 = player.MonteCarloPlayer('Monty200',token=None,simulations=200)
    # monty_500 = player.MonteCarloPlayer('Monty500',token=None,simulations=500)
    # monty_1000 = player.MonteCarloPlayer('Monty1000',token=None,simulations=1000)
    monty_150 = player.MonteCarloPlayer('Monty150',token=None,simulations=150)
    monty_200 = player.MonteCarloPlayer('Monty149',token=None,simulations=200)
    monty_51 = player.MonteCarloPlayer('Monty51',token=None,simulations=51) 


    # arena = [stupid_player,not_stupid_player,monty_50,monty_100,monty_200,monty_500,monty_1000]
    arena = [monty_150,monty_200]
    arena = [monty_50,monty_51]

    all_game_data = []
    for i in range(simulation_count):

        # Draw two players randomly and give them their tokens
        player_1, player_2 = random.sample(arena,2)
        player_1.token = Board.TOKEN_1
        player_2.token = Board.TOKEN_2

        game = Game(p1=player_1, p2=player_2)

        while not game.is_over:
            game.play_turn()
            game.check_for_win()

        all_game_data.append(game.game_data.to_dict())
        logging.info(f'Simulation {i+1} done')

        if i % checkpoints == 0:
            logging.info(f'Checkpoint: {i} simulations done')
            with open(output_file,'w') as f:
                json.dump(all_game_data,f)

    with open(output_file,'w') as f:
        json.dump(all_game_data,f)        

if __name__ == '__main__':
    DATA_FILE = 'model_training/data/simulation_data_testing.json'
    DATA_FILE = 'model_training/data/arena_simulation2.json'    
    NUMBER_OF_GAMES = 10_000
    CHECK_POINTS = 100
    setup_logging()
    run_simulation_arena(output_file=DATA_FILE,simulation_count=NUMBER_OF_GAMES,checkpoints=CHECK_POINTS)

    # print('!!! Simulation Done!!!')
