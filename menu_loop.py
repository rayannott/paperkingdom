import pygame
import pygame_gui

from gui_utils import GUI


class Menu:
    def __init__(self, width, height, window_surface):
        self.width = width
        self.height = height
        self.game_screen_left_margin = 200
        self.game_screen_right_margin = 200
        self.game_screen_button_margin = 10

        self.window_surface = window_surface
        self.manager = pygame_gui.UIManager((width, height), 'menu_theme.json')
        self.clock = pygame.time.Clock()

        button_margin = 0
        self.play_button = pygame_gui.elements.ui_button.UIButton(
            relative_rect=pygame.Rect(button_margin, button_margin,
                                      width - 2 * button_margin,
                                      height - 2 * button_margin),
            text='Play',
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
                            gui.game_loop()
                self.manager.process_events(event)
            self.manager.update(time_delta)
            self.manager.draw_ui(self.window_surface)

            pygame.display.update()
