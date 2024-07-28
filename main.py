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


def randomPiece():
    num = random.randint(1,1)
    match num:
        case 1:
            return I_Type("i-type", 5, 0)
        case 2:
            return S_Type("z-type", 5, 0)


class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("TETRIS")
        self.clock = pygame.time.Clock()
        self.cup = Cup(20, 10, self.win, 20)
        self.piece = randomPiece()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.move_down()
                elif event.key == pygame.K_a:
                    self.move_left()
                elif event.key == pygame.K_d:
                    self.move_right()
                elif event.key == pygame.K_w:
                    self.check_rotate()

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
            self.move_down()

    def spawn_piece(self):
        for x in self.cup.gridList:
            if 1 in x:
                break
        else:
            self.piece = randomPiece()

    # скорее всего это должа делать игра
    def set_move_status(self, is_moving=True):  # [(0,0),(1,0),(0,1),(1,1)]
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        status = 1 if is_moving else 2
        for cube in self.piece.massBlocks:
            self.cup.gridList[cube[1]][cube[0]] = status
        # [print(x) for x in self.cup.gridList]

    def move_left(self):
        if self.check_left():
            self.cup.clear()
            # for x in range(len(self.piece.massBlocks)):
            #     point = list(self.piece.massBlocks[x])
            #     point[0] -= 1
            #     self.piece.massBlocks[x] = tuple(point)
            self.piece.set_XY(self.piece.X-1, self.piece.Y)
            self.set_move_status(self.piece.massBlocks)

    def move_right(self):
        if self.check_right():
            self.cup.clear()
            self.piece.set_XY(self.piece.X+1, self.piece.Y)
            self.set_move_status(self.piece.massBlocks)

    def check_left(self):
        for block in self.piece.massBlocks:
            if block[0] <= 0 or self.cup.gridList[block[1]][block[0] - 1] == 2:
                return False
        else:
            return True

    def check_right(self):
        for block in self.piece.massBlocks:
            if block[0] >= self.cup.width - 1 or self.cup.gridList[block[1]][block[0] + 1] == 2:
                return False
        else:
            return True

    def check_down(self):
        for block in self.piece.massBlocks:
            if block[1] >= self.cup.height - 1 or self.cup.gridList[block[1] + 1][block[0]] == 2:
                return False
        else:
            return True

    # TOD: подумать: что не так с условием - работает не совсем корректно
    def check_rotate(self):
        for block in self.piece.nextRotate:
            if not (0 <= block[0] < self.cup.width and self.cup.gridList[block[1]][block[0] + 1] != 2):
                return False
        else:
            self.piece.rotate()

    def move_down(self):
        global current_time, now
        now = time.time()
        self.check_down()
        if self.check_down():
            self.cup.clear()
            print(self.piece.massBlocks)
            self.piece.set_XY(self.piece.X, self.piece.Y + 1)
            self.set_move_status(self.piece.massBlocks)
            current_time = now
        else:
            self.set_move_status(False)
            self.piece.massBlocks.clear()

    def run(self):
        run = True

        while run:
            run = self.handle_events()
            self.move_piece()
            self.draw()
            self.spawn_piece()
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


class I_Type:
    def __init__(self, type, X, Y):
        self.X = X
        self.Y = Y
        self.type = type
        self.variationNum = 0
        self.variations = self.update()
        self.massBlocks = self.variations[self.variationNum]

    def set_XY(self, X, Y):
        self.X = X
        self.Y = Y
        self.update()

    def rotate(self):
        self.variationNum = (self.variationNum + 1) % len(self.variations)
        self.update()

    # свойство-геттер
    @property
    def nextRotate(self):
        return self.variations[(self.variationNum + 1) % len(self.variations)]

    def update(self):
        self.variations = [[(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X, self.Y + 2)],
                           [(self.X - 1, self.Y), (self.X, self.Y), (self.X + 1, self.Y), (self.X + 2, self.Y)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations

class O_Type:
    def __init__(self, type, X, Y):
        self.type = type
        self.massBlocks = [(X, Y), (X + 1, Y), (X, Y + 1), (X + 1, Y + 1)]



class S_Type:


    def __init__(self, type, X, Y):
        self.X = X
        self.Y = Y
        self.type = type
        self.variationNum = 0
        self.variations = self.update()
        self.massBlocks = self.variations[self.variationNum]

    def set_XY(self, X, Y):
        self.X = X
        self.Y = Y
        self.update()

    def rotate(self):
        self.variationNum = (self.variationNum + 1) % len(self.variations)
        self.update()

    def update(self):
        self.variations = [[(self.X - 1, self.Y + 1), (self.X, self.Y + 1), (self.X, self.Y), (self.X + 1, self.Y)],
                           [(self.X - 1, self.Y - 1), (self.X - 1, self.Y), (self.X, self.Y), (self.X, self.Y + 1)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations



class Z_Type:
    def __init__(self, type, X, Y):
        self.type = type
        self.massBlocks = [(X - 1, Y), (X, Y), (X, Y - 1), (X + 1, Y - 1)]


class L_Type:
    def __init__(self, type, X, Y):
        self.type = type
        self.massBlocks = [(X, Y - 1), (X, Y), (X, Y + 1), (X + 1, Y + 1)]


class J_Type:
    def __init__(self, type, X, Y):
        self.type = type
        self.massBlocks = [(X, Y - 1), (X, Y), (X, Y + 1), (X - 1, Y + 1)]


class T_Type:
    def __init__(self, type, X, Y):
        self.type = type
        self.massBlocks = [(X - 1, Y), (X, Y), (X + 1, Y), (X, Y + 1)]


if __name__ == "__main__":
    game = Game()
    game.run()
