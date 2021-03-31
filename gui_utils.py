import pygame
import pygame_gui


def init_layout(width, height, l_margin, r_margin):
    pygame.init()

    pygame.display.set_caption('Quick Start')
    window_surface = pygame.display.set_mode((width, height))

    manager = pygame_gui.UIManager((width, height), 'theme.json')
    clock = pygame.time.Clock()
    base_panel = pygame_gui.elements.ui_panel.UIPanel(
        relative_rect=pygame.Rect((0, 0), (width, height)),
        manager=manager,
        starting_layer_height=1
    )
    board_size = min(width - l_margin - r_margin, height)
    left_margin = (width - board_size) // 2
    top_margin = (height - board_size) // 2
    board = pygame_gui.elements.ui_panel.UIPanel(
        relative_rect=pygame.Rect((left_margin, top_margin), (board_size, board_size)),
        manager=manager,
        starting_layer_height=1,
        container=base_panel,
        object_id='board'
    )
    butt = pygame_gui.elements.ui_button.UIButton(
        relative_rect=pygame.Rect(10, 10, 100, 100),
        text='hello',
        manager=manager,
        container=base_panel,
        object_id='butt',
        anchors={
            'left': 'left',
            'right': 'right',
            'top': 'top',
            'bottom': 'bottom'
        }
    )
    return window_surface, manager, clock, base_panel, board


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
            if cell.is_player()[0]:
                print(indrow, indcell, 'is player')
                butt = pygame_gui.elements.ui_button.UIButton(
                    relative_rect=rect,
                    text=cell.t,
                    manager=manager,
                    container=board,
                    object_id='player'
                )
                if current_player == cell.is_player()[1]:
                    butt.disable()
            else:
                butt = pygame_gui.elements.ui_button.UIButton(
                    relative_rect=rect,
                    text=cell.t,
                    manager=manager,
                    container=board
                )
            buttons[-1].append(butt)
    return buttons


def update_buttons(buttons, manager, board, game, current_player):
    f = game.get_field()
    for index1, (rowf, rowg) in enumerate(zip(f, buttons)):
        for index2, (cell, button) in enumerate(zip(rowf, rowg)):
            if cell.is_trace():
                rect = button.get_relative_rect()
                button.kill()
                buttons[index1][index2] = pygame_gui.elements.ui_button.UIButton(
                    relative_rect=rect,
                    text=cell.t,
                    manager=manager,
                    container=board,
                    object_id='trace'
                )
                buttons[index1][index2].disable()
            elif cell.is_shot()[0]:
                rect = button.get_relative_rect()
                button.kill()
                buttons[index1][index2] = pygame_gui.elements.ui_button.UIButton(
                    relative_rect=rect,
                    text=cell.t,
                    manager=manager,
                    container=board,
                    object_id='shot'
                )
                buttons[index1][index2].disable()
            elif cell.is_player()[0]:
                rect = button.get_relative_rect()
                button.kill()
                buttons[index1][index2] = pygame_gui.elements.ui_button.UIButton(
                    relative_rect=rect,
                    text=cell.t,
                    manager=manager,
                    container=board,
                    object_id='player'
                )
                if current_player == cell.is_player()[1]:
                    buttons[index1][index2].disable()
            else:
                button.set_text(cell.t)
