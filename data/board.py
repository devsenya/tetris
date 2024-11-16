import pygame

from data.config import WINDOW_W, WINDOW_H, GREY


def drawRect(surface, color, rect):
    pygame.draw.rect(surface, (0, 0, 0), rect)
    pygame.draw.rect(surface, color, (rect[0] + 1, rect[1] + 1, rect[2] - 3, rect[3] - 3))

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
        return len(lines)

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