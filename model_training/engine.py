import pandas as pd
import logging
import json
from datetime import datetime
import time
import random
import uuid

# import constants as constants
from game import Game
from player import Player, RandomPlayer1, RandomPlayer2


def setup_logging() -> None:
    '''Set up logging for the simulation which will log to a file and the terminal.'''
    LOG_FILE = 'simulation.log'
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Add a handler to log to the terminal as well
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    # logging.getLogger().addHandler(console_handler)


def get_game_id() -> str:
    return datetime.now().strftime('%Y%m%d%H%M%S%f')



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

def run_simulations() -> None:
    NUMBER_OF_GAMES = 50_000
    logging.info('Simulation started')
    all_game_data = []
    for i in range(NUMBER_OF_GAMES):
        logging.info(f'Simulation {i+1} started')

        player_1 = RandomPlayer1('Player 1',token=1)
        player_2 = RandomPlayer2('Player 2',token=2)
        game_id = get_game_id()
        game = Game(player_1, player_2,game_id=game_id)
        while not game.is_over:
            game.play_turn()
            game.check_for_win()

        all_game_data.append(game.game_data.to_dict())

        logging.info(f'Simulation {i+1} done')


    DATA_FILE = 'model_training/data/simulation_data.json'
    with open(DATA_FILE,'w') as f:
        json.dump(all_game_data,f)

if __name__ == '__main__':
    # setup_logging()

    run_simulations()

    # print('!!! Simulation Done!!!')
