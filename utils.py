from dataclasses import dataclass

YAXIS = 'ba9876543210'
XAXIS = 'abcdefghijkl'
YAXIS_BACK = {ch: i for i, ch in enumerate(YAXIS)}
XAXIS_BACK = {ch: i for i, ch in enumerate(XAXIS)}

NUMBERS = set('0123456789')


BOARD_SIZE = 12
NUM_OF_PLAYERS = 2


def make_move(str_coord: str) -> 'Pos':
    return Pos(YAXIS_BACK[str_coord[1]], XAXIS_BACK[str_coord[0]])


def make_cm(str_coord_move: str, str_coord_shot: str) -> 'CompleteMove':
    return CompleteMove(make_move(str_coord_move), make_move(str_coord_shot))


def make(cm_normal: str) -> 'CompleteMove':
    '''Returns a CompleteMove object constructed with
    the complete move normal notation'''
    return make_cm(*cm_normal.split('/'))


def is_pos_on_border(pos: 'Pos') -> bool:
    return pos.x in {2, 9} and 2 <= pos.y <= 9 or pos.y in {2, 9} and 2 <= pos.x <= 9


def is_pos_outside_arena(pos: 'Pos') -> bool:
    return pos.x < 2 or pos.x > 9 or pos.y < 2 or pos.y > 9


def is_pos_in_center(pos: 'Pos') -> bool:
    return pos.x in {5, 6} and pos.y in {5, 6}


def min_distance_to_edge(pos: 'Pos') -> int:
    return min(
        min(BOARD_SIZE - 1 - pos.x, pos.x),
        min(BOARD_SIZE - 1 - pos.y, pos.y)
    )

def dist_two_pos(p1: 'Pos', p2: 'Pos') -> float:
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**.5

def clip(value: float, min_: float, max_: float) -> float:
    return max(min_, min(max_, value))


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


INITIAL_PLAYER_POSITIONS = [Pos(3, 3), Pos(8, 8)]

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
