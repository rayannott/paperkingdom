import pathlib
import pygame
import pygame_gui


pygame.font.init()
# TODO add new fonts
assets_dir = pathlib.Path('assets'); dir_name = pathlib.Path('font.ttf')
FONT_SMALL = pygame.font.Font(assets_dir/dir_name, 14)
FONT_NORM = pygame.font.Font(assets_dir/dir_name, 20)
FONT_BIG = pygame.font.Font(assets_dir/dir_name, 34)
FONT_HUGE = pygame.font.Font(assets_dir/dir_name, 50)


def paint(s: str, color: str = '#FFFFFF', size=4):
    '''
    Returns html-colored string s
    '''
    return f'<font color={color} size={size}>{s}</font>'


def init_layout(width, height, button_margin):
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
    board_size = 0.9 * height
    left_margin = (width - board_size) // 2
    top_margin = (height - board_size) // 2
    board = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((left_margin + 40, top_margin), (board_size, board_size)),
        manager=manager,
        container=base_panel,
        object_id='board'
    )

    # coordinate labels:
    label_rect = pygame.Rect((0, 0), (25, 25))
    w, h = board.get_container().get_rect().size
    TILE_SIZE = w // 12
    label_rect.center = (board.get_relative_rect().bottomleft[0] + TILE_SIZE//2, board.get_relative_rect().bottomleft[1] + 10)
    # TODO: show coordinate labels
    label = pygame_gui.elements.UILabel(
        relative_rect=label_rect,
        text='A',
        manager=manager,
        container=base_panel
    )

    left_board = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((0, 0), (left_margin, height)),
        manager=manager,
        container=base_panel,
        object_id='leftboard'
    )
    total_empty = button_margin * 3
    button_size_x = (left_margin - total_empty) / 2
    button_size_y = 40
    textbox_width = button_size_x*2 + button_margin
    info_textbox_height = 400
    restart_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(button_margin, button_margin, button_size_x, button_size_y),
        text='RESTART',
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
    save_game_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(button_margin*2 + button_size_x, button_margin, button_size_x, button_size_y),
        text='SAVE',
        manager=manager,
        container=left_board,
        object_id='save',
        anchors={
            'left': 'left',
            'right': 'right',
            'top': 'top',
            'bottom': 'bottom'
        }
    )
    game_info_textbox = pygame_gui.elements.UITextBox(
        f'{paint("RED", "#F2350C")} to move<br>',
        relative_rect=pygame.Rect(button_margin, button_margin*2 + button_size_y, textbox_width, info_textbox_height),
        manager=manager,
        container=left_board,
        object_id='info_textbox',
        anchors={
            'left': 'left',
            'right': 'right',
            'top': 'top',
            'bottom': 'bottom'
        }
    )
    game_logs_textbox = pygame_gui.elements.UITextBox(
        f'',
        relative_rect=pygame.Rect(button_margin, button_margin*3 + button_size_y + info_textbox_height, textbox_width, info_textbox_height//4),
        manager=manager,
        container=left_board,
        object_id='log_textbox',
        anchors={
            'left': 'left',
            'right': 'right',
            'top': 'top',
            'bottom': 'bottom'
        }
    )
    return window_surface, manager, clock, base_panel, board, left_board, restart_button, save_game_button, game_info_textbox, game_logs_textbox


def generate_field(manager, board, game, current_player):
    rows = 12
    columns = 12
    w, h = board.get_container().get_rect().size
    w, h = w / rows, h / columns
    buttons = []
    for indrow, row in enumerate(game.board):
        this_row = []
        for indcell, cell in enumerate(row):
            rect = pygame.Rect(w * indcell, h * indrow, w, h)
            if cell.is_player():
                butt = pygame_gui.elements.UIButton(
                    relative_rect=rect,
                    text='',
                    manager=manager,
                    container=board,
                    object_id=f'player{cell.player_id}'
                )
                if current_player == cell.player_id:
                    butt.disable()
            else:
                if indrow in {2, 9} and 2 <= indcell <= 9 or indcell in {2, 9} and 2 <= indrow <= 9:
                    empty_cell_obj_id = 'arena_border'
                elif indrow in {5, 6} and indcell in {5, 6}:
                    empty_cell_obj_id = 'arena_center'
                else:
                    empty_cell_obj_id = None
                butt = pygame_gui.elements.UIButton(
                    relative_rect=rect,
                    text='',
                    manager=manager,
                    container=board,
                    object_id=empty_cell_obj_id
                )
            this_row.append(butt)
        buttons.append(this_row)
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
    for row_id, row in enumerate(game.board):
        for col_id, cell in enumerate(row):
            if cell.is_trace():
                kill_create_button(buttons, row_id, col_id, '.', manager, board, f'trace{cell.player_id}', True)
            elif cell.is_shot():
                kill_create_button(buttons, row_id, col_id, '', manager, board, 'shot', True)
            elif cell.is_player():
                kill_create_button(buttons, row_id, col_id, '',
                                    manager, board, f'player{cell.player_id}', current_player == cell.player_id)


def check_field_buttons(event, buttons):
    for indrow, row in enumerate(buttons):
        for indbutt, butt in enumerate(row):
            if event.ui_element == butt:
                return indbutt, indrow
    return -1, -1
