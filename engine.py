'''
This script contains some machine algorithms which can play the game 
'''
from copy import deepcopy

from board import Board
from utils import CompleteMove


class PickBest:
    '''This algorithm just picks the move which provides the best eval outcome'''
    def __init__(self, player_id: int, board: Board) -> None:
        self.player_id = player_id
        self.b = board

    def pick_best_move(self):
        possible_moves = self.b.get_complete_moves()
        move_value: list[tuple[CompleteMove, float]] = []
        for cm in possible_moves:
            b_copy = deepcopy(self.b)
            b_copy.execute_complete_move(cm)
            move_value.append((cm, b_copy.eval_board()))
        move_value.sort(key=lambda x: x[1], reverse=(not self.player_id)) # sorting reversed if player_id=0 (because 0th player maximizes)
        return move_value[0][0]

    def make_best_move(self):
        if self.b.player_to_move != self.player_id:
            print('This is not my turn!')
            return
        best_move = self.pick_best_move()
        self.b.execute_complete_move(best_move)
        return best_move


class Minimax:
    '''
    The minimax algorithm builds a tree of different moves and chooses the one which maximizes the minimum utility.
    In this implementation, red is the maximizer and blue is the minimizer.
    '''