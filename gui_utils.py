import pygame
import pygame_gui

from game import Game
from player import Position
from player import Player


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


class GUI:

    def __init__(self, width, height, l_margin, r_margin, button_margin, window_surface):
        self.r_margin = r_margin
        self.window_surface = window_surface
        self.game, self.num_players, self.current_player, self.move, self.shoot = init_board()

        self.manager = pygame_gui.UIManager((width, height), 'theme.json')
        self.clock = pygame.time.Clock()
        self.base_panel = pygame_gui.elements.ui_panel.UIPanel(
            relative_rect=pygame.Rect((0, 0), (width, height)),
            manager=self.manager,
            starting_layer_height=1,
            object_id='base'
        )
        self.left_panel = pygame_gui.elements.ui_panel.UIPanel(
            relative_rect=pygame.Rect((0, 0), (l_margin, height)),
            manager=self.manager,
            starting_layer_height=1,
            container=self.base_panel,
            object_id='left_panel'
        )
        middle_panel_size = width - l_margin - r_margin
        self.middle_panel = pygame_gui.elements.ui_panel.UIPanel(
            relative_rect=pygame.Rect((l_margin, 0), (middle_panel_size, height)),
            manager=self.manager,
            starting_layer_height=1,
            container=self.base_panel,
            object_id='middle_panel'
        )
        self.right_panel = pygame_gui.elements.ui_panel.UIPanel(
            relative_rect=pygame.Rect((width - r_margin, 0), (r_margin, height)),
            manager=self.manager,
            starting_layer_height=1,
            container=self.base_panel,
            object_id='right_panel'
        )
        self.sequence = pygame_gui.elements.ui_text_box.UITextBox(
            relative_rect=pygame.Rect(0, 0, r_margin - 7, 80),
            html_text='Player ' + str(self.current_player) + ': move shoot',
            manager=self.manager,
            container=self.right_panel,
            object_id='sequence',
        )
        board_size = min(middle_panel_size, height) - 6
        top_margin = (height - board_size) // 2
        self.board = pygame_gui.elements.ui_panel.UIPanel(
            relative_rect=pygame.Rect((1, top_margin - 2), (board_size, board_size)),
            manager=self.manager,
            starting_layer_height=1,
            container=self.middle_panel,
            object_id='board'
        )

        total_empty = button_margin * 3
        button_size_x = (l_margin - total_empty) / 2
        button_size_y = 20
        self.swap_button = pygame_gui.elements.ui_button.UIButton(
            relative_rect=pygame.Rect(button_margin, button_margin, button_size_x, button_size_y),
            text='Swap',
            manager=self.manager,
            container=self.left_panel,
            object_id='butt'
        )
        self.tetra_button = pygame_gui.elements.ui_button.UIButton(
            relative_rect=pygame.Rect(l_margin - button_margin - button_size_x, button_margin, button_size_x,
                                      button_size_y),
            text='Tetra',
            manager=self.manager,
            container=self.left_panel,
            object_id='butt'
        )
        self.restart_button = pygame_gui.elements.ui_button.UIButton(
            relative_rect=pygame.Rect(button_margin, 2 * button_margin + button_size_y, button_size_x, button_size_y),
            text='Restart',
            manager=self.manager,
            container=self.left_panel,
            object_id='restart',
            anchors={
                'left': 'left',
                'right': 'right',
                'top': 'top',
                'bottom': 'bottom'
            }
        )
        self.buttons = None
        self.generate_field(self.game, self.current_player)

    def generate_field(self, game, current_player):
        f = game.get_field()
        rows = len(f)
        columns = len(f[0])
        w, h = self.board.get_container().get_rect().size
        w1, h1 = w // rows, h // columns
        diff1, diff2 = w - w1 * rows, h - h1 * columns
        self.buttons = []
        for indrow, row in enumerate(f):
            self.buttons.append([])
            for indcell, cell in enumerate(row):
                rect = pygame.Rect(w1 * indrow + diff1 // 2, h1 * indcell + diff2 // 2, w1, h1)
                if cell.is_player():
                    butt = pygame_gui.elements.ui_button.UIButton(
                        relative_rect=rect,
                        text=str(cell),
                        manager=self.manager,
                        container=self.board,
                        object_id='player'
                    )
                    if current_player == cell.get_owner_id():
                        butt.disable()
                else:
                    butt = pygame_gui.elements.ui_button.UIButton(
                        relative_rect=rect,
                        text=str(cell),
                        manager=self.manager,
                        container=self.board
                    )
                self.buttons[-1].append(butt)

    def kill_create_button(self, index1, index2, text, object_id, disable=False):
        rect = self.buttons[index1][index2].get_relative_rect()
        self.buttons[index1][index2].kill()
        self.buttons[index1][index2] = pygame_gui.elements.ui_button.UIButton(
            relative_rect=rect,
            text=text,
            manager=self.manager,
            container=self.board,
            object_id=object_id
        )
        if disable:
            self.buttons[index1][index2].disable()

    def kill_all_buttons(self):
        for row in self.buttons:
            for butt in row:
                butt.kill()

    def update_buttons(self, game, current_player):
        f = game.get_field()
        for index1, (rowf, rowg) in enumerate(zip(f, self.buttons)):
            for index2, (cell, button) in enumerate(zip(rowf, rowg)):
                # if button.object_ids[2] in [None, 'player']:
                if cell.is_trace():
                    self.kill_create_button(index1, index2, str(cell), 'trace', True)
                elif cell.is_shot():
                    self.kill_create_button(index1, index2, str(cell), 'shot', True)
                elif cell.is_player():
                    self.kill_create_button(index1, index2, str(cell), 'player', current_player == cell.get_owner_id())
            #     print(cell, end=' ')
            # print()

    def check_field_buttons(self, event):
        for indrow, row in enumerate(self.buttons):
            for indbutt, butt in enumerate(row):
                if event.ui_element == butt:
                    return indrow, indbutt
        return -1, -1

    def update_sequence(self, text):
        self.sequence.kill()
        self.sequence = pygame_gui.elements.ui_text_box.UITextBox(
            relative_rect=pygame.Rect(0, 0, self.r_margin - 7, 80),
            html_text=text,
            manager=self.manager,
            container=self.right_panel,
            object_id='sequence',
        )

    def game_loop(self):
        is_running = True
        while is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.restart_button:
                            self.game, self.num_players, self.current_player, self.move, self.shoot = init_board()
                            self.kill_all_buttons()
                            self.generate_field(self.game, self.current_player)
                            continue
                        indrow, indbutt = self.check_field_buttons(event)
                        if self.move is None:
                            self.move = Position(indrow, indbutt)
                            try:
                                self.game.execute_move(self.current_player, self.move)
                                self.update_sequence('Player ' + str(self.current_player) + ': shoot')
                                self.update_buttons(self.game, self.current_player)
                            except ValueError as e:
                                print(e)
                                self.move = None
                                continue
                        else:
                            self.shoot = Position(indrow, indbutt)
                            try:
                                self.game.execute_shot(self.current_player, self.shoot)
                                print('Successful move', self.move, self.shoot)
                                self.move = None
                                self.current_player = (self.current_player + 1) % self.num_players
                                if self.game.is_ended():
                                    print('disabled')
                                    self.board.enable()
                                    self.board.disable()
                                    self.update_sequence('game ended')
                                else:
                                    self.update_sequence('Player ' + str(self.current_player) + ': move shoot')
                            except ValueError as e:
                                print(e)
                                continue
                            self.update_buttons(self.game, self.current_player)

                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)

            pygame.display.update()
