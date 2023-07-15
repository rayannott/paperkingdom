from copy import deepcopy

from cell import Cell, CellType
import exceptions as exc
from utils import *


class Board:
    def __init__(self) -> None:
        self._reset()
    
    def info(self):
        print(f'moves played: {len(self.move_history)}')
        print(f'player #{self.player_to_move} moves: {self.get_num_of_legal_moves()}')
        print(f'dscr: {self.get_ngd()}')
        print(f'eval: {self.current_eval:.2f}')
        someone_can_win = self.can_win()
        if someone_can_win and self.victor is None:
            print(f'can win by {someone_can_win}')

    def _reset(self):
        self.board = [[Cell(cell_type=CellType.EMPTY) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.players_positions = deepcopy(INITIAL_PLAYER_POSITIONS)
        for pl_id, pl_pos in enumerate(self.players_positions):
            self[pl_pos.tup()].set_player_id(pl_id).set_type(CellType.PLAYER)
        self.player_to_move = 0
        self.victor = None
        self.move_history: list[CompleteMove] = []
        self.eval_history: list[float] = []
        self.current_eval = self.eval_board()

    def set_state_from_ngd(self, ngd: str) -> int:
        '''Plays the game given by the normal game description (NGD) and
        changes the board accordingly.
        If successful, returns the number of played moves.'''
        self._reset()
        for ending in ['r.', 'b.']:
            if ngd.endswith(ending): ngd = ngd.replace(ending, '')
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
        if self.victor is not None: descr += 'rb'[self.victor] + '.'
        return descr
    
    def set_state_from_nbs(self, nbs: str) -> None:
        self._reset()
        rows_nbs, player_to_move_label, victory_status = nbs.split()
        self.player_to_move = 0 if player_to_move_label == 'r' else 1
        self.victor = None if victory_status == '-' else ({'R': 0, 'B': 1}[victory_status])
        rows_nbs_list: list[str] = rows_nbs.split('/')
        self.board = []
        for row_nbs in rows_nbs_list:
            this_row = []
            i = 0
            while i < len(row_nbs):
                if row_nbs[i] in NUMBERS:
                    if row_nbs[i] != '1':
                        for _ in range(int(row_nbs[i])):
                            this_row.append(Cell(cell_type=CellType.EMPTY))
                    else:
                        if i != len(row_nbs) - 1 and row_nbs[i+1] in NUMBERS:
                            for _ in range(10 + int(row_nbs[i+1])):
                                this_row.append(Cell(cell_type=CellType.EMPTY))
                            i += 1
                        else:
                            this_row.append(Cell(cell_type=CellType.EMPTY))
                else:
                    if row_nbs[i] in 'Pp':
                        this_row.append(Cell(cell_type=CellType.PLAYER, player_id=(0 if row_nbs[i] == 'P' else 1)))
                    elif row_nbs[i] in 'Tt':
                        this_row.append(Cell(cell_type=CellType.TRACE, player_id=(0 if row_nbs[i] == 'T' else 1)))
                    elif row_nbs[i] == 'x':
                        this_row.append(Cell(cell_type=CellType.SHOT))
                i += 1
            self.board.append(this_row)


    def get_nbs(self) -> str:
        '''Returns the normal board state (NBS) string.
        The NBS is equivalent to chess' FEN'''
        #! make as in chess: using numbers for consecutive blank tiles
        to_ret = []
        for row_id in range(BOARD_SIZE):
            row = ''
            current_empty_cell_counter = 0
            for col_id in range(BOARD_SIZE):
                this_cell = self.board[row_id][col_id]
                if this_cell.is_empty(): current_empty_cell_counter += 1
                else:
                    if current_empty_cell_counter:
                        row += str(current_empty_cell_counter)
                        current_empty_cell_counter = 0
                    if this_cell.is_shot(): row += 'x'
                    elif this_cell.is_trace():
                            row += 'T' if this_cell.player_id == 0 else 't'
                    elif this_cell.is_player(): row += 'P' if this_cell.player_id == 0 else 'p'
            if current_empty_cell_counter:
                row += str(current_empty_cell_counter)
            to_ret.append(row)
        return '/'.join(to_ret) + ' ' + \
            ('r' if self.player_to_move == 0 else 'b') + ' ' + \
            ('-' if self.victor is None else 'RB'[self.victor])
    
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
        for delta in SHOT_DELTAS + (SHOT_DELTAS_BOUNDARY if is_pos_on_border(shot_from) else []):
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

    def _get_complete_moves_for(self, player_id: int) -> list[CompleteMove]:
        complete_moves = []
        for move in self._get_moves_from_for(self.players_positions[player_id], player_id):
            for shot in self._get_shots_from_for(move, self.player_to_move):
                complete_moves.append(CompleteMove(move, shot))
        return complete_moves

    def get_complete_moves(self) -> list[CompleteMove]:
        '''Returns a list of complete moves possible for the current player'''
        return self._get_complete_moves_for(self.player_to_move)

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
        if self.victor is not None:
            raise exc.GameIsOverException('Cannot move: the game is over')
        if not self._if_complete_move_possible(complete_move):
            raise exc.InvalidCompleteMoveException('Cannot execute this move')
        self.move_player_to(self.player_to_move, complete_move.move)
        self.shoot_by_from_to(self.player_to_move, complete_move.move, complete_move.shot)
        self.move_history.append(complete_move)
        self.player_to_move = 1 - self.player_to_move
        self.victor = self.check_victory()
        self.current_eval = self.eval_board()
        self.eval_history.append(self.current_eval)

    def get_num_of_legal_moves(self) -> int:
        return len(self.get_complete_moves())

    def can_win(self) -> CompleteMove | None:
        return self.can_win_by(self.player_to_move)

    def can_win_by(self, player_id: int) -> CompleteMove | None:
        for cm in self._get_complete_moves_for(player_id):
            if cm.shot == self.players_positions[1 - player_id]:
                return cm
        return None

    def eval_board(self) -> float:
        '''Evaluates the board. Gives a float score.
        +1 --- best for the red player;
        -1 --- best for the blue player'''
        if self.victor is not None:
            return 1 if self.victor == 0 else -1
        red_moves = self._get_complete_moves_for(player_id=0)
        blue_moves = self._get_complete_moves_for(player_id=1)
        if self.player_to_move == 0:
            for cm in red_moves: 
                if cm.shot == self.players_positions[1]: return 1 # if red can win and it's their move
            ...
        else:
            for cm in blue_moves:
                if cm.shot == self.players_positions[0]: return -1 # if blue can win and it's their move
            ...
        eval_ = (len(red_moves) - len(blue_moves))/(len(blue_moves) + len(red_moves))
        return eval_ + \
            abs(eval_) * (-1 if self.player_to_move == 0 else 1) * 0.15 + \
            -0.1 * is_pos_outside_arena(self.players_positions[0]) + 0.1 * is_pos_outside_arena(self.players_positions[1])


class GameReplay:
    def __init__(self, ngd: str) -> None:
        '''Loads a game as a list of complete moves.
        Returns a number of loaded moves if successful'''
        self.b = Board()
        for ending in ['r.', 'b.']:
            if ngd.endswith(ending): ngd = ngd.replace(ending, '')
        moves_normal = ngd.replace(',', '').strip().split() # a list of normal moves (ex.: 'f7/g5') 
        complete_moves = []
        for move_normal in moves_normal:
            complete_moves.append(make(move_normal))
        self.complete_moves = iter(complete_moves)
        print(f'Loaded {len(complete_moves)} moves')

    def play(self):
        cm = next(self.complete_moves)
        self.b.execute_complete_move(cm)
