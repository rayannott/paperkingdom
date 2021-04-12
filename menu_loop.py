import pygame
import pygame_gui

from gui_utils import GUI


class Menu:
    def __init__(self, width, height, window_surface: pygame.Surface):
        self.width = width
        self.height = height
        self.game_screen_left_margin = 200
        self.game_screen_right_margin = 200
        self.game_screen_button_margin = 10

        self.window_surface = window_surface
        self.black_screen = pygame.Surface((0, 0))
        self.black_screen.fill(pygame.Color(255, 255, 255))
        self.manager = pygame_gui.UIManager((width, height), 'menu_theme.json')
        self.clock = pygame.time.Clock()

        num_buttons = 4
        button_margin = 30

        top_margin = 100
        bottom_margin = 100
        left_margin = 200
        right_margin = 200

        butt_size_x = width - left_margin - right_margin
        butt_size_y = (height - top_margin - bottom_margin - (num_buttons - 1) * button_margin) / num_buttons
        self.play_button = pygame_gui.elements.ui_button.UIButton(
            relative_rect=pygame.Rect(left_margin,
                                      top_margin + (butt_size_y + button_margin) * 0,
                                      butt_size_x,
                                      butt_size_y),
            text='Play',
            manager=self.manager,
            object_id='butt'
        )
        self.saved_games_button = pygame_gui.elements.ui_button.UIButton(
            relative_rect=pygame.Rect(left_margin,
                                      top_margin + (butt_size_y + button_margin) * 1,
                                      butt_size_x,
                                      butt_size_y),
            text='Saved games',
            manager=self.manager,
            object_id='butt'
        )
        self.options_button = pygame_gui.elements.ui_button.UIButton(
            relative_rect=pygame.Rect(left_margin,
                                      top_margin + (butt_size_y + button_margin) * 2,
                                      butt_size_x,
                                      butt_size_y),
            text='Options',
            manager=self.manager,
            object_id='butt'
        )
        self.exit_button = pygame_gui.elements.ui_button.UIButton(
            relative_rect=pygame.Rect(left_margin,
                                      top_margin + (butt_size_y + button_margin) * 3,
                                      butt_size_x,
                                      butt_size_y),
            text='Exit',
            manager=self.manager,
            object_id='butt'
        )

    def menu_loop(self):
        is_running = True
        while is_running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.play_button:
                            gui = GUI(
                                self.width,
                                self.height,
                                self.game_screen_left_margin,
                                self.game_screen_right_margin,
                                self.game_screen_button_margin,
                                self.window_surface
                            )
                            is_running = gui.game_loop()
                            pygame.draw.rect(self.window_surface, (0, 0, 0),
                                             (0, 0, self.width, self.height))
                        elif event.ui_element == self.exit_button:
                            is_running = False

                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)
            self.window_surface.blit(self.black_screen, (0, 0))
            pygame.display.update()
