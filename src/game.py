"""
This file contains the Game class

which will be resposilbe for all rendering methods for the game
including grpahics and sounds
"""

import pygame
from const import *
from board import Board
from dragger import Dragger

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()

    # show methods

    def show_background(self, surface):

        # draw the board
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (199, 194, 172)
                else:
                    color = (91, 87, 83)

                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) # (x, y, width, height)

                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):

        for row in range(ROWS):
            for col in range(COLS):
                
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # show all pieces except the ones that are being dragged.
                    if piece is not self.dragger.piece:
                        img = pygame.image.load(piece.img_path)
                        center_coordinates = (col * SQUARE_SIZE) + (SQUARE_SIZE // 2), row * SQUARE_SIZE + (SQUARE_SIZE // 2)

                        # align the piece to the center of the square
                        piece.pos = img.get_rect(center=center_coordinates)

                        # show the piece.
                        surface.blit(img, piece.pos)

    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            # loop on all valid moves that were added to the moves array.
            for move in piece.moves:
                color = "#C86464" if (move.final.row + move.final.col) % 2 == 0 else "#C84646"

                rect = (move.final.col * SQUARE_SIZE, move.final.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

                pygame.draw.rect(surface, color, rect)