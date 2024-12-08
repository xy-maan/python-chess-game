import pygame  # for creating game console
import sys  # for quitting the game

from const import *


class Main:
    def __init__(self):
        pygame.init()  # initialize required modules.

        self.game_window = pygame.display.set_mode((WIDTH, HEIGHT))  # start a game console with the passed width and height
        pygame.display.set_caption("Chess")  # window title bar

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # shutdown all the modules that were initalized earlier
                    sys.exit()  # close the game window

                pygame.display.update()  # update the screen with any made event


main = Main()
main.main_loop()
