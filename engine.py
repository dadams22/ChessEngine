import chess
import random
import time
import json
import multiprocessing.dummy

class Player:
    """
    This class represents a single player playing either the white or black
    pieces.
    Superclass of both Human and Engine classes.
    """
    def __init__(self, board, color):
        # Set the board attribute to the board being used for the game
        self.board = board
        # Set the color to the appropriate setting, wither chess.WHITE or
        # chess.BLACK
        self.color = color

    def generate_move(self):
        """
        Must be overridden.
        This method should return a move object.  It will be used to get the
        requested move of the player whether it is a Human or Engine.
        """
        raise NotImplementedError('generate_move must be implemented')

    def make_move(self):
        """
        Gets the requested move using the generate_move method, then pushes this
        move to the board being used by GameRunner.
        """
        move = self.generate_move()
        self.board.push(move)


class Human(Player):
    """ Represents a player being played by a human. """
    def __init__(self, board, color):
        super().__init__(board, color)

    def get_move_input(self):
        """
        Asks the user what move they would like to make, and if valid, returns
        the move as a Move instance.
        """
        try:
            # Get a string representation of a move from the user in SAN
            move_san = input('Enter a valid move in SAN: ')
            # Try converting the SAN to a Move instance
            move = self.board.parse_san(move_san)
        # If an error is raised, call the method again recursively
        except ValueError:
            print('Not a valid move.\n')
            move = self.get_move_input()

        return move

    def generate_move(self):
        """
        Asks the user what move they would like to make using get_move_input.
        Returns a legal move as a Move instance.
        Overrides generate_move in Player.
        """
        move = self.get_move_input()
        # Make sure the move is legal given the board position
        # If not legal, call generate_move again to get another move to try
        if move not in self.board.legal_moves:
            print('Not a valid move.\n')
            move = self.generate_move()

        return move



