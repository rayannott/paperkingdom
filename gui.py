import pygame
import pygame_gui
import gui_utils

from game import Game
from move import Move
from player import Position
from player import Player

WIDTH = 1200
HEIGHT = 1000
LMARGIN = 200
RMARGIN = 200
NUM_PLAYERS = 2

g = Game(NUM_PLAYERS)
window_surface, manager, clock, base_panel, board = gui_utils.init_layout(WIDTH, HEIGHT, LMARGIN, RMARGIN)
buttons = gui_utils.generate_field(manager, board, g)

is_running = True
move = None
shoot = None
current_player = 0
while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                for indrow, row in enumerate(buttons):
                    for indbutt, butt in enumerate(row):
                        if event.ui_element == butt:
                            if move is None:
                                move = Position(indrow, indbutt)
                            else:
                                shoot = Position(indrow, indbutt)
                                try:
                                    g.execute_move(current_player, Move(False, move, shoot))
                                    move = None
                                    shoot = None
                                    gui_utils.set_text_to_buttons(buttons, g)
                                    current_player = (current_player + 1) % NUM_PLAYERS
                                except ValueError as e:
                                    print(e)
                                    continue


                print('clicked button', move, shoot)
        manager.process_events(event)

    manager.update(time_delta)
    manager.draw_ui(window_surface)

    pygame.display.update()