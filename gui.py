import pygame
import pygame_gui
import gui_utils

from game import Game
from move import Move
from player import Position
from player import Player

WIDTH = 1000
HEIGHT = 600
LMARGIN = 200
RMARGIN = 200
BMARGIN = 10


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


g, num_players, current_player, move, shoot = init_board()
(window_surface, manager, clock, base_panel, board, left_board,
 swap_button, tetra_button, restart_button) = gui_utils.init_layout(WIDTH, HEIGHT, LMARGIN, RMARGIN, BMARGIN)
buttons = gui_utils.generate_field(manager, board, g, current_player)


is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == restart_button:
                    g, num_players, current_player, move, shoot = init_board()
                    gui_utils.kill_all_buttons(buttons)
                    buttons = gui_utils.generate_field(manager, board, g, current_player)
                    continue
                indrow, indbutt = gui_utils.check_field_buttons(event, buttons)
                if move is None:
                    move = Position(indrow, indbutt)
                    try:
                        m = Move(False, move, None)
                        g.execute_move(current_player, m)
                    except ValueError as e:
                        print(e)
                        move = None
                        shoot = None
                        continue
                    gui_utils.update_buttons(buttons, manager, board, g, current_player)
                else:
                    shoot = Position(indrow, indbutt)
                    try:
                        m = Move(False, move, shoot)
                        g.execute_shot(current_player, m)
                        print('Successful move', move, shoot)
                        move = None
                        shoot = None
                        current_player = (current_player + 1) % num_players
                        if g.is_ended():
                            board.disable()
                    except ValueError as e:
                        print(e)
                        shoot = None
                        continue
                    gui_utils.update_buttons(buttons, manager, board, g, current_player)

        manager.process_events(event)

    manager.update(time_delta)
    manager.draw_ui(window_surface)

    pygame.display.update()
