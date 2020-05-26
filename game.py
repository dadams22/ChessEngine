""" This file should be run using python3 to start the game. """
import chess
from engine import *

class GameRunner():
    """ Object to be created to run the game and store data. """
    def __init__(self):
        # Sets the board to a default board and sets the first turn to white
        self.board = chess.Board()
        self.whose_turn = chess.WHITE

    def print_board(self):
        print('\n     BLACK')
        print(self.board)
        print('     WHITE')

    def determine_player_types(self):
        """
        Gets input from the user as to whether white and black should each be
        played by a computer or human.
        """
        # Ask the user whether a user would like to play white until a 'Y' or 'N'
        # response is received
        white_is_human = ''
        while white_is_human.upper() != 'Y' and white_is_human.upper() != 'N':
            white_is_human = input(
                'Would a user like to play white?  Y or N: '
            )

        # If Y, set white_player to a Human instance
        if white_is_human.upper() == 'Y':
            self.white_player = Human(self.board, chess.WHITE)
        # If N, set white_player to an Engine instance
        else:
            self.white_player = Engine(self.board, chess.WHITE)

        # Ask the user whether a user would like to play black until a 'Y' or 'N'
        # response is received
        black_is_human = ''
        while black_is_human.upper() != 'Y' and black_is_human.upper() != 'N':
            black_is_human = input(
                'Would a user like to play black?  Y or N: '
            )
        # If Y, set black_player to a Human instance
        if black_is_human.upper() == 'Y':
            self.black_player = Human(self.board, chess.BLACK)
        # If N, set black_player to a Human instance
        else:
            self.black_player = Engine(self.board, chess.BLACK)

    def run_half_turn(self):
        """ Runs a half turn, or a single player's move. """
        if self.whose_turn == chess.WHITE:
            print('\n\nWHITE TURN:')
            # Call the make move method of white_player, whether it is an Engine
            # or Human
            self.white_player.make_move()
            # Set whos_turn to the other player to prepare for the next turn
            self.whose_turn = chess.BLACK

        elif self.whose_turn == chess.BLACK:
            print('\n\nBLACK TURN:')
            # Call the make move method of black_player, whether it is an Engine
            # or Human
            self.black_player.make_move()
            # Set whos_turn to the other player to prepare for the next turn
            self.whose_turn = chess.WHITE

        self.print_board()

    def run_game(self):
        """
        This method should be called to run the whole game.
        It should be the only method called from GameRunner.
        It will not cease execution until the game has been completed.
        """
        # Determine the types of each player (Human or Engine) before starting
        # the game
        self.determine_player_types()
        self.print_board()

        # As long as the game is not over (a checkmate, stalemate or draw has
        # not happened), run a half turn of the game
        while not self.board.is_game_over():
            self.run_half_turn()

        # If the game is over, print the result and the winner
        result = self.board.result()
        print()
        if result == '1-0':
            print('WHITE VICTORY')
        elif result == '0-1':
            print('BLACK VICTORY')
        elif result == '1/2-1/2':
            print('DRAW')


if __name__ == '__main__':
    # When game.py is run, a GameRunner instance will be created and the game
    # will be run by calling the run_game method
    game_runner = GameRunner()
    game_runner.run_game()
