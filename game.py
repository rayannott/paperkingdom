from player import Player
from player import Position
from cell import Cell
from json import dump
from datetime import datetime

def is_king(pos1: Position, pos2: Position):
    """
    checks if two positions are 'king' away from e/o
    """
    return abs((pos1 - pos2).x) <= 1 and abs((pos1 - pos2).y) <= 1


def is_knight(pos1: Position, pos2: Position):
    """
    checks if two positions are 'knight' away from e/o
    """
    return abs(pos1.x - pos2.x) * abs(pos1.y - pos2.y) == 2


def is_diag(pos1: Position, pos2: Position):
    """
    checks if two positions are at the corners of a square of side 3
    """
    return abs(pos1.x - pos2.x) == 2 and abs(pos1.y - pos2.y) == 2


class Game:
    def __init__(self, players, board_size, current_move=0, interactive=True):
        """
        levels (fuck levels!):
        1 - core
        2 - prev + borders
        3 - prev + knights + nerf
        4 - prev + tetras + tetras for
        """
        self.board_size = board_size
        self.number_of_players = len(players)
        self.field = [[Cell(0) for _ in range(board_size.y)] for _ in range(board_size.x)]
        self.players = players
        self.current_move = current_move
        self.is_ended_local = False
        self.deltas = [Position(0, 1), Position(1, 0), Position(0, -1), Position(-1, 0),
                       Position(1, 1), Position(1, -1), Position(-1, -1), Position(-1, 1),

                       Position(-2, -2), Position(-2, 2), Position(2, -2), Position(2, 2),

                       Position(-2, -1), Position(-1, -2), Position(2, 1), Position(1, 2),
                       Position(-2, 1), Position(2, -1), Position(-1, 2), Position(1, -2)]
        self.init_config = self.convert_game_to_config()
        self.moves_save = []
        self.tmp_dict = {}
        for ind, i in enumerate(self.players):
            pos = i.get_trace()[-1]
            self.field[pos.x][pos.y] = Cell(1, ind)

    def is_ended(self):
        """
        !is used outside Game to end the game loop
        """
        some_player_cannot_move = False
        for pl in self.players:
            pos = pl.get_trace()[-1]
            is_kn = pl.is_knight
            poss_moves = self.possible_moves(pos, is_kn)
            viable_moves = 0
            for shoot_from in poss_moves:
                viable_moves += len(self.possible_shots(shoot_from))
            if viable_moves == 0:
                some_player_cannot_move = True

        return self.is_ended_local or some_player_cannot_move

    # TODO: add num_of_blanks here after s,
    def is_shot_possible(self, pos, s):
        """
        checks if it is possible to shoot from position pos to s
        """
        if not (0 <= s.x < self.board_size.x and 0 <= s.y < self.board_size.y):
            return False
        shoot_from_border = self.is_on_border(pos) and is_diag(pos, s)
        shoot_to_empty = self.field[s.x][s.y].is_empty()
        shoot_blank = s.x + s.y == -2  # and player.get_blanks() > 0
        player_shot = self.field[s.x][s.y].is_player()
        return is_knight(pos, s) and (player_shot or shoot_to_empty or shoot_blank) \
               or shoot_from_border and (player_shot or shoot_to_empty or shoot_blank)

    def is_move_possible(self, pos, m, is_knight_=False):
        """
        checks if it is possible to move from position pos to s
        considering that a player may be a knight
        """
        if not (0 <= m.x < self.board_size.x and 0 <= m.y < self.board_size.y):
            return False
        if len(self.possible_shots(m)) == 0:
            return False
        move_to_empty = self.field[m.x][m.y].is_empty()
        return (is_king(m, pos) or is_knight_ and is_knight(m, pos)) and move_to_empty

    def execute_move(self, current_player_index, m):
        """
        !is used outside Game
        if possible:
            moves the player with current_player_index and updates the cells
        """
        player = self.players[current_player_index]
        pos = player.get_trace()[-1]
        if self.is_move_possible(pos, m, player.is_knight) and \
                current_player_index == self.current_move % self.number_of_players:
            self.players[current_player_index].next_position(m)
            self.field[m.x][m.y] = Cell(1, current_player_index)  # this is a "player" now
            self.field[pos.x][pos.y] = Cell(2, current_player_index)  # this is a "trace" now
            self.tmp_dict = {
                'player_id': current_player_index,
                'move': [m.x, m.y]
            }
        else:
            raise ValueError('Invalid move')

    def execute_shot(self, current_player_index, s):
        """
        !is used outside Game
        if possible:
            records the shot made by the player with current_player_index and updates the cells
        """
        player = self.players[current_player_index]
        pos = player.get_trace()[-1]
        if self.is_shot_possible(pos, s) and \
                current_player_index == self.current_move % self.number_of_players:
            self.current_move += 1

            shoot_blank = s.x + s.y == -2 and player.get_blanks() > 0
            player_shot = self.field[s.x][s.y].is_player()
            # TODO: blanks
            if shoot_blank:
                player.reduce_blanks()
                # something else...
            # TODO: what if the player was shot
            elif player_shot:
                print('Player was shot')
                # player_to_be_killed = self.field[s.x][s.y].get_owner_id()
                # this will be needed in version 2 (mult players)
                # self.kill_this_player(player_to_be_killed)
                self.field[s.x][s.y] = Cell(3, current_player_index)
                self.is_ended_local = True  # tmp
            else:
                self.field[s.x][s.y] = Cell(3, current_player_index)
                self.tmp_dict['shot'] = [s.x, s.y]
                self.moves_save.append(self.tmp_dict)
        else:
            raise ValueError('Invalid shot')

    def possible_moves(self, pos, is_knight_=False):
        # player = self.players[player_index]
        # pos = player.get_trace()[-1]
        # is_knight_ = player.get_is_knight()
        result = [pos + de for de in self.deltas[:8] if self.is_move_possible(pos, pos + de, is_knight_)]
        if is_knight_:
            result += [pos + de for de in self.deltas[12:] if self.is_move_possible(pos, pos + de, is_knight_)]
        return result

    def possible_shots(self, pos):
        return [pos + de for de in self.deltas[8:] if self.is_shot_possible(pos, pos + de)]

    def kill_this_player(self, current_player_index):
        player = self.players[current_player_index]
        player.kill()

    def convert_game_to_config(self):
        config = {
            'cells': [
                [
                    {
                        'cell_type': cell.cell_type,
                        'owner_id': cell.owner_id,
                        'parameter': cell.parameter
                    }
                    for cell in row
                ]
                for row in self.field
            ],
            'players': [
                {
                    'id': ind,
                    'name': pl.name,
                    'is_knight': pl.is_knight,
                    'is_alive': pl.is_alive,
                }
                for ind, pl in enumerate(self.players)
            ]
        }
        return config

    def save_the_game(self):
        game = {
            'board_size': [self.board_size.x, self.board_size.y],
            'is_finished': self.is_ended(),
            'init_config': self.init_config,
            'moves': self.moves_save,
            'final_config': self.convert_game_to_config()
        }
        filename = str(datetime.now())
        with open(filename + ".json", "w") as write_file:
            dump(game, write_file, indent=4)


    def get_field(self):
        return self.field

    def is_on_border(self, pos):
        return pos.x == 0 or pos.x == self.board_size.x - 1 or pos.y == 0 or pos.y == self.board_size.y - 1
