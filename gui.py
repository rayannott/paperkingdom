import datetime
from typing import Literal

import pygame
import pygame_gui

import gui_utils
from gui_utils import paint
from board import Board
from utils import Pos, CompleteMove
import exceptions as exc
from engine import PickBest, PickRandom, Minimax

WIDTH = 1000
HEIGHT = 600
LMARGIN = 200
RMARGIN = 200
BMARGIN = 10

def main(engine_: Literal['minimax', 'pickbest', 'pickrandom'] | None = None):
    g = Board()
    move, shoot = None, None
    (window_surface, manager, clock, base_panel, board, left_board,
        restart_button, save_game_button, game_info_textbox) = gui_utils.init_layout(WIDTH, HEIGHT, LMARGIN, RMARGIN, BMARGIN)
    buttons = gui_utils.generate_field(manager, board, g, g.player_to_move)

    if engine_ == 'minimax':
        engine = Minimax(player_id=1, board=g, depth=2, randomize=True)
    elif engine_ == 'pickbest':
        engine = PickBest(player_id=1, board=g, randomize=True, verbose=True)
    elif engine_ == 'pickrandom':
        engine = PickRandom(player_id=1, board=g)

    is_running = True
    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == restart_button:
                        g = Board()
                        move, shoot = None, None
                        (window_surface, manager, clock, base_panel, board, left_board,
                            restart_button, save_game_button, game_info_textbox) = gui_utils.init_layout(WIDTH, HEIGHT, LMARGIN, RMARGIN, BMARGIN)
                        buttons = gui_utils.generate_field(manager, board, g, g.player_to_move)
                        engine = PickBest(player_id=1, board=g, randomize=True, verbose=True)
                        continue
                    elif event.ui_element == save_game_button:
                        with open('games.log', 'a') as f:
                            print(f'[{datetime.datetime.now().strftime("%d.%m.%Y %H:%M")}]', file=f)
                            if engine_:
                                print(f'# against the {engine_} bot', file=f)
                                print(g.get_ngd(), file=f)
                            else:
                                print('# player vs. player', file=f)
                            print(file=f)
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
                        else:
                            if engine_:
                                try:
                                    engine.make_move()
                                except exc.GameIsOverException as e:
                                    print(e)
                                g.info()
                                if g.victor is not None:
                                    board.disable()
                                    g.info()
                            game_info_textbox.set_text(
                                    f'{paint("BLUE", "#0C6EF2") if g.player_to_move else paint("RED", "#F2350C")} to move<br>{paint(g.get_ngd(), "#BAE2CB")}'
                                )
                        gui_utils.update_buttons(buttons, manager, board, g, g.player_to_move)

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(window_surface)

        pygame.display.update()
