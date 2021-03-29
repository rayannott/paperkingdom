from player import Player
from player import Position


class Cell:
    def __init__(self, t):
        self.t = t


class Game:
    def __init__(self, number_of_players):
        self.number_of_players = number_of_players
        self.field = [[Cell(None) for _ in range(8)] for _ in range(8)]
        positions = [Position(2, 2), Position(5, 5)]
        names = ['Alan', 'Bill']
        self.players = [Player(False, False, 0, positions[i], names[i]) for i in range(number_of_players)]
        self.current_move = 0
        for ind, i in enumerate(self.players):
            self.field[positions[ind].x][positions[ind].y] = Cell(i)
        # self.field[2][2] = Cell(p1)
        # self.field[5][5] = Cell(p2)

    def is_move_possible(self, current_player_index, the_move):
        player = self.players[current_player_index]
        pos = player.get_trace()[-1]
        m = the_move.get_move()
        s = the_move.get_shoot()
        # TODO: a place for swap = the_move.get_swap()

        # for ind_i, i in enumerate(self.field):
        #     for ind_j, j in enumerate(i):
        #         if (
        #                 abs(ind_i - pos.x) <= 1 and abs(ind_j - pos.y) <= 1
        #                 and self.field[ind_i][ind_j] is None
        #                 or player.get_is_knight() and abs(ind_i - pos.x) * abs(ind_j - pos.y) == 2
        #         ):
        #             moves.append(Position(ind_i, ind_j))

        if (
                (abs(m.x - pos.x) <= 1 and abs(m.y - pos.y) <= 1 or player.get_is_knight() and
                 abs(m.x - pos.x) * abs(m.y - pos.y) == 2) and self.field[m.x][m.y] is None
        ):
            if (
                    abs(m.x - s.x) * abs(m.y - s.y) == 2 and
                    (isinstance(self.field[s.x][s.y], Player) or self.field[s.x][s.y] is None or
                     (m.x + m.y == -2 and player.get_blanks() > 0))
            ):
                return True
            else:
                return False
        else:
            return False

    def execute_move(self, current_player_index, the_move):
        if (
                self.is_move_possible(current_player_index,
                                      the_move) and current_player_index == self.current_move % self.number_of_players
        ):
            self.players[current_player_index].next_position(the_move.get_move())
            self.current_move += 1
        else:
            raise ValueError
