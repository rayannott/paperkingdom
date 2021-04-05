from player import Player
from player import Position
from cell import Cell


# if two positions given are a KING away from one another
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
        some_player_cannot_move = False
        num_of_players = len(self.players)
        for pl_ind in range(num_of_players):
            if len(self.possible_moves(pl_ind)) == 0:
                print('cannot move')
                some_player_cannot_move = True
                break

        return self.is_ended_local or some_player_cannot_move

    def is_shot_possible(self, current_player_index, s):
        if not (0 <= s.x < self.board_size.x and 0 <= s.y < self.board_size.y):
            return False
        player = self.players[current_player_index]
        pos = player.get_trace()[-1]
        # m = the_move.get_move()
        # s = the_move.get_shoot()
        shoot_to_empty = self.field[s.x][s.y].is_empty()
        shoot_blank = s.x + s.y == -2 and player.get_blanks() > 0
        player_shot = self.field[s.x][s.y].is_player()
        return is_knight(pos, s) and (player_shot or shoot_to_empty or shoot_blank)

    def is_move_possible(self, current_player_index, m):
        if not (0 <= m.x < self.board_size.x and 0 <= m.y < self.board_size.y):
            return False
        player = self.players[current_player_index]
        pos = player.get_trace()[-1]
        # m = the_move.get_move()
        move_to_empty = self.field[m.x][m.y].is_empty()
        return (is_king(m, pos) or player.get_is_knight() and is_knight(m, pos)) and move_to_empty

    def execute_move(self, current_player_index, m):
        if self.is_move_possible(current_player_index, m) and \
                current_player_index == self.current_move % self.number_of_players:
            # m = the_move.get_move()
            player = self.players[current_player_index]
            pos = player.get_trace()[-1]

            self.players[current_player_index].next_position(m)
            self.field[m.x][m.y] = Cell(1, current_player_index)
            self.field[pos.x][pos.y] = Cell(2, current_player_index)

            # print possible shots after successful move
            # print('shots:')
            # for i in self.possible_shots(current_player_index):
            #     print(i)
        else:
            raise ValueError('Invalid move')

    def execute_shot(self, current_player_index, s):
        # s = the_move.get_shoot()
        if self.is_shot_possible(current_player_index, s) and \
                current_player_index == self.current_move % self.number_of_players:
            self.current_move += 1
            player = self.players[current_player_index]
            shoot_blank = s.x + s.y == -2 and player.get_blanks() > 0
            player_shot = self.field[s.x][s.y].is_player()
            # TODO: blanks
            if shoot_blank:
                player.reduce_blanks()
                # something else...
            # TODO: what if the player was shot
            elif player_shot:
                print('player was shot')
                player_to_be_killed = self.field[s.x][s.y].get_owner_id()
                # this will be needed in version 2 (mult players)
                # self.kill_this_player(player_to_be_killed)
                self.field[s.x][s.y] = Cell(3, current_player_index)
                self.is_ended_local = True  # tmp
            else:
                self.field[s.x][s.y] = Cell(3, current_player_index)
                # print possible moves after successful move
                # print('moves:')
                # for i in self.possible_moves(current_player_index):
                #     print(i)

        else:
            # pos_wrong = player.get_trace()[-1]
            # self.field[pos_wrong.x][pos_wrong.y] = Cell(0)
            # player.cancel_move()
            # pos_prev = player.get_trace()[-1]

            # self.field[pos_prev.x][pos_prev.y] = Cell(1, current_player_index)

            raise ValueError('Invalid shot')

    def kill_this_player(self, current_player_index):
        player = self.players[current_player_index]
        player.kill()

    def get_field(self):
        return self.field

    def possible_moves(self, player_index):
        player = self.players[player_index]
        pos = player.get_trace()[-1]
        is_knight_ = player.get_is_knight()
        result = [pos + de for de in self.deltas[:8] if self.is_move_possible(player_index, pos+de)]
        if is_knight_:
            result += [pos + de for de in deltas[8:] if self.is_move_possible(player_index, pos+de)]
        return result

    def possible_shots(self, player_index):
        player = self.players[player_index]
        pos = player.get_trace()[-1]
        return [pos + de for de in self.deltas[8:] if self.is_shot_possible(player_index, pos+de)]
