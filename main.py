import pygame

import random, time, sys, abc
from pygame.locals import *

fps = 25
WINDOW_W, WINDOW_H = 600, 500
GREY = (180, 180, 180)
WHITE = (255, 255, 255)
FPS = 120
fall_time = 0.5  # Интервал времени между падениями фигурки (в секундах)
current_time = 0
now = time.time()
pygame.font.init()
LIVES_FONT = pygame.font.SysFont("comicsans", 40)


def drawRect(surface, color, rect):
    pygame.draw.rect(surface, (0, 0, 0), rect)
    pygame.draw.rect(surface, color, (rect[0] + 1, rect[1] + 1, rect[2] - 3, rect[3] - 3))


def randomPiece():
    num = random.randint(1, 7)
    match num:
        case 1:
            return I_Type(5, 1)
        case 2:
            return O_Type(4, 0)
        case 3:
            return S_Type(5, 0)
        case 4:
            return Z_Type(5, 1)
        case 5:
            return L_Type(5, 1)
        case 6:
            return J_Type(5, 1)
        case 7:
            return T_Type(5, 0)


class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("TETRIS")
        self.clock = pygame.time.Clock()
        self.cup = Cup(20, 10, self.win, 20)
        self.spawn_piece()
        self.background_image = pygame.image.load("IM1.JPG")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.drop_down()
                elif event.key == pygame.K_a:
                    self.move_left()
                elif event.key == pygame.K_d:
                    self.move_right()
                elif event.key == pygame.K_w:
                    self.check_rotate()
                elif event.key == pygame.K_SPACE:
                    pass

        return True

    def draw(self):
        # self.win.blit(self.background_image, self.background_image.get_rect())

        # f1 = pygame.font.Font(None, 36)
        # text1 = f1.render('Hello Привет', 1, (180, 0, 0))
        # self.win.blit(text1, (10, 50))
        self.win.fill(WHITE)
        text = LIVES_FONT.render("11", 1, "black")
        self.win.blit(text, (0, 0))
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
        global now, current_time
        for line in self.cup.gridList:
            for x in line:
                if 1 <= x <= 7:
                    return
        else:
            print("заспавнили")
            self.piece = randomPiece()
            self.piece.set_XY(self.piece.X, self.piece.Y)
            self.set_move_status()
            now = time.time()
            current_time = now

    # скорее всего это должа делать игра
    def set_move_status(self, is_moving=True):  # [(0,0),(1,0),(0,1),(1,1)]
        status = self.piece.id if is_moving else self.piece.id * 10
        for cube in self.piece.massBlocks:
            try:
                self.cup.gridList[cube[1]][cube[0]] = status
            except:
                print(cube[1])
        if status >= 10:
            # TODO: Вынести в отдельную функцию/метод
            self.cup.delete_lines()

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
            if block[0] <= 0 or self.cup.gridList[block[1]][block[0] - 1] >= 10:
                return False
        else:
            return True

    def check_right(self):
        for block in self.piece.massBlocks:
            if block[0] >= self.cup.width - 1 or self.cup.gridList[block[1]][block[0] + 1] >= 10:
                return False
        else:
            return True

    def check_down(self):
        for block in self.piece.massBlocks:
            if block[1] + 1 >= self.cup.height or self.cup.gridList[block[1] + 1][block[0]] >= 10:
                return False
        else:
            return True

    def drop_down(self):
        while self.check_down():
            self.move_down()
        self.set_move_status(False)
        self.spawn_piece()

    def check_rotate(self):
        for block in self.piece.nextRotate:
            if not (0 <= block[0] < self.cup.width and 0 <= block[1] < self.cup.height and self.cup.gridList[block[1]][
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
            self.piece.set_XY(self.piece.X, self.piece.Y + 1)
            self.set_move_status(self.piece.massBlocks)
        else:
            self.set_move_status(False)
            self.spawn_piece()
        current_time = now

    def run(self):
        run = True
        while run:
            run = self.handle_events()
            self.draw()
            self.move_piece()
            self.clock.tick(FPS)

        pygame.quit()
        quit()


class Cup:
    def __init__(self, cup_h, cup_w, serface, cell_size):
        self.width, self.height = cup_w, cup_h
        self.surface = serface
        self.cell_size = cell_size
        self.gridList = [[0] * self.width for _ in range(self.height)]
        self.posX = (WINDOW_W - self.width * cell_size) // 2
        self.posY = WINDOW_H - self.height * cell_size
        self.colors = {
            "LIGHT_BLUE": (135, 206, 250),
            "BLUE": (70, 130, 180),
            "LIGHT_GREEN": (144, 238, 144),
            "GREEN": (34, 139, 34),
            "LIGHT_PINK": (255, 182, 193),
            "PINK": (220, 20, 60),
            "LIGHT_ORANGE": (255, 165, 0),
            "ORANGE": (255, 140, 0),
            "LIGHT_PURPLE": (221, 160, 221),
            "PURPLE": (138, 43, 226),
            "LIGHT_YELLOW": (255, 255, 102),
            "YELLOW": (255, 215, 0),
            "LIGHT_MINT": (175, 238, 238),
            "MINT": (72, 209, 204)
        }

    def clear(self):
        for line in range(len(self.gridList)):
            for col in range(len(self.gridList[line])):
                if self.gridList[line][col] in [1, 2, 3, 4, 5, 6, 7, 8]:
                    self.gridList[line][col] = 0

    def delete_lines(self):
        lines = []
        # flag = False
        for x in range(len(self.gridList) - 1, -1, -1):
            if 0 not in self.gridList[x]:
                # if not flag:
                #     [print(x) for x in self.gridList]
                flag = True
                lines.append(x)

        if lines:
            print(f"--->{len(lines)}<---")

            for m in lines:
                del self.gridList[m]

            for _ in lines:
                self.gridList.insert(0, [0] * self.width)

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
                        drawRect(self.surface, self.colors["LIGHT_BLUE"], rect)
                    case 2:
                        drawRect(self.surface, self.colors["LIGHT_GREEN"], rect)
                    case 3:
                        drawRect(self.surface, self.colors["LIGHT_PINK"], rect)
                    case 4:
                        drawRect(self.surface, self.colors["LIGHT_ORANGE"], rect)
                    case 5:
                        drawRect(self.surface, self.colors["LIGHT_PURPLE"], rect)
                    case 6:
                        drawRect(self.surface, self.colors["LIGHT_YELLOW"], rect)
                    case 7:
                        drawRect(self.surface, self.colors["LIGHT_MINT"], rect)
                    case 10:
                        drawRect(self.surface, self.colors["BLUE"], rect)
                    case 20:
                        drawRect(self.surface, self.colors["GREEN"], rect)
                    case 30:
                        drawRect(self.surface, self.colors["PINK"], rect)
                    case 40:
                        drawRect(self.surface, self.colors["ORANGE"], rect)
                    case 50:
                        drawRect(self.surface, self.colors["PURPLE"], rect)
                    case 60:
                        drawRect(self.surface, self.colors["YELLOW"], rect)
                    case 70:
                        drawRect(self.surface, self.colors["MINT"], rect)


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
        self.id = 1
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
        self.id = 2
        # self.moving_color = (144, 238, 144)  # Светлый цвет
        # self.stopped_color = (34, 139, 34)  # Тёмный цвет

    def update(self):
        self.variations = [[(self.X, self.Y), (self.X + 1, self.Y), (self.X, self.Y + 1), (self.X + 1, self.Y + 1)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations


class S_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 3
        # self.moving_color = (255, 182, 193)  # Светлый цвет
        # self.stopped_color =   # Тёмный цвет

    def update(self):
        self.variations = [[(self.X - 1, self.Y + 1), (self.X, self.Y + 1), (self.X, self.Y), (self.X + 1, self.Y)],
                           [(self.X - 1, self.Y - 1), (self.X - 1, self.Y), (self.X, self.Y), (self.X, self.Y + 1)]]
        self.massBlocks = self.variations[self.variationNum]
        return self.variations


class Z_Type(Shape):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.id = 4
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
        self.id = 5
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
        self.id = 6
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
        self.id = 7
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
