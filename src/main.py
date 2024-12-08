import pygame  # for creating game console
import sys  # for quitting the game

from const import *
from game import Game


class Main:
    def __init__(self):
        pygame.init()  # initialize required modules.

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # start a game console with the passed width and height
        pygame.display.set_caption("Chess")  # window title bar

        self.game = Game()

    def main_loop(self):

        running = True
        game = self.game
        screen = self.screen

        while running:

            game.show_background(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                pygame.display.update()  # update the screen with the latest made events

        pygame.quit() # shutdown all initlaized modules 
        sys.exit() # close the game window


main = Main()
main.main_loop()
