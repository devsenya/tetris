import pygame

import random, time, sys, abc
from pygame.locals import *

fps = 25
WINDOW_W, WINDOW_H = 600, 500
GREY = (180, 180, 180)
WHITE = (255, 255, 255)
FPS = 120
fall_time = 1  # Интервал времени между падениями фигурки (в секундах)
current_time = 0
now = time.time()


def randomPiece():
    num = random.randint(1, 7)
    match num:
        case 1:
            return I_Type(5, 0)
        case 2:
            return O_Type(5, 0)
        case 3:
            return S_Type(5, 0)
        case 4:
            return Z_Type(5, 0)
        case 5:
            return L_Type(5, 0)
        case 6:
            return J_Type(5, 0)
        case 7:
            return T_Type(5, 0)


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
                elif event.key == pygame.K_SPACE:
                    [print(x) for x in self.cup.gridList]

        return True

    def draw(self):
        # self.win.blit(self.background_image, self.background_image.get_rect())
        self.win.fill(WHITE)
        self.cup.draw(self)
        pygame.display.flip()

    def move_piece(self):
        global current_time, now
        now = time.time()
        # подение куба
        # должно будет работать только если фигура еще падает
        if now - current_time >= fall_time:
            self.move_down()

    def spawn_piece(self):
        for line in self.cup.gridList:
            for x in line:
                if 1 <= x <= 7:
                    return
        else:
            self.piece = randomPiece()

    # скорее всего это должа делать игра
    def set_move_status(self, is_moving=True):  # [(0,0),(1,0),(0,1),(1,1)]
        status = self.piece.id if is_moving else self.piece.id * 10
        for cube in self.piece.massBlocks:
            self.cup.gridList[cube[1]][cube[0]] = status

    def move_left(self):
        if self.check_left():
            self.cup.clear()
            self.piece.set_XY(self.piece.X - 1, self.piece.Y)
            self.set_move_status(self.piece.massBlocks)

    def move_right(self):
        if self.check_right():
            self.cup.clear()
            self.piece.set_XY(self.piece.X + 1, self.piece.Y)
            self.set_move_status(self.piece.massBlocks)

    def check_left(self):
        for block in self.piece.massBlocks:
            if block[0] <= 0 or self.cup.gridList[block[1]][block[0] - 1] > 10:
                return False
        else:
            return True

    def check_right(self):
        for block in self.piece.massBlocks:
            if block[0] >= self.cup.width - 1 or self.cup.gridList[block[1]][block[0] + 1] > 10:
                return False
        else:
            return True

    def check_down(self):
        for block in self.piece.massBlocks:
            if block[1] >= self.cup.height - 1 or self.cup.gridList[block[1] + 1][block[0]] > 10:
                return False
        else:
            return True

    def check_rotate(self):
        for block in self.piece.nextRotate:
            if not (0 <= block[0] < self.cup.width and block[1] < self.cup.height and self.cup.gridList[block[1]][
                block[0]] < 10):
                return False
        else:
            self.piece.rotate()
            self.cup.clear()
            self.piece.set_XY(self.piece.X, self.piece.Y)
            self.set_move_status(self.piece.massBlocks)

    def move_down(self):
        global current_time, now
        now = time.time()
        if self.check_down():
            self.cup.clear()
            # print(self.piece.massBlocks)
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
        self.colors = [(0, 255, 0), (135, 206, 250), (144, 238, 144), (255, 182, 193), (255, 165, 0), (221, 160, 221),
                       (255, 255, 102), (175, 238, 238)]

    def clear(self):
        for line in range(len(self.gridList)):
            for col in range(len(self.gridList[line])):
                if self.gridList[line][col] in [1, 2, 3, 4, 5, 6, 7, 8]:
                    self.gridList[line][col] = 0

    def draw(self, colors):
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

                match self.gridList[line][col]:
                    case 1:
                        pygame.draw.rect(self.surface, self.colors[0], rect)
                    case 2:
                        pygame.draw.rect(self.surface, self.colors[1], rect)
                    case 3:
                        pygame.draw.rect(self.surface, self.colors[2], rect)
                    case 4:
                        pygame.draw.rect(self.surface, self.colors[3], rect)
                    case 5:
                        pygame.draw.rect(self.surface, self.colors[4], rect)
                    case 6:
                        pygame.draw.rect(self.surface, self.colors[5], rect)
                    case 7:
                        pygame.draw.rect(self.surface, self.colors[6], rect)
                    case 8:
                        pygame.draw.rect(self.surface, self.colors[7], rect)


