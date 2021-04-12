from player import Player
from player import Position
from cell import Cell


def is_king(pos1, pos2):
    return abs((pos1 - pos2).x) <= 1 and abs((pos1 - pos2).y) <= 1


def is_knight(pos1, pos2):
    return abs(pos1.x - pos2.x) * abs(pos1.y - pos2.y) == 2


class Game:
    def __init__(self, players, board_size, interactive=True):
        self.board_size = board_size
        self.number_of_players = len(players)
        self.field = [[Cell(0) for _ in range(board_size.y)] for _ in range(board_size.x)]
        self.players = players
        self.current_move = 0
        self.is_ended_local = False
        self.deltas = [Position(0, 1), Position(1, 0), Position(0, -1), Position(-1, 0),
                       Position(1, 1), Position(1, -1), Position(-1, -1), Position(-1, 1),
                       Position(-2, -1), Position(-1, -2), Position(2, 1), Position(1, 2),
                       Position(-2, 1), Position(2, -1), Position(-1, 2), Position(1, -2)]
        for ind, i in enumerate(self.players):
            pos = i.get_trace()[-1]
            self.field[pos.x][pos.y] = Cell(1, ind)

    def is_ended(self):
        some_player_cannot_Move = False

        for pl in self.players:
            pos = pl.get_trace()[-1]
            is_kn = pl.get_is_knight()
            poss_moves = self.possible_moves(pos, is_kn)
            viable_moves = 0
            for shoot_from in poss_moves:
                viable_moves += len(self.possible_shots(shoot_from))
            if viable_moves == 0:
                some_player_cannot_Move = True

        return self.is_ended_local or some_player_cannot_Move

    # TODO: add num_of_blanks here after s,
    def is_shot_possible(self, pos, s):
        if not (0 <= s.x < self.board_size.x and 0 <= s.y < self.board_size.y):
            return False
        shoot_to_empty = self.field[s.x][s.y].is_empty()
        shoot_blank = s.x + s.y == -2  # and player.get_blanks() > 0
        player_shot = self.field[s.x][s.y].is_player()
        return is_knight(pos, s) and (player_shot or shoot_to_empty or shoot_blank)

    def is_move_possible(self, pos, m, is_knight_=False):
        if not (0 <= m.x < self.board_size.x and 0 <= m.y < self.board_size.y):
            return False
        if len(self.possible_shots(m)) == 0:
            return False
        move_to_empty = self.field[m.x][m.y].is_empty()
        return (is_king(m, pos) or is_knight_ and is_knight(m, pos)) and move_to_empty

    def execute_move(self, current_player_index, m):
        player = self.players[current_player_index]
        pos = player.get_trace()[-1]
        if self.is_move_possible(pos, m, player.get_is_knight()) and \
                current_player_index == self.current_move % self.number_of_players:
            self.players[current_player_index].next_position(m)
            self.field[m.x][m.y] = Cell(1, current_player_index)
            self.field[pos.x][pos.y] = Cell(2, current_player_index)
        else:
            raise ValueError('Invalid move')

    def execute_shot(self, current_player_index, s):
        # s = the_move.get_shoot()
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
                print('player was shot')
                # player_to_be_killed = self.field[s.x][s.y].get_owner_id()
                # this will be needed in version 2 (mult players)
                # self.kill_this_player(player_to_be_killed)
                self.field[s.x][s.y] = Cell(3, current_player_index)
                self.is_ended_local = True  # tmp
            else:
                self.field[s.x][s.y] = Cell(3, current_player_index)
        else:
            raise ValueError('Invalid shot')

    def kill_this_player(self, current_player_index):
        player = self.players[current_player_index]
        player.kill()

    def get_field(self):
        return self.field

    def get_traces(self):
        return [pl.get_trace() for pl in self.players]

    def possible_moves(self, pos, is_knight_=False):
        # player = self.players[player_index]
        # pos = player.get_trace()[-1]
        # is_knight_ = player.get_is_knight()
        result = [pos + de for de in self.deltas[:8] if self.is_move_possible(pos, pos + de, is_knight_)]
        if is_knight_:
            result += [pos + de for de in self.deltas[8:] if self.is_move_possible(pos, pos + de, is_knight_)]
        return result

    def possible_shots(self, pos):
        # player = self.players[player_index]
        # pos = player.get_trace()[-1]
        return [pos + de for de in self.deltas[8:] if self.is_shot_possible(pos, pos + de)]
