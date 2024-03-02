import pygame
import random, time, sys
from pygame.locals import *

fps = 25
window_w, window_h = 600, 500
block, cup_h, cup_w = 20, 20, 10





FPS = 25
class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((window_w, window_h))
        pygame.display.set_caption("TETRIS")
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def draw(self):
        # self.win.blit(self.background_image, self.background_image.get_rect())
        pygame.display.update()

    def run(self):
        run = True
        while run:
            run = self.handle_events()

            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        quit()

class Cup:
    def __init__(self):
        cupMass = []
        for i in range(cup_w):
            cupMass.append([empty] * cup_h)
        return cup

if __name__ == "__main__":
    game = Game()
    game.run()