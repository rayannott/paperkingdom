from string import ascii_lowercase

from board import Board, BOARD_SIZE, NUM_OF_PLAYERS, CompleteMove, Pos
from cell import Cell, CellType

from utils import *

def make_move(str_coord: str) -> Pos:
    return Pos(YAXIS_BACK[str_coord[1]], XAXIS_BACK[str_coord[0]])

def make_cm(str_coord_move: str, str_coord_shot: str) -> CompleteMove:
    return CompleteMove(make_move(str_coord_move), make_move(str_coord_shot))

def make(cm_normal: str) -> CompleteMove:
    return make_cm(*cm_normal.split('/'))

class Game:
    def __init__(self) -> None:
        self._reset()

    def _reset(self):
        self.board = Board()
        self.player_id_to_move = 0
        self.victor = None
        self.move_history: list[CompleteMove] = []

    def set_state_to(self, normal_dscr: str) -> int:
        '''Sets state of the game to the one after the listed moves'''
        self._reset()
        for ending in ['b.', 'r.']:
            if normal_dscr.endswith(ending): normal_dscr.replace(ending, '')
        moves_normal = normal_dscr.replace(',', '').strip().split()
        for move_normal in moves_normal:
            self.execute_complete_move(make(move_normal))
        return len(moves_normal)
    
    def info(self):
        print(f'moves played: {len(self.move_history)}')
        print(f'player #{self.player_id_to_move} moves: {self.board.eval_num_of_moves(self.player_id_to_move)}')
        print(f'dscr: {self.get_game_description()}')
        someone_can_win = self.board.can_win_by(self.player_id_to_move)
        if someone_can_win and self.victor is None:
            print(f'can win by {someone_can_win}')

    def execute_complete_move(self, complete_move: CompleteMove):
        self.board.execute_complete_move_by(self.player_id_to_move, complete_move)
        self.move_history.append(complete_move)
        self.player_id_to_move = (self.player_id_to_move + 1) % NUM_OF_PLAYERS
        self.victor = self.check_victory()

    def check_victory(self) -> int | None:
        '''Return an index of a winner or None if game is not terminated'''
        if self.board[self.board.players_positions[self.player_id_to_move].tup()].is_shot() \
            or not self.board.get_complete_moves(self.player_id_to_move):
            return 1 - self.player_id_to_move
        return None
    
    def get_game_description(self):
        descr = ''
        for i, cm in enumerate(self.move_history):
            descr += XAXIS[cm.move.y]
            descr += YAXIS[cm.move.x]
            descr += '/'
            descr += XAXIS[cm.shot.y]
            descr += YAXIS[cm.shot.x]
            descr += ',' if i % 2 else ''
            descr += ' '
        if self.victor is not None: descr += ['b', 'r'][self.victor] + '.'
        return descr
