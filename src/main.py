import pygame  # for creating game console
import sys  # for quitting the game

from const import *
from game import Game
from square import Square
from move import Move
from piece import Pawn


class Main:
    def __init__(self):
        pygame.init()  # initialize required modules.

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # start a game console with the passed width and height
        pygame.display.set_caption("Chess")  # window title bar

        self.game = Game()

    def main_loop(self):

        # save long names in variables for shorter code
        running = True
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board

        while running:

            game.show_background(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

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

                        # is it the player's turn ?
                        if game.player == piece.color:
                            board.calc_moves(clicked_row, clicked_col, piece)

                            dragger.save_init_pos(event.pos)

                            dragger.drag_on(piece)

                            # game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            # game.show_pieces(screen)

                # mouse motion event
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQUARE_SIZE
                    motion_col = event.pos[0] // SQUARE_SIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        # to avoid the illusion of having another piece behind the piece that is being dragged.
                        # game.show_background(screen)

                        game.show_last_move(screen)
                        game.show_moves(screen)
                        # game.show_pieces(screen)
                        game.show_hover(screen)

                        dragger.drag(screen)

                # release event
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:

                        # update the pos to the place we released the piece on.
                        dragger.update_mouse(event.pos)

                        # get the new coordinates.
                        release_row = dragger.mouseY // SQUARE_SIZE
                        release_col = dragger.mouseX // SQUARE_SIZE

                        # create initial and final squares to move on.
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(release_row, release_col)

                        move = Move(initial, final)

                        # check if the square we released the piece on is actually a valid square.
                        if board.valid_move(dragger.piece, move):

                            # if the square we are moving into has a piece, then we play the capture sound, otherwise move sound.
                            capture = board.squares[release_row][release_col].has_piece()

                            board.move(dragger.piece, move)

                            # promition sound logic, by xy-man.
                            if board.promoted(piece, release_row):
                                game.promote_sound()
                            # castling sound logic also by xy-man.
                            elif board.castled(piece, initial, final):
                                game.castle_sound()
                            else:
                                # play the sound of the move
                                game.move_sound(capture)

                            # change the turn for other player.
                            game.change_player()

                            game.show_background(screen)
                            # game.show_moves(screen)

                            game.show_last_move(screen)

                            # game.show_pieces(screen)

                    dragger.drag_off()

                    # to fix the "must click again to show the piece after release" error.
                    game.show_pieces(screen)

                # key press
                elif event.type == pygame.KEYDOWN:

                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # reset the game
                    if event.key == pygame.K_r:
                        game.reset()

                        # since we restarted the game, we need to refresh the values.
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                elif event.type == pygame.QUIT:
                    running = False

                pygame.display.update()  # update the screen with the latest made events

        pygame.quit()  # shutdown all initlaized modules
        sys.exit()  # close the game window


main = Main()
main.main_loop()
