import chess
import time
from engine import *

num_trials = 100000

board = chess.Board()
engine = Engine(board, chess.WHITE)

trials_done = 0
start_time = time.time()
while trials_done < num_trials:
        possible_moves = [move for move in board.legal_moves]
        for move in possible_moves:
            board.push(move)
            # engine.board_value()
            board.pop()
            trials_done += 1

end_time = time.time()
duration = end_time - start_time
print(str(num_trials) + ' trials done in ' + str(round(duration, 3)) + 's')

avg_milliseconds = duration / trials_done * 1000
print(str(avg_milliseconds) + 'ms per trial')
