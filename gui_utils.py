import pygame
import pygame_gui

from player import Position
from move import Move

def init_layout(width, height, l_margin, r_margin, button_margin):
    pygame.init()

    pygame.display.set_caption('Quick Start')
    window_surface = pygame.display.set_mode((width, height))

    manager = pygame_gui.UIManager((width, height), 'theme.json')
    clock = pygame.time.Clock()
    base_panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((0, 0), (width, height)),
        manager=manager,
        object_id='base'
    )
    board_size = min(width - l_margin - r_margin, height)
    left_margin = (width - board_size) // 2
    top_margin = (height - board_size) // 2
    board = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((left_margin, top_margin), (board_size, board_size)),
        manager=manager,
        container=base_panel,
        object_id='board'
    )
    left_board = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((0, 0), (left_margin, height)),
        manager=manager,
        container=base_panel,
        object_id='leftboard'
    )
    total_empty = button_margin * 3
    button_size_x = (left_margin - total_empty) / 2
    button_size_y = 20
    swap_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(button_margin, button_margin, button_size_x, button_size_y),
        text='Swap',
        manager=manager,
        container=left_board,
        object_id='butt',
        anchors={
            'left': 'left',
            'right': 'right',
            'top': 'top',
            'bottom': 'bottom'
        }
    )
    tetra_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(left_margin - button_margin - button_size_x, button_margin, button_size_x, button_size_y),
        text='Tetra',
        manager=manager,
        container=left_board,
        object_id='butt',
        anchors={
            'left': 'left',
            'right': 'right',
            'top': 'top',
            'bottom': 'bottom'
        }
    )
    restart_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(button_margin, 2 * button_margin + button_size_y, button_size_x, button_size_y),
        text='Restart',
        manager=manager,
        container=left_board,
        object_id='restart',
        anchors={
            'left': 'left',
            'right': 'right',
            'top': 'top',
            'bottom': 'bottom'
        }
    )
    return window_surface, manager, clock, base_panel, board, left_board, swap_button, tetra_button, restart_button


def generate_field(manager, board, game, current_player):
    f = game.get_field()
    rows = len(f)
    columns = len(f[0])
    w, h = board.get_container().get_rect().size
    w, h = w / rows, h / columns
    buttons = []
    for indrow, row in enumerate(f):
        buttons.append([])
        for indcell, cell in enumerate(row):
            rect = pygame.Rect(w * indrow, h * indcell, w, h)
            if cell.is_player():
                butt = pygame_gui.elements.UIButton(
                    relative_rect=rect,
                    text=str(cell),
                    manager=manager,
                    container=board,
                    object_id='player'
                )
                if current_player == cell.get_owner_id():
                    butt.disable()
            else:
                butt = pygame_gui.elements.UIButton(
                    relative_rect=rect,
                    text=str(cell),
                    manager=manager,
                    container=board
                )
            buttons[-1].append(butt)
    return buttons


def kill_create_button(buttons, index1, index2, text, manager, board, object_id, disable):
    rect = buttons[index1][index2].get_relative_rect()
    buttons[index1][index2].kill()
    buttons[index1][index2] = pygame_gui.elements.UIButton(
        relative_rect=rect,
        text=text,
        manager=manager,
        container=board,
        object_id=object_id
    )
    if disable:
        buttons[index1][index2].disable()


def kill_all_buttons(buttons):
    for row in buttons:
        for butt in row:
            butt.kill()


def update_buttons(buttons, manager, board, game, current_player):
    f = game.get_field()
    for index1, (rowf, rowg) in enumerate(zip(f, buttons)):
        for index2, (cell, button) in enumerate(zip(rowf, rowg)):
            # if button.object_ids[2] in [None, 'player']:
                if cell.is_trace():
                    kill_create_button(buttons, index1, index2, str(cell), manager, board, 'trace', True)
                elif cell.is_shot():
                    kill_create_button(buttons, index1, index2, str(cell), manager, board, 'shot', True)
                elif cell.is_player():
                    kill_create_button(buttons, index1, index2, str(cell),
                                       manager, board, 'player', current_player == cell.get_owner_id())
                # print(cell, end=' ')
        # print()


def check_field_buttons(event, buttons):
    for indrow, row in enumerate(buttons):
        for indbutt, butt in enumerate(row):
            if event.ui_element == butt:
                return indrow, indbutt
    return -1, -1
