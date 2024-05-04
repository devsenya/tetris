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
        # if self.cube[-1][1] < self.cup.height - 1:
        #     for x in range(len(self.cube)):
        #         point = list(self.cube[x])
        #         point[1] += 1
        #         self.cube[x] = tuple(point)
        #     self.cup.move_cube(self.cube)
        # else:
        #     self.cup.move_cube(self.cube, False)


        # движение вправо и влево
        if self.cube[-1][1] < self.cup.height - 1:
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
        self.width, self.height = cup_w, cup_h
        self.surface = serface
        self.cell_size = cell_size
        self.gridList = [[0] * self.width for x in range(self.height)]
        self.posX = (WINDOW_W - self.width * cell_size) // 2
        self.posY = WINDOW_H - self.height * cell_size
        # [print(x) for x in self.gridList]

    def clear(self):
        for line in range(len(self.gridList)):
            for col in range(len(self.gridList[line])):
                if self.gridList[line][col] == 1:
                    self.gridList[line][col] = 0

    def draw(self):
        # отрисовка вертикальных линий
        for numLine in range(self.width + 1):
            startPoint = self.posX + self.cell_size * numLine, self.posY
            endPoint = self.posX + self.cell_size * numLine, WINDOW_H

            pygame.draw.line(self.surface, GREY, startPoint, endPoint)
        # отрисовка горизонтальных линий
        for x in range(self.height + 1):
            pygame.draw.line(self.surface, GREY, (self.posX, self.posY + self.cell_size * x),
                             (self.posX + self.width * self.cell_size, self.posY + self.cell_size * x))
        # отрисовка фигур
        for line in range(len(self.gridList)):
            # print(f"начало линии {line}")
            for col in range(len(self.gridList[line])):
                rect = (self.posX + self.cell_size * col, self.posY + self.cell_size * line, 20, 20)
                # point2 = (self.posX + self.cell_size + self.cell_size * col, self.posY  + self.cell_size + self.cell_size * line)
                # print(point1, point2)
                if self.gridList[line][col] == 1:
                    pygame.draw.rect(self.surface, GREEN, rect)
                elif self.gridList[line][col] == 2:
                    pygame.draw.rect(self.surface, LIGHT_GREEN, rect)

    # скорее всего это должа делать игра
    def set_move_status(self, figura, is_moving=True):  # [(0,0),(1,0),(0,1),(1,1)]
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        status = 1 if is_moving else 2
        for cube in figura:
            self.gridList[cube[1]][cube[0]] = status
        [print(x) for x in self.gridList]

class Piece:
    def __init__(self, type, coords):
        self.type = type
        self.massBlocks = coords

    def move_right(self):
        for x in range(len(self.massBlocks)):
            point = list(self.massBlocks[x])
            point[0] += 1
            self.massBlocks[x] = tuple(point)

    def move_left(self):
        for x in range(len(self.massBlocks)):
            point = list(self.massBlocks[x])
            point[0] -= 1
            self.massBlocks[x] = tuple(point)

if __name__ == "__main__":
    game = Game()
    game.run()
