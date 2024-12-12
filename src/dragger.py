import pygame
from const import *


class Dragger:

    def __init__(self):

        # to know which piece are we dragging
        self.piece = None

        # to know if we are in a dragging state or not.
        self.dragging = False

        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos  # pos = (x, y)

    def drag(self, surface):

        piece = self.piece

        img = pygame.image.load(piece.img_path)
        center_coordinates = (self.mouseX, self.mouseY)

        # align the piece to the center of the square
        piece.pos = img.get_rect(center=center_coordinates)

        # show the piece.
        surface.blit(img, piece.pos)

    def save_init_pos(self, pos):
        self.initial_row = pos[1] // SQUARE_SIZE
        self.initial_col = pos[0] // SQUARE_SIZE

    def drag_on(self, piece):
        self.piece = piece
        self.dragging = True

    def drag_off(self):
        self.piece = None
        self.dragging = False
