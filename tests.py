import chess
from game import *
from engine import *
import unittest
import time
import random


class EngineTest(unittest.TestCase):
    # def test_piece_valuation(self):
    #     board = chess.Board()
    #     color = chess.BLACK
    #     engine = Engine(board, color)
    #     self.assertEqual(engine.own_piece_values(), 39)
    #     self.assertEqual(engine.opponent_piece_values(), 39)
    #
    #     board.set_board_fen('rnbqkbN1/ppP3pp/5n2/3B4/1p2P3/8/P2P1PPP/RNB1K2R')
    #     expected_black_piece_val = 31
    #     observed_black_piece_val = engine.own_piece_values()
    #     self.assertEqual(expected_black_piece_val, observed_black_piece_val)
    #     expected_white_piece_val = 29
    #     observed_white_piece_val = engine.opponent_piece_values()
    #     self.assertEqual(expected_white_piece_val, observed_white_piece_val)

    def test_invert_index(self):
        board = chess.Board()
        engine = Engine(board, chess.WHITE)
        self.assertEqual(engine.invert_index(0), 63)
        self.assertEqual(engine.invert_index(63), 0)
        self.assertEqual(engine.invert_index(25), 38)


# class ChessLibraryTest(unittest.TestCase):
#     def test_board_push_and_pop_speed(self):
#         num_trials = 100000
#         board = chess.Board()
#         start_time = time.time()
#
#         for i in range(num_trials):
#             possible_moves = [move for move in board.legal_moves]
#             move = random.choice(possible_moves)
#             board.push(move)
#             board.pop()
#
#         end_time = time.time()
#         duration = round(end_time - start_time, 4)
#         print()
#         print(str(num_trials) + ' trials done in ' + str(duration) + 's')
#         print()


# class GameRunnerTest(unittest.TestCase):
#     def test_determine_player_types(self):
#         game_runner = GameRunner()
#         print('Enter white as Y and Black as N')
#         game_runner.determine_player_types()
#         self.assertEqual(type(game_runner.white_player), Human)
#         self.assertEqual(type(game_runner.black_player), Engine)


if __name__ == '__main__':
    unittest.main()
