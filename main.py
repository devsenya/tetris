import pygame
import random, time, sys
from pygame.locals import *

fps = 25
WINDOW_W, WINDOW_H = 600, 500
GREY = (180, 180, 180)
WHITE = (255, 255, 255)
FPS = 25


class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("TETRIS")
        self.clock = pygame.time.Clock()
        self.cup = Cup(20, 10, self.win, 20)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def draw(self):
        # self.win.blit(self.background_image, self.background_image.get_rect())
        self.win.fill(WHITE)
        self.cup.draw_grid()
        pygame.display.flip()

    def run(self):
        run = True
        while run:
            run = self.handle_events()

            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        quit()


class Cup:
    def __init__(self, cup_h, cup_w, serface, cell_size):
        self.cup_h, self.cup_w = cup_h, cup_w
        self.serface = serface
        self.cell_size = cell_size
        self.grid = []
        self.posX = (WINDOW_W - cup_w * cell_size) // 2
        self.posY = WINDOW_H - cup_h * cell_size
        for i in range(cup_h):
            self.grid.append([0] * cup_w)

    def draw_grid(self):
        for x in range(self.cup_w + 1):
            pygame.draw.line(self.serface, GREY, (self.posX + self.cell_size * x, self.posY),
                             (self.posX + self.cell_size * x, WINDOW_H))
        for x in range(self.cup_h + 1):
            pygame.draw.line(self.serface, GREY, (self.posX , self.posY + self.cell_size * x),
                             (self.posX + self.cup_w * self.cell_size, self.posY + self.cell_size * x))


if __name__ == "__main__":
    game = Game()
    game.run()
