from game import Game
from move import Move
from Player import Position


def get_move():
    move = input()
    swap = move.startswith('swap ')
    if swap:
        move = move[5:]
    if move.startswith('move '):
        m = Position(int(move[5]), int(move[7]))
    move = move[9:]
    if move.startswith('shoot '):
        s = Position(int(move[7]), int(move[9]))
    return Move(swap, m, s)


NUM_PLAYERS = 2


def game_cycle():
    players = list(range(NUM_PLAYERS))
    current_player_index = 0

    g = Game(NUM_PLAYERS)
    game_ended = False

    while not game_ended:
        move = get_move()
        g.move(players[current_player_index], move)
        game_ended = True


if __name__ == '__main__':
    game_cycle()
