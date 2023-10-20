import numpy as np
import pygame as pg
from pygame.math import Vector2

import sys

pg.init()

MAX_FPS = 60
clock = pg.time.Clock()

SCREEN_SIZE = Vector2(1000, 800)
screen = pg.display.set_mode(SCREEN_SIZE)

multiplier = 1
start = 100


def sin_wave(period_multiplier: float, start_y: int) -> list[Vector2]:
    x: np.ndarray = np.linspace(0, 4 * np.pi, 100)
    vectors = [Vector2(400 + 20 * np.sin(period_multiplier * num), pg.math.clamp(start_y + 20 * num, start_y, 360)) for
               num in x if
               start_y + 20 * num <= 360]
    vectors.append(Vector2(vectors[len(vectors) - 1].x - 30, vectors[len(vectors) - 1].y))
    return vectors


t = 0

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == pg.BUTTON_LEFT:
                multiplier += 0.5
                start += 10

            elif event.button == pg.BUTTON_RIGHT:
                if multiplier > 1:
                    multiplier -= 0.5
                    start -= 10

    screen.fill("White")

    pg.draw.lines(screen, "Black", False, sin_wave(multiplier, start))

    pg.display.update()
    clock.tick(MAX_FPS)
