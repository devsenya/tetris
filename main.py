import pygame
import random, time, sys
from pygame.locals import *

fps = 25
WINDOW_W, WINDOW_H = 600, 500
GREY = (180, 180, 180)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
FPS = 1


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
        self.cup.draw()
        pygame.display.flip()

    def run(self):
        run = True
        while run:
            run = self.handle_events()

            self.draw()
            self.cup.push_cube([(0,0),(1,0),(0,1),(1,1)])
            self.clock.tick(FPS)
        pygame.quit()
        quit()


class Cup:
    def __init__(self, cup_h, cup_w, serface, cell_size):
        self.cup_h, self.cup_w = cup_h, cup_w
        self.surface = serface
        self.cell_size = cell_size
        self.grid = [[0] * self.cup_w for x in range(self.cup_h)]
        self.posX = (WINDOW_W - cup_w * cell_size) // 2
        self.posY = WINDOW_H - cup_h * cell_size
        [print(x) for x in self.grid]

    def draw(self):
        # отрисовка вертикальных линий
        for x in range(self.cup_w + 1):
            pygame.draw.line(self.surface, GREY, (self.posX + self.cell_size * x, self.posY),
                             (self.posX + self.cell_size * x, WINDOW_H))
        # отрисовка горизонтальных линий
        for x in range(self.cup_h + 1):
            pygame.draw.line(self.surface, GREY, (self.posX, self.posY + self.cell_size * x),
                             (self.posX + self.cup_w * self.cell_size, self.posY + self.cell_size * x))
        # отрисовка фигур
        for line in range(len(self.grid)):
            print(f"начало линии {line}")
            for col in range(len(self.grid[line])):
                point1 = (self.posX + self.cell_size * col, self.posY + self.cell_size * line)
                point2 = (self.posX + self.cell_size + self.cell_size * col, self.posY  + self.cell_size + self.cell_size * line)
                print(point1, point2)
                if self.grid[line][col] == 1:
                    pygame.draw.rect(self.surface, GREEN, (point1, point2))



    def push_cube(self, addr_cube): #[(0,0),(1,0),(0,1),(1,1)]
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        for cube in addr_cube:
            self.grid[cube[1]][cube[0]] = 1
        [print(x) for x in self.grid]


if __name__ == "__main__":
    game = Game()
    game.run()
