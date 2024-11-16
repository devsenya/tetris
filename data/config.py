import time

import pygame

fps = 25
WINDOW_W, WINDOW_H = 600, 500
GREY = (180, 180, 180)
WHITE = (255, 255, 255)
FPS = 120
current_time = 0
now = time.time()
pygame.font.init()
LIVES_FONT = pygame.font.SysFont("comicsans", 40)