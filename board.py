from dataclasses import dataclass

from cell import Cell, CellType
import exceptions as exc
from utils import *

BOARD_SIZE = 12
NUM_OF_PLAYERS = 2


@dataclass
class Pos:
    x: int
    y: int
    def __add__(self, other: 'Pos') -> 'Pos':
        return Pos(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Pos') -> 'Pos':
        return Pos(self.x - other.x, self.y - other.y)

    def tup(self):
        return (self.x, self.y)

    def __str__(self) -> str:
        return f'{XAXIS[self.y]}{YAXIS[self.x]}'


MOVE_DELTAS = [Pos(0, 1), Pos(1, 0), Pos(0, -1), Pos(-1, 0),
            Pos(1, 1), Pos(1, -1), Pos(-1, -1), Pos(-1, 1)]
SHOT_DELTAS = [Pos(-2, -1), Pos(-1, -2), Pos(2, 1), Pos(1, 2),
            Pos(-2, 1), Pos(2, -1), Pos(-1, 2), Pos(1, -2)]
SHOT_DELTAS_BOUNDARY = [Pos(-2, -2), Pos(-2, 2), Pos(2, -2), Pos(2, 2)]


@dataclass
class CompleteMove:
    move: Pos
    shot: Pos
    def __repr__(self) -> str:
        return f'{self.move}/{self.shot}'


class Board:
    def __init__(self) -> None:
        self.board = [[Cell(cell_type=CellType.EMPTY) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.players_positions = [Pos(3, 4), Pos(8, 7)]
        for pl_id, pl_pos in enumerate(self.players_positions):
            self[pl_pos.tup()].set_player_id(pl_id).set_type(CellType.PLAYER)
    
    def __getitem__(self, s: tuple[int, int]) -> Cell:
        return self.board[s[0]][s[1]]

    def _get_moves(self, pos: Pos) -> list[Pos]:
        '''Returns moves possible from a given position'''
        #? add jumping over root?
        moves = []
        for delta in MOVE_DELTAS:
            if not 0 <= pos.x + delta.x < BOARD_SIZE or not 0 <= pos.y + delta.y < BOARD_SIZE:
                continue
            if self[pos.x + delta.x, pos.y + delta.y].is_empty():
                moves.append(Pos(pos.x + delta.x, pos.y + delta.y))
        return moves

    def _get_shots(self, pos: Pos, player_id: int) -> list[Pos]:
        '''Returns shots possible from a given position'''
        shots = []
        for delta in SHOT_DELTAS + (SHOT_DELTAS_BOUNDARY if pos.x in {2, 9} or pos.y in {2, 9} else []):
            if not 0 <= pos.x + delta.x < BOARD_SIZE or not 0 <= pos.y + delta.y < BOARD_SIZE:
                continue
            if self[pos.x + delta.x, pos.y + delta.y].is_empty() or \
                self[pos.x + delta.x, pos.y + delta.y].is_player(1-player_id):
                shots.append(Pos(pos.x + delta.x, pos.y + delta.y))
        return shots
    
    def _if_complete_move_possible(self, player_id: int, complete_move: CompleteMove) -> bool:
        if complete_move.move not in self._get_moves(self.players_positions[player_id]):
            return False
        if complete_move.shot not in self._get_shots(complete_move.move, player_id):
            return False
        return True
    
    def get_complete_moves(self, player_id: int) -> list[CompleteMove]:
        '''Returns a list of complete moves possible from a given position'''
        pos = self.players_positions[player_id]
        complete_moves = []
        for move in self._get_moves(pos):
            for shot in self._get_shots(move, player_id):
                complete_moves.append(CompleteMove(move, shot))
        return complete_moves

    def move_player_to(self, player_id: int, move_to: Pos):
        if move_to in self._get_moves(self.players_positions[player_id]):
            self[self.players_positions[player_id].tup()].set_type(CellType.TRACE) # reset prev cell
            self.players_positions[player_id] = move_to # change player's pos
            self[move_to.tup()].set_player_id(player_id).set_type(CellType.PLAYER) # set new pos on the board
        else:
            raise exc.InvalidMoveException(f'Cannot move player #{player_id} to {move_to}')

    def shoot_by_from_to(self, player_id: int, shoot_from: Pos, shoot_to: Pos):
        if shoot_to in self._get_shots(shoot_from, player_id):
            self[shoot_to.tup()].set_player_id(player_id).set_type(CellType.SHOT)
        else:
            raise exc.InvalidShotException(f'Cannot shoot by player #{player_id} from {shoot_from} to {shoot_to}')

    def execute_complete_move_by(self, player_id: int, complete_move: CompleteMove):
        if not self._if_complete_move_possible(player_id, complete_move):
            raise exc.InvalidCompleteMoveException('Cannot execute this move')
        self.move_player_to(player_id, complete_move.move)
        self.shoot_by_from_to(player_id, complete_move.move, complete_move.shot)
    
    def eval_num_of_moves(self, player_to_move: int) -> int:
        return len(self.get_complete_moves(player_to_move))

    def can_win_by(self, player_to_move: int) -> CompleteMove | None:
        for cm in self.get_complete_moves(player_to_move):
            if cm.shot == self.players_positions[1 - player_to_move]:
                return cm
        return None

    def eval_num_of_non_lethal_moves(self, player_to_move: int) -> int:
        pass