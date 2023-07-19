import pygame
import pygame_gui
import gui_utils

from board import Board
from utils import Pos, CompleteMove
import exceptions as exc
from engine import PickBest

WIDTH = 1000
HEIGHT = 600
LMARGIN = 200
RMARGIN = 200
BMARGIN = 10


g = Board()
move, shoot = None, None
(window_surface, manager, clock, base_panel, board, left_board,
 swap_button, tetra_button, restart_button) = gui_utils.init_layout(WIDTH, HEIGHT, LMARGIN, RMARGIN, BMARGIN)
buttons = gui_utils.generate_field(manager, board, g, g.player_to_move)

engine = PickBest(player_id=1, board=g, randomize=True, verbose=True)
ENGINE_ON = True

is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == restart_button:
                    continue
                indbutt, indrow = gui_utils.check_field_buttons(event, buttons)
                print(indbutt, indrow)
                if move is None:
                    move = Pos(indrow, indbutt)
                else:
                    shoot = Pos(indrow, indbutt)
                    cm = CompleteMove(move, shoot)
                    try:
                        g.execute_complete_move(cm)
                        print('Successful complete move:', cm)
                        move = None
                        shoot = None
                        if g.victor is not None:
                            board.disable()
                            g.info()
                    except exc.InvalidCompleteMoveException as e:
                        print(e)
                        move = None
                        shoot = None
                        continue
                    # except exc.GameIsOverException as e:
                    #     print(e)
                    #     board.disable()
                    #     print(g.info())
                    else:
                        if ENGINE_ON:
                            try:
                                engine.make_move()
                            except exc.GameIsOverException as e:
                                print(e)
                            g.info()
                            if g.victor is not None:
                                board.disable()
                                print(g.info())
                    gui_utils.update_buttons(buttons, manager, board, g, g.player_to_move)

        manager.process_events(event)

    manager.update(time_delta)
    manager.draw_ui(window_surface)

    pygame.display.update()
