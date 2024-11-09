import logging
import simulation_params
from game import Game
from player import Player


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
    game_data = []
    for i in range(simulation_params.NUMBER_OF_GAMES):
        logging.info(f'Simulation {i+1} started')

        # Initialize the game
        player_1 = Player()
        player_2 = Player()
        game = Game(player_1, player_2)
        while not game.is_over():
            game.save_state()
            game.play_turn()
        game.save_state()
        game_data.append(game.get_data())



        logging.info(f'Simulation {i+1} done')



if __name__ == '__main__':
    setup_logging()

    run_simulations()

    # print('!!! Simulation Done!!!')
