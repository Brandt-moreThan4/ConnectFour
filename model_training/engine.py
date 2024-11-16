import pandas as pd
import logging
import json

# import constants as constants
from game import Game
from player import Player, RandomPlayer1, RandomPlayer2


def setup_logging() -> None:
    '''Set up logging for the simulation which will log to a file and the terminal.'''
    LOG_FILE = 'simulation.log'
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Add a handler to log to the terminal as well
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(console_handler)




def run_simulations() -> None:
    NUMBER_OF_GAMES = 5
    logging.info('Simulation started')
    all_game_data = []
    for i in range(NUMBER_OF_GAMES):
        logging.info(f'Simulation {i+1} started')

        player_1 = RandomPlayer1('Player 1',token=1)
        player_2 = RandomPlayer2('Player 2',token=2)
        game = Game(player_1, player_2)
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
