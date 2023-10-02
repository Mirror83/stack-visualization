from typing import Any

import pygame


class Candy(pygame.sprite.Sprite):
    VERTICAL_START = 600

    def __init__(self, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.image = pygame.Surface((50, 50))
        self.image.fill("Red")
        self.rect = self.image.get_rect(midbottom=(500, Candy.VERTICAL_START))
        print(f"{Candy.VERTICAL_START=}")
        self.t = 0

    # def interpolate(self):
    #     old_x = 0
    #     new_x = 1000
    #
    #     self.rect.x = old_x + (new_x - old_x) * self.t
    #     if self.rect.x == new_x:
    #         self.t = 0
    #     else:
    #         self.t += 0.005
    #
    #     print(self.rect.x)

    @classmethod
    def decrement_vertical_start(cls):
        Candy.VERTICAL_START -= 75

    @classmethod
    def increment_vertical_start(cls):
        Candy.VERTICAL_START += 75

    def update(self, *args: Any, **kwargs: Any) -> None:
        pass