class Engine(Player):
    """ Represents a Player played by the computer. """
    def __init__(self, board, color):
        super().__init__(board, color)

        # Since game is just starting, we are in the opening and not middle_game
        self.is_opening = True
        self.is_middle_game = False

        # Set the piece values to some generally accepted constants
        self.PIECE_VALUES = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3.2,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 200,
        }

        # Load the openings, which are stored in a json file
        # Note: openings are stored as a list of dictionaries
        with open('json/openings.json', 'r') as openings_file:
            self.openings = json.load(openings_file)

        # Create a square value matrix for each piece type

        # This will encourage certain generally strong tactics to be played,
        # such as keeping the knights in the center and taking control of the
        # center with the pawns

        # Each matrix is stored as a single-dimensional list, since the Board
        # class of chess refers to each square using a single integer
        self.PIECE_SQUARES = {
            chess.PAWN: [
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                 0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1,
                 .05, .05, 0.1, .25, .25, 0.1, .05, .05,
                 0.0, 0.0, 0.0, 0.2, 0.2, 0.0, 0.0, 0.0,
                 .05,-.05,-0.1, 0.0, 0.0,-0.1,-.05, .05,
                 .05, 0.1, 0.1,-0.2,-0.2, 0.1, 0.1, .05,
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            ],
            chess.KNIGHT: [
                -0.5,-0.4,-0.3,-0.3,-0.3,-0.3,-0.4,-0.5,
                -0.4,-0.2, 0.0, 0.0, 0.0, 0.0,-0.2,-0.4,
                -0.3, 0.0, 0.1, .15, .15, 0.1, 0.0,-0.3,
                -0.3, .05, .15, 0.2, 0.2, .15, .05,-0.3,
                -0.3, 0.0, .15, 0.2, 0.2, .15, 0.0,-0.3,
                -0.3, .05, 0.1, .15, .15, 0.1, .05,-0.3,
                -0.4,-0.2, 0.0, .05, .05, 0.0,-0.2,-0.4,
                -0.5,-0.4,-0.3,-0.3,-0.3,-0.3,-0.4,-0.5,
            ],
            chess.BISHOP: [
                -0.2,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.2,
                -0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,-0.1,
                -0.1, 0.0, .05, 0.1, 0.1, .05, 0.0,-0.1,
                -0.1, .05, .05, 0.1, 0.1, .05, .05,-0.1,
                -0.1, 0.0, 0.1, 0.1, 0.1, 0.1, 0.0,-0.1,
                -0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,-0.1,
                -0.1, .05, 0.0, 0.0, 0.0, 0.0, .05,-0.1,
                -0.2,-0.1,-0.1,-0.1,-0.1,-0.1,-0.1,-0.2,
            ],
            chess.ROOK: [
                 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                 .05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, .05,
                -.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,-.05,
                -.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,-.05,
                -.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,-.05,
                -.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,-.05,
                -.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,-.05,
                 0.0, 0.0, 0.0, .05, .05, 0.0, 0.0, 0.0,
            ],
            chess.QUEEN: [
                -0.2,-0.1,-0.1,-.05,-.05,-0.1,-0.1,-0.2,
                -0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,-0.1,
                -0.1, 0.0, .05, .05, .05, .05, 0.0,-0.1,
                -.05, 0.0, .05, .05, .05, .05, 0.0,-.05,
                 0.0, 0.0, .05, .05, .05, .05, 0.0,-.05,
                -0.1, .05, .05, .05, .05, .05, 0.0,-0.1,
                -0.1, 0.0, .05, 0.0, 0.0, 0.0, 0.0,-0.1,
                -0.2,-0.1,-0.1,-.05,-.05,-0.1,-0.1,-0.2,
            ],
            chess.KING: [
                -0.3,-0.4,-0.4,-0.5,-0.5,-0.4,-0.4,-0.3,
                -0.3,-0.4,-0.4,-0.5,-0.5,-0.4,-0.4,-0.3,
                -0.3,-0.4,-0.4,-0.5,-0.5,-0.4,-0.4,-0.3,
                -0.3,-0.4,-0.4,-0.5,-0.5,-0.4,-0.4,-0.3,
                -0.2,-0.3,-0.3,-0.4,-0.4,-0.3,-0.3,-0.1,
                -0.1,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.1,
                 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2,
                 0.2, 0.3, 0.1, 0.0, 0.0, 0.1, 0.3, 0.2,
            ],
        }

        # Reverse every matrix so that the bottom right corner of each matrix is
        # indexed as 0 and the top left corner is indexed as 63
        for piece_square_matrix in self.PIECE_SQUARES.values():
            piece_square_matrix.reverse()

    def get_move_history(self, board=None):
        """
        Return the entire move history for the given board.
        If no argument is passed, self.board will be used as the board.
        """
        if board is None:
            board = self.board

        move_history = []
        flag = True
        while flag:
            try:
                move = board.pop()
            except:
                move = None
                flag = False

            if move != None:
                move_history.append(move)

        move_history.reverse()

        for move in move_history:
            board.push(move)
        return move_history

    def is_possible_opening(self, opening, move_history):
        try:
            opening_move_history = opening['m'][:len(move_history)]
        except:
            return False
        return opening_move_history == move_history and len(opening['m']) > len(move_history)

    def generate_opening_move(self):
        move_history = self.get_move_history()
        move_history = [str(move) for move in move_history]

        possible_openings = []
        for opening in self.openings:
            if self.is_possible_opening(opening, move_history):
                possible_openings.append(opening)

        if not possible_openings:
            return False
        else:
            random.shuffle(possible_openings)
            fewest_moves = min([len(opening['m']) for opening in possible_openings])
            closest_possible_openings = []
            for possible_opening in possible_openings:
                if len(possible_opening['m']) == fewest_moves:
                    closest_possible_openings.append(possible_opening)
            chosen_opening = random.choice(closest_possible_openings)
            return chosen_opening, chosen_opening['m'][len(move_history)]

    def invert_index(self, index):
        row = index // 8
        col = index % 8

        new_row = 7 - row
        new_col = 7 - col
        return new_row * 8 + new_col

    def piece_values(self, color, piece_map, board=None):
        total = 0
        for index, piece in piece_map.items():
            if piece.color == color:
                if piece.color == chess.BLACK:
                    index = self.invert_index(index)
                piece_value = self.PIECE_VALUES[piece.piece_type]
                square_value = self.PIECE_SQUARES[piece.piece_type][index]
                total += (piece_value + square_value)
        return total


    def evaluate_board(self, board=None):
        if board is None:
            board = self.board

        threefold_repetition = board.can_claim_threefold_repetition()
        if board.is_game_over():
            result = board.result()
            if result == '1-0':
                winner = chess.WHITE
            elif result == '0-1':
                winner = chess.BLACK
            elif result == '1/2-1/2' or three_fold_repetition:
                winner = None

            if winner == None:
                return 0
            elif winner == self.color:
                return 999
            elif winner != self.color:
                return -999
        else:
            piece_map = board.piece_map()
            own_piece_values = self.piece_values(self.color, piece_map, board)
            opponent_color = chess.WHITE if self.color == chess.BLACK else chess.BLACK
            opponent_piece_values = self.piece_values(opponent_color, piece_map)
            return own_piece_values - opponent_piece_values

    def minimax(self, depth, maximizing=True, alpha=-1000, beta=1000):
        self.calls_to_minimax += 1
        if self.calls_to_minimax % 1000 == 0:
            print(self.calls_to_minimax)

        if depth == 0 or self.board.is_game_over():
            self.board_evaluations += 1
            return (None, self.evaluate_board())

        if maximizing:
            best_move = (None, -1000)
            possible_moves = [move for move in self.board.legal_moves]
            for move in possible_moves:
                self.board.push(move)
                move_value = self.minimax(depth-.5, not maximizing)[1]
                self.board.pop()

                if move_value > best_move[1]:
                    best_move = (move, move_value)
                elif move_value == best_move[1]:
                    best_move = random.choice([best_move, (move, move_value)])

        elif not maximizing:
            best_move = (None, 1000)
            possible_moves = [move for move in self.board.legal_moves]
            for move in possible_moves:
                self.board.push(move)
                move_value = self.minimax(depth-.5, not maximizing)[1]
                self.board.pop()

                if move_value < best_move[1]:
                    best_move = (move, move_value)
                elif move_value == best_move[1]:
                    best_move = random.choice([best_move, (move, move_value)])

        print(str(self.board_evaluations) + 'evaluations')
        print(str(self.calls_to_minimax) + ' calls to minimax')
        return best_move

    def evaluate_branch_of_root(self, data):
        move, depth, board = data
        board.push(move)
        return move, self.alpha_beta_minimax(depth-.5, False, board=board)

    def alpha_beta_minimax_from_root(self, depth):
        start_time = time.time()
        self.static_evals = 0
        possible_moves = [move for move in self.board.legal_moves]
        random.shuffle(possible_moves)
        best_move = None
        best_move_val = -1000

        for move in possible_moves:
            self.board.push(move)
            move_val = self.alpha_beta_minimax(depth-.5, False)
            self.board.pop()
            if move_val > best_move_val:
                best_move = move
                best_move_val = move_val

        end_time = time.time()
        duration = round(end_time - start_time, 2)
        return best_move, best_move_val, depth, duration

    def alpha_beta_minimax_with_multithreading(self, depth):
        start_time = time.time()
        self.static_evals = 0
        possible_moves = [move for move in self.board.legal_moves]
        random.shuffle(possible_moves)

        thread_pool = multiprocessing.dummy.Pool()
        inputs = [(move, depth, self.board.copy()) for move in possible_moves]
        results = thread_pool.map(self.evaluate_branch_of_root, inputs)

        best_move = None
        best_move_val = -1000
        for move, move_val in results:
            if move_val > best_move_val:
                best_move, best_move_val = move, move_val

        end_time = time.time()
        duration = round(end_time - start_time, 2)
        return best_move, best_move_val, depth, duration

    def alpha_beta_minimax(self, depth, maximizing, alpha=-1000, beta=1000,
                           board=None):
        if board is None:
            board = self.board

        if depth == 0 or board.is_game_over():
            self.static_evals += 1
            return self.evaluate_board(board)

        possible_moves = [move for move in board.legal_moves]
        if maximizing:
            for move in possible_moves:
                board.push(move)
                move_val = self.alpha_beta_minimax(depth-.5, False, alpha, beta, board)
                board.pop()

                alpha = max(move_val, alpha)
                if alpha >= beta:
                    return alpha

            return alpha

        elif not maximizing:
            for move in possible_moves:
                board.push(move)
                move_val = self.alpha_beta_minimax(depth-.5, True, alpha, beta, board)
                board.pop()

                beta = min(move_val, beta)
                if beta <= alpha:
                    return beta

            return beta

    def alpha_beta_minimax_with_time_limit(self, depth, time_limit):
        start_time = time.time()
        insurance_move, insurance_val, _, _ = self.alpha_beta_minimax_from_root(depth-.5)
        self.static_evals = 0
        possible_moves = [move for move in self.board.legal_moves]
        random.shuffle(possible_moves)
        best_move = None
        best_move_val = -1000
        for move in possible_moves:
            current_time = time.time()
            duration = current_time - start_time
            if duration > time_limit:
                return insurance_move, insurance_val, depth - .5, round(duration, 2)

            self.board.push(move)
            move_val = self.alpha_beta_minimax(depth-.5, False)
            self.board.pop()
            if move_val > best_move_val:
                best_move = move
                best_move_val = move_val

        end_time = time.time()
        duration = round(end_time - start_time, 2)
        return best_move, best_move_val, depth, round(duration, 2)

    def generate_move(self):
        if self.is_opening:
            opening_move = self.generate_opening_move()
            if opening_move:
                opening, move_string = opening_move
                from_square = move_string[:2]
                from_square_num = chess.SQUARE_NAMES.index(from_square)
                to_square = move_string[2:]
                to_square_num = chess.SQUARE_NAMES.index(to_square)
                best_move = chess.Move(from_square_num, to_square_num)
                print(opening['n'])
                print('Move: ' + self.board.san(best_move))
            else:
                self.is_opening = False
                self.is_middle_game = True

        if self.is_middle_game:
            result = self.alpha_beta_minimax_with_time_limit(2, 15)
            best_move, best_move_val, depth_reached, duration = result
            print('Move: ' + self.board.san(best_move))
            print('Expected move value: ' + str(best_move_val))
            print('Depth reached: ' + str(depth_reached))
            print('Time elapsed: ' + str(duration) + 's')
            print('Static evaluations: ' + str(self.static_evals))
        return best_move
