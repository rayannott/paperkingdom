from player import Player


class Cell:
    def __init__(self, t):
        self.t = t


class Game:
    def __init__(self, number_of_players):
        self.number_of_players = number_of_players
        self.field = [[Cell(None) for _ in range(8)] for _ in range(8)]
        p1 = Player(False, False, 0, [(2, 2)])
        p2 = Player(False, False, 0, [(5, 5)])
        self.field[2][2] = Cell(p1)
        self.field[5][5] = Cell(p2)

    def is_move_possible(self, player, move):
        moves = []
        pos = player.get_trace()[-1]
        for ind_i, i in enumerate(self.field):
            for ind_j, j in enumerate(i):
                if (
                        abs(ind_i - pos[0]) <= 1 and abs(ind_j - pos[1]) <= 1
                        and self.field[ind_i][ind_j] is None
                        or player.get_is_knight() and abs(ind_i - pos[0]) * abs(ind_j - pos[1]) == 2
                ):
                    moves.append((ind_i, ind_j))
        return True
