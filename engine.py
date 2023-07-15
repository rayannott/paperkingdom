'''
This script contains some machine algorithms which can play the game 
'''
from copy import deepcopy
import math

from board import Board
from utils import CompleteMove
import exceptions as exc


import random
class PickRandom:
    def __init__(self, player_id: int, board: Board) -> None:
        self.player_id = player_id
        self.b = board
    
    def pick_move(self) -> CompleteMove:
        possible_moves = self.b.get_complete_moves()
        return random.choice(possible_moves)

    def make_move(self):
        if self.b.player_to_move != self.player_id:
            print('This is not my turn!')
            return
        best_move = self.pick_move()
        self.b.execute_complete_move(best_move)
        return best_move

class PickBest:
    '''This algorithm just picks the move which provides the best eval outcome'''
    def __init__(self, player_id: int, board: Board, randomize: bool = False) -> None:
        self.player_id = player_id
        self.b = board
        self.randomize = randomize

    def pick_move(self) -> CompleteMove:
        possible_moves = self.b.get_complete_moves()
        if not possible_moves:
            raise exc.GameIsOverException('No moves left: the game is over')
        moves_values: list[tuple[CompleteMove, float]] = []
        for cm in possible_moves:
            b_copy = deepcopy(self.b)
            b_copy.execute_complete_move(cm)
            moves_values.append((cm, b_copy.eval_board()))
        moves_values.sort(key=lambda x: x[1], reverse=(not self.player_id)) # sorting reversed if player_id=0 (because 0th player maximizes)
        if not self.randomize:
            return moves_values[0][0]
        # randomizing over the moves with the same value
        equivalent_cms = []
        common_value = moves_values[0][1]
        for cm, value in moves_values:
            if math.isclose(common_value, value):
                common_value = value
                equivalent_cms.append(cm)
            else:
                break
        print('randomizing among', len(equivalent_cms))
        return random.choice(equivalent_cms)

    def make_move(self):
        if self.b.player_to_move != self.player_id:
            print('This is not my turn!')
            return
        best_move = self.pick_move()
        self.b.execute_complete_move(best_move)
        return best_move


class Minimax:
    '''
    The minimax algorithm builds a tree of different moves and chooses the one which maximizes the minimum utility.
    In this implementation, red is the maximizer and blue is the minimizer.
    '''
    def __init__(self, player_id: int, board: Board, depth: int = 3, randomize: bool = False) -> None:
        self.player_id = player_id
        self.b = board
        self.depth = depth - 1
        self.randomize = randomize
    
    def minimax(self, board: Board, cur_depth: int, alpha: float, beta: float, is_maximizing_player: bool) -> float:
        '''Returns a minimax evaluation of the [board]'''
        if cur_depth == 0 or board.victor is not None:
            return board.eval_board()
        # print(f'{cur_depth=} {alpha=} {beta=}')
        if is_maximizing_player:
            if board.can_win():
                return 1.
            max_eval = -math.inf
            for cm in self.b.get_complete_moves():
                b_copy = deepcopy(self.b)
                b_copy.execute_complete_move(cm) # now b_copy is the child
                eval_ = self.minimax(b_copy, cur_depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_)
                alpha = max(alpha, eval_)
                if beta <= alpha:
                    # print('pruned')
                    break
            return max_eval
        else:
            if board.can_win():
                return -1.
            min_eval = math.inf
            for cm in self.b.get_complete_moves():
                b_copy = deepcopy(self.b)
                b_copy.execute_complete_move(cm) # now b_copy is the child
                eval_ = self.minimax(b_copy, cur_depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_)
                beta = min(beta, eval_)
                if beta <= alpha:
                    # print('pruned')
                    break
            return min_eval

    def pick_move(self) -> CompleteMove:
        possible_moves = self.b.get_complete_moves()
        if not possible_moves:
            raise exc.GameIsOverException('No moves left: the game is over')
        moves_values: list[tuple[CompleteMove, float]] = []
        for i, cm in enumerate(possible_moves):
            print(i, end=',')
            b_copy = deepcopy(self.b)
            b_copy.execute_complete_move(cm)
            minimax_value = self.minimax(
                                board=b_copy,
                                cur_depth=self.depth,
                                alpha=-math.inf,
                                beta=math.inf,
                                is_maximizing_player=bool(self.player_id)
                            )
            if minimax_value == 1. and self.player_id == 0 or minimax_value == -1. and self.player_id == 1:
                return cm
            moves_values.append(
                (
                    cm, 
                    minimax_value
                )
            )
        moves_values.sort(key=lambda x: x[1], reverse=(not self.player_id)) # sorting reversed if player_id=0 (because 0th player maximizes)
        if not self.randomize:
            return moves_values[0][0]
        equivalent_cms = []
        common_value = moves_values[0][1]
        for cm, value in moves_values:
            if math.isclose(common_value, value):
                common_value = value
                equivalent_cms.append(cm)
            else:
                break
        print('randomizing among', len(equivalent_cms))
        return random.choice(equivalent_cms)

    def make_move(self):
        if self.b.player_to_move != self.player_id:
            print('This is not my turn!')
            return
        best_move = self.pick_move()
        self.b.execute_complete_move(best_move)
        return best_move
