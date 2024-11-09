import pandas as pd
import logging
import simulation_params
from game import Game
from player import Player, RandomPlayer


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
    logging.info('Simulation started')
    all_game_data = []
    for i in range(simulation_params.NUMBER_OF_GAMES):
        logging.info(f'Simulation {i+1} started')

        # Initialize the game
        player_1 = RandomPlayer('Player 1',token=1)
        player_2 = RandomPlayer('Player 2',token=2)
        game = Game(player_1, player_2)
        while not game.is_over:
            # game.save_state()
            game.play_turn()
            game.check_for_win()
        if game.winner != 'Tie':
            logging.info(f'The winner of the game was {game.winner}!')
        game_data = game.get_data()
        game_data['game_id'] = i
        # game_data['winner'] = game.winner
        all_game_data.append(game_data)


        logging.info(f'Simulation {i+1} done')

    all_game_data = pd.concat(all_game_data)
    all_game_data.to_csv('model_training/data/simulation_data.csv',index=False)


if __name__ == '__main__':
    setup_logging()

    run_simulations()

    # print('!!! Simulation Done!!!')
