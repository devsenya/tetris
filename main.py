import pygame
import random, time, sys
from pygame.locals import *

fps = 25
WINDOW_W, WINDOW_H = 600, 500
GREY = (180, 180, 180)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 155, 0)
FPS = 120
fall_time = 1  # Интервал времени между падениями фигурки (в секундах)
current_time = 0
now = time.time()


class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("TETRIS")
        self.clock = pygame.time.Clock()
        self.cup = Cup(20, 10, self.win, 20)
        self.piece = Line("i-type", [(5, 0), (5, 1), (5, 2), (5, 3)])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.piece.move_down(self.cup)
                    self.push_figure_in_cup()
                elif event.key == pygame.K_a:
                    self.piece.move_left(self.cup)
                    self.push_figure_in_cup()
                elif event.key == pygame.K_d:
                    self.piece.move_right(self.cup)
                    self.push_figure_in_cup()

        return True

    def draw(self):
        # self.win.blit(self.background_image, self.background_image.get_rect())
        self.win.fill(WHITE)
        self.cup.draw()
        pygame.display.flip()

    def move_piece(self):
        global current_time, now
        now = time.time()
        # подение куба
        # должно будет работать только если фигура еще падает
        if now - current_time >= fall_time:
            self.piece.move_down(self.cup)
            self.push_figure_in_cup()

    # скорее всего это должа делать игра
    def push_figure_in_cup(self):
        status = 1 if self.piece.is_moving else 2
        for cube in self.piece.massBlocks:
            self.cup.gridList[cube[1]][cube[0]] = status

    def run(self):
        run = True

        while run:
            run = self.handle_events()
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
            for col in range(len(self.gridList[line])):
                rect = (self.posX + self.cell_size * col, self.posY + self.cell_size * line, 20, 20)

                if self.gridList[line][col] == 1:
                    pygame.draw.rect(self.surface, GREEN, rect)
                elif self.gridList[line][col] == 2:
                    pygame.draw.rect(self.surface, LIGHT_GREEN, rect)



class Line:
    def __init__(self, type, coords):
        self.type = type
        self.massBlocks = coords
        self.is_moving = True

    def move_left(self, cup):
        min_x = min(self.massBlocks, key=lambda block: block[0])[0]
        if min_x > 0 and self.is_moving:
            cup.clear()
            for x in range(len(self.massBlocks)):
                point = list(self.massBlocks[x])
                point[0] -= 1
                self.massBlocks[x] = tuple(point)

    def move_right(self, cup):
        max_x = max(self.massBlocks, key=lambda block: block[0])[0]
        if max_x < cup.width-1 and self.is_moving:
            cup.clear()
            for x in range(len(self.massBlocks)):
                point = list(self.massBlocks[x])
                point[0] += 1
                self.massBlocks[x] = tuple(point)

    def move_down(self, cup):
        global current_time, now
        now = time.time()
        max_y = max(self.massBlocks, key=lambda X: X[1])[1]
        if max_y < cup.height - 1 and self.is_moving:
            cup.clear()
            for x in range(len(self.massBlocks)):
                point = list(self.massBlocks[x])
                point[1] += 1
                self.massBlocks[x] = tuple(point)
            current_time = now
        else:
            self.is_moving = False

if __name__ == "__main__":
    game = Game()
    game.run()