class Shape(abc.ABC):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
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

    @abc.abstractmethod
    def update(self):
        pass


class I_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 2
        # self.moving_color = (135, 206, 250)  # Светлый цвет
        # self.stopped_color = (70, 130, 180)  # Тёмный цвет

    def update(self):
        self.variations = [[(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X, self.Y + 2)],
                           [(self.X - 1, self.Y), (self.X, self.Y), (self.X + 1, self.Y), (self.X + 2, self.Y)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations


class O_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 3
        # self.moving_color = (144, 238, 144)  # Светлый цвет
        # self.stopped_color = (34, 139, 34)  # Тёмный цвет

    def update(self):
        self.variations = [[(self.X, self.Y), (self.X + 1, self.Y), (self.X, self.Y + 1), (self.X + 1, self.Y + 1)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations


class S_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 4
        # self.moving_color = (255, 182, 193)  # Светлый цвет
        # self.stopped_color = (220, 20, 60)  # Тёмный цвет

    def update(self):
        self.variations = [[(self.X - 1, self.Y + 1), (self.X, self.Y + 1), (self.X, self.Y), (self.X + 1, self.Y)],
                           [(self.X - 1, self.Y - 1), (self.X - 1, self.Y), (self.X, self.Y), (self.X, self.Y + 1)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations


class Z_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 5
        # self.moving_color = (255, 165, 0)  # Светлый цвет
        # self.stopped_color = (255, 140, 0)  # Тёмный цвет

    def update(self):
        self.variations = [[(self.X - 1, self.Y - 1), (self.X, self.Y - 1), (self.X, self.Y), (self.X + 1, self.Y)],
                           [(self.X + 1, self.Y - 1), (self.X + 1, self.Y), (self.X, self.Y), (self.X, self.Y + 1)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations


class L_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 6
        # self.moving_color = (221, 160, 221)  # Светлый цвет
        # self.stopped_color = (138, 43, 226)  # Тёмный цвет

    def update(self):
        self.variations = [[(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X + 1, self.Y + 1)],
                           [(self.X + 1, self.Y), (self.X, self.Y), (self.X - 1, self.Y), (self.X - 1, self.Y + 1)],
                           [(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X - 1, self.Y - 1)],
                           [(self.X + 1, self.Y), (self.X, self.Y), (self.X - 1, self.Y), (self.X + 1, self.Y - 1)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations


class J_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 7
        # self.moving_color = (255, 255, 102)  # Светлый цвет
        # self.stopped_color = (255, 215, 0)  # Тёмный цвет

    def update(self):
        self.variations = [[(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X - 1, self.Y + 1)],
                           [(self.X + 1, self.Y), (self.X, self.Y), (self.X - 1, self.Y), (self.X - 1, self.Y - 1)],
                           [(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X + 1, self.Y - 1)],
                           [(self.X + 1, self.Y), (self.X, self.Y), (self.X - 1, self.Y), (self.X + 1, self.Y + 1)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations


class T_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 8
        # self.moving_color = (175, 238, 238)  # Светлый цвет
        # self.stopped_color = (72, 209, 204)  # Тёмный цвет

    def update(self):
        self.variations = [[(self.X - 1, self.Y), (self.X, self.Y), (self.X + 1, self.Y), (self.X, self.Y + 1)],
                           [(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X - 1, self.Y)],
                           [(self.X - 1, self.Y), (self.X, self.Y), (self.X + 1, self.Y), (self.X, self.Y - 1)],
                           [(self.X, self.Y - 1), (self.X, self.Y), (self.X, self.Y + 1), (self.X + 1, self.Y)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations


if __name__ == "__main__":
    game = Game()
    game.run()
