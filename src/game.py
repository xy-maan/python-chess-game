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
        self.player = "white"
        self.hovered_square = None
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

                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)  # (x, y, width, height)

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

    def show_last_move(self, surface):
        if self.board.last_move:

            # save the initial and final squares.
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                color = (244, 247, 116) if (pos.row + pos.col) % 2 == 0 else (172, 196, 51)

                rect = (pos.col * SQUARE_SIZE, pos.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

                pygame.draw.rect(surface, color, rect)

    def set_hover(self, row, col):
        self.hovered_square = self.board.squares[row][col]

    def show_hover(self, surface):
        if self.hovered_square:
            color = (180, 180, 180)

            rect = (self.hovered_square.col * SQUARE_SIZE, self.hovered_square.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

            pygame.draw.rect(surface, color, rect, width=3)

    def change_player(self):
        self.player = "white" if self.player == "black" else "black"
