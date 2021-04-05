from game import Game
from move import Move
from player import Position
from player import Player


def get_move():
    move = input().split()
    swap = move[0] == 'swap'
    m = None
    s = None
    if swap:
        move = move[1:]
    if move[0] in ['move', 'm']:
        m = Position(int(move[1]), int(move[2]))
        move = move[3:]
    else:
        raise ValueError('Move input could not be parsed')

    if move[0] in ['noshoot', 'ns']:
        s = Position(-1, -1)
    else:
        if move[0] in ['shoot', 's']:
            s = Position(int(move[1]), int(move[2]))

    return Move(swap, m, s)


def draw_field(field):
    for row in field:
        for cell in row:
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
        print('Player ', current_player_index, "'s turn", sep='')
        move = get_move()
        try:
            g.execute_move(current_player_index, move)
        except ValueError as e:
            # it doesn't show anything otherwise
            print(e)
            continue
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        game_ended = g.is_ended()

        f = g.get_field()
        draw_field(f)


if __name__ == '__main__':
    game_cycle()
