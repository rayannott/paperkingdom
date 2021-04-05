import pygame
import pygame_gui

from gui_utils import GUI
from menu_loop import Menu

from move import Move

WIDTH = 1000
HEIGHT = 600
LMARGIN = 200
RMARGIN = 200
BMARGIN = 10
assert WIDTH > LMARGIN + RMARGIN


def game_loop():
    pygame.init()
    pygame.display.set_caption('Paper Kingdom')
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    menu = Menu(WIDTH, HEIGHT, window)
    menu.menu_loop()
    # gui_game = GUI(WIDTH, HEIGHT, LMARGIN, RMARGIN, BMARGIN, window)
    # gui_game.game_loop()


if __name__ == '__main__':
    game_loop()
