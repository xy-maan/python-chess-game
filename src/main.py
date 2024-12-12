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
        dragger = self.game.dragger
        board = self.game.board

        while running:

            game.show_background(screen)
            game.show_pieces(screen)

            for event in pygame.event.get():

                # Events that help dragging the pieces around the board.

                # click event
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # event.pos holds the position where we click.
                    dragger.update_mouse(event.pos)

                    # determine the indices of the clicked square.
                    clicked_row = dragger.mouseY // SQUARE_SIZE
                    clicked_col = dragger.mouseX // SQUARE_SIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        dragger.save_init_pos(event.pos)
                        dragger.drag_on(piece)

                # mouse motion event
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        # to void the illusion of having another piece behind the piece that is being dragged.
                        # game.show_background(screen)
                        # game.show_pieces(screen)

                        dragger.update_blit(screen)

                # release event
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.drag_off()

                    # to fix the "must click again to show the piece after release" error.
                    game.show_pieces(screen)

                if event.type == pygame.QUIT:
                    running = False

                pygame.display.update()  # update the screen with the latest made events

        pygame.quit()  # shutdown all initlaized modules
        sys.exit()  # close the game window


main = Main()
main.main_loop()
