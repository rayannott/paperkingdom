from player import Player
from player import Position


# players - list of Player, field_size - tuple if ints,
# is_singleplayer - bool, difficulty - double from
# 0. to 1. (only if is_singleplayer)
class Configuration:
    def __init__(self, players, field_size):
        pass


class Cell:
    """
    The t parameter is a string; it has a form of <character,number,extra_parameters>
    Here are some examples:
    'p4' is a player 4
    'o2' is a trace left by a player 2
    'o1u' is a trace of a player 1 that has been used in a tetra
    'x0' is a shot made by a player 0
    'n-' is an empty cell
    'w-' is a wall
    't-' is a target
    """

    def __init__(self, t):
        self.t = t

    def is_player(self):
        if self.t[0] == 'p':
            return True, int(self.t[1:])
        else:
            return False, 0

    def is_shot(self):
        if self.t[0] == 'x':
            return True, int(self.t[1:])
        else:
            return False, 0

    def is_target(self):
        if self.t[0] == 't':
            return True
        else:
            return False

    def is_trace_used(self):
        if self.t[-1] == 'u':
            return True
        else:
            return False

    def is_trace(self):
        if self.t[0] == 'o':
            return True
        else:
            return False

    def is_empty(self):
        if self.t[0] == 'n':
            return True
        else:
            return False


board_x, board_y = 8, 8
positions = [Position(2, 2), Position(5, 5)]
names = ['Alan', 'Bill']


# is_king = lambda pos1, pos2: abs(pos1.x - pos2.x) <= 1 and abs(pos1.y - pos2.y) <= 1
# is_knight = lambda pos1, pos2: abs(pos1.x - pos2.x) * abs(pos1.y - pos2.y) == 2

# if two positions given are a KING away from one another
def is_king(pos1, pos2):
    return abs(pos1.x - pos2.x) <= 1 and abs(pos1.y - pos2.y) <= 1


# -/- KNIGHT -/-
def is_knight(pos1, pos2):
    return abs(pos1.x - pos2.x) * abs(pos1.y - pos2.y) == 2


class Game:
    # TODO: [in __init__] a clever way to initialise a field configuration: number of players, size of the \
    #  field. (init_positions, (A times B))
    def __init__(self, number_of_players):

        self.number_of_players = number_of_players
        self.field = [[Cell('n-') for _ in range(board_y)] for _ in range(board_x)]
        # [positions[i] must be in a list here:
        self.players = [Player(True, False, 0, [positions[i]], names[i]) for i in range(number_of_players)]
        self.current_move = 0
        self.is_ended_local = False
        for ind, i in enumerate(self.players):
            self.field[positions[ind].x][positions[ind].y] = Cell('p' + str(ind))  # it has been Cell(i)
        # self.field[2][2] = Cell(p1)
        # self.field[5][5] = Cell(p2)

    def is_ended(self):
        return self.is_ended_local

    def get_field(self):
        return self.field

    def is_move_possible(self, current_player_index, the_move):
        player = self.players[current_player_index]
        pos = player.get_trace()[-1]
        m = the_move.get_move()
        s = the_move.get_shoot()
        # TODO: a place for \
        #  swap = the_move.get_swap()

        move_to_empty = self.field[m.x][m.y].is_empty()
        shoot_to_empty = self.field[s.x][s.y].is_empty()
        shoot_blank = s.x + s.y == -2 and player.get_blanks() > 0
        player_shot, _ = self.field[s.x][s.y].is_player()
        # TODO: catch attempts to shoot or move out of the field
        if (is_king(m, pos) or player.get_is_knight() and is_knight(m, pos)) and move_to_empty:
            if is_knight(m, s) and (player_shot or shoot_to_empty or shoot_blank):
                # TODO: blanks
                if shoot_blank:
                    player.reduce_blanks()
                # TODO: what if the player was shot
                if player_shot:
                    print('player was shot')
                    self.is_ended_local = True
                return True
            else:
                return False
        else:
            return False

    def execute_move(self, current_player_index, the_move):
        if self.is_move_possible(current_player_index, the_move) and \
                current_player_index == self.current_move % self.number_of_players:
            m = the_move.get_move()
            s = the_move.get_shoot()
            player = self.players[current_player_index]
            pos = player.get_trace()[-1]
            self.players[current_player_index].next_position(the_move.get_move())
            # changing the field
            self.field[m.x][m.y] = Cell('p' + str(current_player_index))
            self.field[s.x][s.y] = Cell('x' + str(current_player_index))
            self.field[pos.x][pos.y] = Cell('o' + str(current_player_index))

            self.current_move += 1
        else:
            raise ValueError('Invalid move')
