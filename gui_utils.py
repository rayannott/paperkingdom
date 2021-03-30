import pygame
import pygame_gui


def init_layout(width, height, l_margin, r_margin):
    pygame.init()

    pygame.display.set_caption('Quick Start')
    window_surface = pygame.display.set_mode((width, height))

    manager = pygame_gui.UIManager((width, height))
    clock = pygame.time.Clock()
    base_panel = pygame_gui.elements.ui_panel.UIPanel(
        relative_rect=pygame.Rect((0, 0), (width, height)),
        manager=manager,
        starting_layer_height=1
    )
    board = pygame_gui.elements.ui_panel.UIPanel(
        relative_rect=pygame.Rect((l_margin, 0), (width - l_margin - r_margin, height)),
        manager=manager,
        starting_layer_height=1,
        container=base_panel
    )

    return window_surface, manager, clock, base_panel, board


def generate_field(manager, board, game):
    f = game.get_field()
    rows = len(f)
    columns = len(f[0])
    buttons = []
    for indrow, row in enumerate(f):
        buttons.append([])
        for indcell, cell in enumerate(row):
            w, h = board.get_container().get_rect().size
            w, h = w // rows, h // columns
            rect = pygame.Rect(w * indrow, h * indcell, w, h)
            butt = pygame_gui.elements.ui_button.UIButton(
                relative_rect=rect,
                text=cell.t,
                manager=manager,
                container=board
            )
            buttons[-1].append(butt)
    return buttons


def set_text_to_buttons(buttons, game):
    f = game.get_field()
    for rowf, rowg in zip(f, buttons):
        for cell, button in zip(rowf, rowg):
            button.set_text(cell.t)
