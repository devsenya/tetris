import random
import time

import pygame

from data import config, blocks
from data.blocks import I_Type, S_Type, Z_Type, L_Type, T_Type, J_Type, O_Type
from data.board import Cup
from data.config import WINDOW_W, WINDOW_H, WHITE, LIVES_FONT, FPS, GREY
from presentation.renderer import CupRenderer




class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("TETRIS")
        self.clock = pygame.time.Clock()
        self.cup = Cup(20, 10)
        self.demoCup = Cup(4, 4)
        self.cupRenderer = CupRenderer(self.win, self.cup.width, self.cup.height, 20, self.cup.gridList, GREY)
        self.demoCupRenderer = CupRenderer(self.win, self.demoCup.width, self.demoCup.height, 20, self.demoCup.gridList, WHITE)
        self.piece = None
        self.demoPiece = None
        self.spawn_piece()
        self.spawn_demoPiece()
        self.background_image = pygame.image.load("IM1.JPG")
        self.SCORE = 0
        self.linesToNextLevel = 10
        self.LEVEL = 0
        self.set_speed()  # Интервал времени между падениями фигурки (в секундах)
        print()

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

        self.win.fill(WHITE)
        score = LIVES_FONT.render(str(self.SCORE), 1, "black")
        self.win.blit(score, (0, 0))
        self.cupRenderer.draw((config.WINDOW_W - self.cupRenderer.cup_width * self.cupRenderer.cell_size) // 2, config.WINDOW_H - self.cupRenderer.cup_height * self.cupRenderer.cell_size)
        self.demoCupRenderer.draw(450, 50)
        pygame.display.flip()

    def move_piece(self):
        global current_time, now
        now = time.time()
        # подение куба
        # должно будет работать только если фигура еще падает
        if now - current_time >= self.fall_time:
            self.move_down()

    def spawn_piece(self):
        global now, current_time
        for line in self.cup.gridList:
            for x in line:
                if 1 <= x <= 7:
                    return
        else:
            self.piece = self.demoPiece if self.demoPiece else blocks.randomPiece()
            self.spawn_demoPiece()
            self.piece.set_XY(self.piece.X, self.piece.Y)
            self.set_move_status()
            now = time.time()
            current_time = now

    def spawn_demoPiece(self):
        self.demoCup.clear()
        self.demoPiece = blocks.randomPiece()
        self.demoPiece.set_XY(self.demoPiece.X, self.demoPiece.Y)
        for cube in self.demoPiece.massBlocks:
            try:
                self.demoCup.gridList[cube[1]][cube[0]-3] = self.demoPiece.id
            except:
                print(cube[1])


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
            if count_lines := self.cup.delete_lines():
                self.set_score(count_lines)
                self.check_level(count_lines)

    def set_score(self, count_lines):
        match count_lines:
            case 1:
                self.SCORE += 100
            case 2:
                self.SCORE += 300
            case 3:
                self.SCORE += 700
            case 4:
                self.SCORE += 1500
            case _:
                pass

    def set_speed(self):
        match self.LEVEL:
            case 0: frame = 48
            case 1: frame = 43
            case 2: frame = 38
            case 3: frame = 33
            case 4: frame = 28
            case 5: frame = 23
            case 6: frame = 18
            case 7: frame = 13
            case 8: frame = 8
            case 9: frame = 6
            case 10: frame = 5
            case 11: frame = 5
            case 12: frame = 5
            case 13: frame = 4
            case 14: frame = 4
            case 15: frame = 4
            case 16: frame = 3
            case 17: frame = 3
            case 18: frame = 3
            case _: frame = 2
        self.fall_time = round(frame / 60, 2)

    def check_level(self, count_lines):
        self.linesToNextLevel -= count_lines
        if self.linesToNextLevel <= 0:
            self.LEVEL += 1
            self.set_speed()
            print("Уровень-----", self.LEVEL)
            self.linesToNextLevel = 10 - abs(self.linesToNextLevel)

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
