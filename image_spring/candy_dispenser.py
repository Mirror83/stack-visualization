import pygame as pg
from pygame import Vector2, Surface


class Spring:
    def __init__(self, mid_bottom: Vector2):
        self.original_image = pg.image.load("../assets/spring.png").convert_alpha()
        self.original_image = pg.transform.scale_by(self.original_image, 0.85)
        self.image = self.original_image

        self.rect = self.image.get_rect()
        self.base = mid_bottom
        self.rect.midbottom = self.base

        self.resize_factor = 0.95
        self.resize_exponent = 0

    def reset_rect(self):
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.base

    def shrink(self):
        self.resize_exponent += 1
        self.image = pg.transform.scale_by(self.original_image, (1, self.resize_factor ** self.resize_exponent))
        self.reset_rect()

    def grow(self):
        self.resize_exponent -= 1
        self.image = pg.transform.scale_by(self.original_image, (1, self.resize_factor ** self.resize_exponent))
        self.reset_rect()

    def render(self, surface: Surface):
        surface.blit(self.image, self.rect)
