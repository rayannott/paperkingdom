from cell import Cell, CellType
import exceptions as exc
from utils import *


class Board:
    def __init__(self) -> None:
        self._reset()
    
    def info(self):
        print(f'moves played: {len(self.move_history)}')
        print(f'player #{self.player_to_move} moves: {self.eval_num_of_moves()}')
        print(f'dscr: {self.get_ngd()}')
        someone_can_win = self.can_win_by()
        if someone_can_win and self.victor is None:
            print(f'can win by {someone_can_win}')

    def _reset(self):
        self.board = [[Cell(cell_type=CellType.EMPTY) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.players_positions = [Pos(3, 4), Pos(8, 7)]
        for pl_id, pl_pos in enumerate(self.players_positions):
            self[pl_pos.tup()].set_player_id(pl_id).set_type(CellType.PLAYER)
        self.player_to_move = 0
        self.victor = None
        self.move_history: list[CompleteMove] = []

    def set_state_from_ngd(self, ngd: str) -> int:
        '''Plays the game given by the normal game description (NGD) and
        changes the board accordingly.
        If successful, returns the number of played moves.'''
        self._reset()
        for ending in ['b.', 'r.']:
            if ngd.endswith(ending): ngd.replace(ending, '')
        moves_normal = ngd.replace(',', '').strip().split()
        for move_normal in moves_normal:
            self.execute_complete_move(make(move_normal))
        return len(moves_normal)

    def get_ngd(self) -> str:
        '''Returns the normal game description (NGD) as a string'''
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
    
    def set_state_from_nbs(self, nbs: str) -> None:
        pass

    def get_nbs(self) -> str:
        '''Returns the normal board state (NBS) string.
        The NBS is equivalent to chess' FEN'''
        #! make as in chess: using numbers for consecutive blank tiles
        to_ret = []
        for row_id in range(BOARD_SIZE):
            row = ''
            for col_id in range(BOARD_SIZE):
                this_cell = self.board[row_id][col_id]
                if this_cell.is_empty(): row += '.'
                elif this_cell.is_shot(): row += 'x'
                elif this_cell.is_trace(): row += 'T' if this_cell.player_id == 0 else 't'
                elif this_cell.is_player(): row += 'P' if this_cell.player_id == 0 else 'p'
            to_ret.append(row)
        return '/'.join(to_ret)
    
    def __getitem__(self, s: tuple[int, int]) -> Cell:
        return self.board[s[0]][s[1]]

    def get_cpp(self) -> Pos:
        '''Returns the current player's position'''
        return self.players_positions[self.player_to_move]

    def check_victory(self) -> int | None:
        '''Return an index of a winner or None if game is not terminated'''
        if self[self.get_cpp().tup()].is_shot() \
            or not self.get_complete_moves():
            return 1 - self.player_to_move
        return None

    def _get_moves_from_for(self, move_from: Pos, move_for: int) -> list[Pos]:
        '''Returns moves possible for the current player'''
        #? add jumping over root?
        moves = []
        for delta in MOVE_DELTAS:
            if not 0 <= move_from.x + delta.x < BOARD_SIZE or not 0 <= move_from.y + delta.y < BOARD_SIZE:
                continue
            if self[move_from.x + delta.x, move_from.y + delta.y].is_empty():
                moves.append(Pos(move_from.x + delta.x, move_from.y + delta.y))
        return moves

    def _get_shots_from_for(self, shot_from: Pos, shot_for: int):
        shots = []
        for delta in SHOT_DELTAS + (SHOT_DELTAS_BOUNDARY if shot_from.x in {2, 9} or shot_from.y in {2, 9} else []):
            if not 0 <= shot_from.x + delta.x < BOARD_SIZE or not 0 <= shot_from.y + delta.y < BOARD_SIZE:
                continue
            if self[shot_from.x + delta.x, shot_from.y + delta.y].is_empty() or \
                self[shot_from.x + delta.x, shot_from.y + delta.y].is_player(1-shot_for):
                shots.append(Pos(shot_from.x + delta.x, shot_from.y + delta.y))
        return shots
        
    def _if_complete_move_possible(self, complete_move: CompleteMove) -> bool:
        if complete_move.move not in self._get_moves_from_for(self.get_cpp(), self.player_to_move):
            return False
        if complete_move.shot not in self._get_shots_from_for(complete_move.move, self.player_to_move):
            return False
        return True
    
    def get_complete_moves(self) -> list[CompleteMove]:
        '''Returns a list of complete moves possible for the current player'''
        complete_moves = []
        for move in self._get_moves_from_for(self.get_cpp(), self.player_to_move):
            for shot in self._get_shots_from_for(move, self.player_to_move):
                complete_moves.append(CompleteMove(move, shot))
        return complete_moves

    def move_player_to(self, player_id: int, move_to: Pos):
        if move_to in self._get_moves_from_for(self.get_cpp(), self.player_to_move):
            self[self.players_positions[player_id].tup()].set_type(CellType.TRACE) # reset prev cell
            self.players_positions[player_id] = move_to # change player's pos
            self[move_to.tup()].set_player_id(player_id).set_type(CellType.PLAYER) # set new pos on the board
        else:
            raise exc.InvalidMoveException(f'Cannot move player #{player_id} to {move_to}')

    def shoot_by_from_to(self, player_id: int, shoot_from: Pos, shoot_to: Pos):
        if shoot_to in self._get_shots_from_for(shoot_from, player_id):
            self[shoot_to.tup()].set_player_id(player_id).set_type(CellType.SHOT)
        else:
            raise exc.InvalidShotException(f'Cannot shoot by player #{player_id} from {shoot_from} to {shoot_to}')

    def execute_complete_move(self, complete_move: CompleteMove):
        if not self._if_complete_move_possible(complete_move):
            raise exc.InvalidCompleteMoveException('Cannot execute this move')
        self.move_player_to(self.player_to_move, complete_move.move)
        self.shoot_by_from_to(self.player_to_move, complete_move.move, complete_move.shot)
        self.move_history.append(complete_move)
        self.player_to_move = 1 - self.player_to_move
        self.victor = self.check_victory()
    
    def eval_num_of_moves(self) -> int:
        return len(self.get_complete_moves())

    def can_win_by(self) -> CompleteMove | None:
        for cm in self.get_complete_moves():
            if cm.shot == self.players_positions[1 - self.player_to_move]:
                return cm
        return None

    def eval_num_of_non_lethal_moves(self, player_to_move: int) -> int:
        return 0
