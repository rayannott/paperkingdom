import pygame
import pygame_gui
import gui_utils

from gui_utils import GUI
from game import Game
from move import Move
from player import Position
from player import Player

WIDTH = 1000
HEIGHT = 600
LMARGIN = 200
RMARGIN = 200
BMARGIN = 10
assert WIDTH > LMARGIN + RMARGIN


def init_board():
    board_size = Position(8, 8)
    players_ = [Player(False, False, 0, [Position(2, 2)]),
                Player(False, False, 0, [Position(5, 5)])]
    g_ = Game(players_, board_size)
    n_ = len(players_)
    c_ = 0
    m_ = None
    s_ = None
    return g_, n_, c_, m_, s_


game, num_players, current_player, move, shoot = init_board()
gui = GUI(WIDTH, HEIGHT, LMARGIN, RMARGIN, BMARGIN, game, current_player)

is_running = True
while is_running:
    time_delta = gui.get_time_delta()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == gui.restart_button:
                    game, num_players, current_player, move, shoot = init_board()
                    gui.kill_all_buttons()
                    gui.generate_field(game, current_player)
                    continue
                indrow, indbutt = gui.check_field_buttons(event)
                if move is None:
                    move = Position(indrow, indbutt)
                    try:
                        m = Move(False, move, None)
                        game.execute_move(current_player, m)
                        sequence = gui.update_sequence('Player ' + str(current_player) + ': shoot')
                    except ValueError as e:
                        print(e)
                        move = None
                        shoot = None
                        continue
                    gui.update_buttons(game, current_player)
                else:
                    shoot = Position(indrow, indbutt)
                    try:
                        m = Move(False, move, shoot)
                        game.execute_shot(current_player, m)
                        print('Successful move', move, shoot)
                        move = None
                        shoot = None
                        current_player = (current_player + 1) % num_players
                        if game.is_ended():
                            gui.board.disable()
                            sequence = gui.update_sequence('game ended')
                        else:
                            sequence = gui.update_sequence('Player ' + str(current_player) + ': move shoot')
                    except ValueError as e:
                        print(e)
                        shoot = None
                        continue
                    gui.update_buttons(game, current_player)

        gui.manager.process_events(event)

    gui.manager.update(time_delta)
    gui.manager.draw_ui(gui.window_surface)

    pygame.display.update()
