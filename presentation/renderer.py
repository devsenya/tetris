import pygame


class CupRenderer:
    def __init__(self, surface, cup_width, cup_height, cell_size, gridList, color):
        self.gridList = gridList
        self.cup_width, self.cup_height = cup_width, cup_height
        self.surface = surface
        self.cell_size = cell_size
        self.color = color

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

    def draw(self, posX, posY):
        self.posX = posX
        self.posY = posY

        # отрисовка вертикальных линий
        for numLine in range(self.cup_width + 1):
            startPoint = self.posX + self.cell_size * numLine, self.posY
            endPoint = self.posX + self.cell_size * numLine, self.posY + self.cell_size * self.cup_height

            pygame.draw.line(self.surface, self.color, startPoint, endPoint)
        # отрисовка горизонтальных линий
        for x in range(self.cup_height + 1):
            pygame.draw.line(self.surface, self.color, (self.posX, self.posY + self.cell_size * x),
                             (self.posX + self.cup_width * self.cell_size, self.posY + self.cell_size * x))
        # отрисовка фигур
        for line in range(len(self.gridList)):
            for col in range(len(self.gridList[line])):
                rect = (self.posX + self.cell_size * col, self.posY + self.cell_size * line, 20, 20)

                match self.gridList[line][col]:
                    case 1:
                        self.drawRect(self.colors["LIGHT_BLUE"], rect)
                    case 2:
                        self.drawRect(self.colors["LIGHT_GREEN"], rect)
                    case 3:
                        self.drawRect(self.colors["LIGHT_PINK"], rect)
                    case 4:
                        self.drawRect(self.colors["LIGHT_ORANGE"], rect)
                    case 5:
                        self.drawRect(self.colors["LIGHT_PURPLE"], rect)
                    case 6:
                        self.drawRect(self.colors["LIGHT_YELLOW"], rect)
                    case 7:
                        self.drawRect(self.colors["LIGHT_MINT"], rect)
                    case 10:
                        self.drawRect(self.colors["BLUE"], rect)
                    case 20:
                        self.drawRect(self.colors["GREEN"], rect)
                    case 30:
                        self.drawRect(self.colors["PINK"], rect)
                    case 40:
                        self.drawRect(self.colors["ORANGE"], rect)
                    case 50:
                        self.drawRect(self.colors["PURPLE"], rect)
                    case 60:
                        self.drawRect(self.colors["YELLOW"], rect)
                    case 70:
                        self.drawRect(self.colors["MINT"], rect)


    def drawRect(self, color, rect):
        pygame.draw.rect(self.surface, (0, 0, 0), rect)
        pygame.draw.rect(self.surface, color, (rect[0] + 1, rect[1] + 1, rect[2] - 3, rect[3] - 3))




