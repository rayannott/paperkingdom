from player import Player
from player import Position



board_x, board_y = 8, 8
positions = [Position(2, 2), Position(5, 5)]
names = ['Alan', 'Bill']


# if two positions given are a KING away from one another
def is_king(pos1, pos2):
    return abs(pos1.x - pos2.x) <= 1 and abs(pos1.y - pos2.y) <= 1


# -/- KNIGHT -/-
def is_knight(pos1, pos2):
    return abs(pos1.x - pos2.x) * abs(pos1.y - pos2.y) == 2


class Game:
    def __init__(self, number_of_players):

        self.number_of_players = number_of_players
        self.field = [[Cell(0, -1, 0) for _ in range(board_y)] for _ in range(board_x)]
        self.players = [Player(True, False, 0, [positions[i]], names[i]) for i in range(number_of_players)]
        self.current_move = 0
        self.is_ended_local = False
        for ind, i in enumerate(self.players):
            self.field[positions[ind].x][positions[ind].y] = Cell(1, ind)

    def is_ended(self):
        return self.is_ended_local

    def get_field(self):
        return self.field

    def is_shot_possible(self, current_player_index, the_move):
        player = self.players[current_player_index]
        pos = player.get_trace()[-1]
        s = the_move.get_shoot()
        shoot_to_empty = self.field[s.x][s.y].is_empty()
        shoot_blank = s.x + s.y == -2 and player.get_blanks() > 0
        player_shot, _ = self.field[s.x][s.y].is_player()
        return is_knight(m, s) and (player_shot or shoot_to_empty or shoot_blank)

    def is_move_possible(self, current_player_index, the_move):
        player = self.players[current_player_index]
        pos = player.get_trace()[-1]
        m = the_move.get_move()
        move_to_empty = self.field[m.x][m.y].is_empty()
        return (is_king(m, pos) or player.get_is_knight() and is_knight(m, pos)) and move_to_empty

    def execute_move(self, current_player_index, the_move):
        if self.is_move_possible(current_player_index, the_move) and \
                current_player_index == self.current_move % self.number_of_players:
            m = the_move.get_move()
            player = self.players[current_player_index]
            pos = player.get_trace()[-1]

            self.players[current_player_index].next_position(the_move.get_move())
            self.field[m.x][m.y] = Cell(1, current_player_index)
            self.field[pos.x][pos.y] = Cell(2, current_player_index)
        else:
            raise ValueError('Invalid move')

    def execute_shot(self, current_player_index, the_move):
        player = self.players[current_player_index]

        if self.is_shot_possible(current_player_index, the_move) and \
                current_player_index == self.current_move % self.number_of_players:
            self.field[s.x][s.y] = Cell(3, current_player_index)
            self.current_move += 1
            shoot_blank = s.x + s.y == -2 and player.get_blanks() > 0
            player_shot, _ = self.field[s.x][s.y].is_player()
            # TODO: blanks
            if shoot_blank:
                player.reduce_blanks()
            # TODO: what if the player was shot
            if player_shot:
                print('player was shot')
                self.kill_this_player(current_player_index)
                self.is_ended_local = True  # tmp
            return True

        else:
            pos_wrong = player.get_trace()[-1]
            self.field[pos_wrong.x][pos_wrong.y] = Cell('n-')
            player.cancel_move()
            pos_prev = player.get_trace()[-1]

            self.field[pos_prev.x][pos_prev.y] = Cell(1, current_player_index)

            raise ValueError('Invalid shot')

    def kill_this_player(self, current_player_index):
        player = self.players[current_player_index]
        player.kill()

