import pygame
import os

from sound import Sound
from theme import Theme


class Config:

    def __init__(self):

        # an array to hold the themes we can change between.
        self.themes = []

        # add our basic 4 themes.
        self._add_themes()

        # index of the current selected theme
        self.idx = 0
        
        # currenttly selected theme
        self.theme = self.themes[self.idx]

        # font that will be used to display coordinates on the board (letters and numbers)
        self.font = pygame.font.SysFont("monospace", 18, bold=True)

        # move sound
        self.move_sound = Sound(os.path.join("../assets/sounds/move.mp3"))

        # capture sound
        self.capture_sound = Sound(os.path.join("../assets/sounds/capture.mp3"))

        # promotion sound
        self.promotion_sound = Sound(os.path.join("../assets/sounds/promote.mp3"))


    def change_theme(self):

        # go to the next theme
        self.idx += 1

        # so that it doesn't exceed the array limit.
        self.idx %= len(self.themes)

        # set the new theme.
        self.theme = self.themes[self.idx]


    # adding the theme colors
    def _add_themes(self):
        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), "#C86464", "#C84646")
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), "#C86464", "#C84646")
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), "#C86464", "#C84646")
        gray = Theme((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128), "#C86464", "#C84646")

        self.themes = [green, brown, blue, gray]
