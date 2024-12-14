import pygame

class Sound:

    def __init__(self, path):

        # save the sound file path.
        self.path = path

        # make a pygame sound so that we can play it later.
        self.sound = pygame.mixer.Sound(path)

    # play the sound
    def play(self):
        pygame.mixer.Sound.play(self.sound)
