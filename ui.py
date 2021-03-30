from game import Game
from move import Move
from player import Position
from player import Player


def get_move():
    move = input()
    swap = move.startswith('swap ')
    m = None
    s = None
    if swap:
        move = move[5:]
    if move.startswith('move '):
        m = Position(int(move[5]), int(move[7]))
    move = move[9:]
    if move.startswith('shoot '):
        s = Position(int(move[6]), int(move[8]))
    elif move.startswith('noshoot'):
        s = Position(-1, -1)
    return Move(swap, m, s)


def draw_field(field):
    for row in field:
        for cell in row:
            # if isinstance(cell.t, Player):
            #     print(cell.t.name, end=' ')
            # else:
            #     print(cell.t)
            print(cell.t, end=' ')
        print()


NUM_PLAYERS = 2


def game_cycle():
    current_player_index = 0

    g = Game(NUM_PLAYERS)
    game_ended = False

    f = g.get_field()
    draw_field(f)

    while not game_ended:
        # let's print this out
        print(current_player_index)
        move = get_move()
        try:
            g.execute_move(current_player_index, move)
        except ValueError as e:
            # it doesn't show anything otherwise
            print(e)
            continue
        # ? is this to keep track of what player's move it is ? twice ?
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        game_ended = g.is_ended()

        f = g.get_field()
        draw_field(f)


if __name__ == '__main__':
    game_cycle()
