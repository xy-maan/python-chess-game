"""
This file contains the Game class

which will be resposilbe for all rendering methods for the game
including grpahics and sounds
"""

import pygame
from const import *

class Game:
	def __init__(self):
		pass

	# show methods

	def show_background(self, surface):

		# draw the board
		for row in range(ROWS):
			for col in range(COLS):
				if (row + col) % 2 == 0:
					color = (234, 235, 200) # light green
				else:
					color = (119, 154, 88) # dark green

				rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) # (x, y, width, height)

				pygame.draw.rect(surface, color, rect)