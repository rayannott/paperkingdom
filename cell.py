from enum import Enum, auto
from dataclasses import dataclass

class CellType(Enum):
    EMPTY = auto()
    PLAYER = auto()
    TRACE = auto()
    SHOT = auto()

@dataclass
class Cell:
    cell_type: CellType
    player_id: int | None = None

    def set_type(self, set_to: CellType) -> 'Cell':
        self.cell_type = set_to
        return self

    def set_player_id(self, set_to: int | None) -> 'Cell':
        self.player_id = set_to
        return self

    def is_empty(self):
        return self.cell_type == CellType.EMPTY
    
    def is_player(self, _id: int | None = None):
        return self.cell_type == CellType.PLAYER and (True if _id is None else _id == self.player_id)

    def is_trace(self, _id: int | None = None):
        return self.cell_type == CellType.TRACE and (True if _id is None else _id == self.player_id)

    def is_shot(self, _id: int | None = None):
        return self.cell_type == CellType.SHOT and (True if _id is None else _id == self.player_id)

    def reset(self):
        '''Resets self to an empty cell with no player info'''
        self.set_type(CellType.EMPTY)
        self.set_player_id(None)
