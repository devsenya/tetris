import pygame
import random, time, sys
from pygame.locals import *

fps = 25
WINDOW_W, WINDOW_H = 600, 500
GREY = (180, 180, 180)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 155, 0)
FPS = 1


class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("TETRIS")
        self.clock = pygame.time.Clock()
        self.cup = Cup(20, 10, self.win, 20)
        self.cube = [(4, 0), (5, 0), (4, 1), (5, 1)]
        # self.cube = [(0, 0), (1, 0), (0, 1), (1, 1)]
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.move_piece()
        return True

    def draw(self):
        # self.win.blit(self.background_image, self.background_image.get_rect())
        self.win.fill(WHITE)
        self.cup.draw()
        pygame.display.flip()

    def move_piece(self):
        # подение куба
        # должно будет работать только если фигура еще падает
        # if self.cube[-1][1] < self.cup.cup_h - 1:
        #     for x in range(len(self.cube)):
        #         point = list(self.cube[x])
        #         point[1] += 1
        #         self.cube[x] = tuple(point)
        #     self.cup.move_cube(self.cube)
        # else:
        #     self.cup.move_cube(self.cube, False)


        # движение вправо и влево
        if self.cube[-1][1] < self.cup.cup_h - 1:
            for x in range(len(self.cube)):
                point = list(self.cube[x])
                if point[0] <= 0:
                    break
            else:
                for x in range(len(self.cube)):
                    point = list(self.cube[x])
                    point[0] -= 1
                    self.cube[x] = tuple(point)
            self.cup.set_move_status(self.cube)
        else:
            self.cup.set_move_status(self.cube, False)




    def run(self):
        run = True

        while run:
            run = self.handle_events()
            self.cup.clear()
            self.move_piece()
            self.draw()
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
        # [print(x) for x in self.grid]

    def clear(self):
        for line in range(len(self.grid)):
            for col in range(len(self.grid[line])):
                if self.grid[line][col] == 1:
                    self.grid[line][col] = 0

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
            # print(f"начало линии {line}")
            for col in range(len(self.grid[line])):
                rect = (self.posX + self.cell_size * col, self.posY + self.cell_size * line, 20, 20)
                # point2 = (self.posX + self.cell_size + self.cell_size * col, self.posY  + self.cell_size + self.cell_size * line)
                # print(point1, point2)
                if self.grid[line][col] == 1:
                    pygame.draw.rect(self.surface, GREEN, rect)
                elif self.grid[line][col] == 2:
                    pygame.draw.rect(self.surface, LIGHT_GREEN, rect)

    def set_move_status(self, addr_cube, is_moving=True):  # [(0,0),(1,0),(0,1),(1,1)]
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        status = 1 if is_moving else 2
        for cube in addr_cube:
            self.grid[cube[1]][cube[0]] = status
        [print(x) for x in self.grid]



if __name__ == "__main__":
    game = Game()
    game.run()
