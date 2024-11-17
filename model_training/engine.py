import pandas as pd
import logging
import json
from datetime import datetime
import time
import random
import uuid

# import constants as constants
from game import Game
from player import  RandomNotStupidPlayer, RandomNaivePlayer
import player


CHECK_POINTS = 200

def setup_logging() -> None:
    '''Set up logging for the simulation which will log to a file and the terminal.'''
    LOG_FILE = 'simulation.log'
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filemode='w')

    # Add a handler to log to the terminal as well
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    # logging.getLogger().addHandler(console_handler)


def get_game_id() -> str:
    # Get current timestamp with microsecond precision
    timestamp = int(time.time() * 1_000_000)
    
    # Generate a random number
    random_num = random.randint(0, 999999)
    
    # Get a portion of a UUID
    uuid_part = uuid.uuid4().hex[:8]
    
    # Combine all parts
    unique_id = f"{timestamp:015d}-{random_num:06d}-{uuid_part}"
    
    return unique_id


def run_simulations(output_file:str,simulation_count:int) -> None:

    all_game_data = []
    for i in range(simulation_count):
        # logging.info(f'Simulation {i+1} started')

        # player_a = RandomPlayer1('Player 1',token=1)
        # player_b = RandomPlayer2('Player 2',token=2)        
        player_a = player.MonteCarloPlayer('Player 1',token=1,simulations=100)
        player_b = RandomNotStupidPlayer('Player 1',token=2)

        game_id = get_game_id()

        # Alternate the starting player
        if i % 2 == 0:
            game = Game(p1=player_a, p2= player_b, game_id=game_id)
        else:
            game = Game(p1=player_b, p2=player_a, game_id=game_id)
        while not game.is_over:
            game.play_turn()
            game.check_for_win()

        all_game_data.append(game.game_data.to_dict())
        logging.info(f'Simulation {i+1} done')

        if i % CHECK_POINTS == 0:
            logging.info(f'Checkpoint: {i} simulations done')
            with open(output_file,'w') as f:
                json.dump(all_game_data,f)

    with open(output_file,'w') as f:
        json.dump(all_game_data,f)

if __name__ == '__main__':
    DATA_FILE = 'model_training/data/simulation_data_testing.json'
    DATA_FILE = 'model_training/data/simulation_data_testing.json'    
    NUMBER_OF_GAMES = 2000
    setup_logging()
    run_simulations(output_file=DATA_FILE,simulation_count=NUMBER_OF_GAMES)

    # print('!!! Simulation Done!!!')
