from pygame import Surface, Vector2, Rect
import pygame as pg
from pygame.font import Font


class Candy:
    CANDY_COLORS = ["Red", "Green", "Pink", "Yellow"]
    CURRENT_COLOR_INDEX = 0

    def __init__(self, midbottom: Vector2, size: Vector2):
        self._surface = Surface(size).convert_alpha()
        self._rect = self._surface.get_rect()
        self._rect.midbottom = midbottom
        self._color = self.CANDY_COLORS[self.CURRENT_COLOR_INDEX % len(self.CANDY_COLORS)]
        self._number = self.CURRENT_COLOR_INDEX
        self._font = Font(None, 20)
        self._font_surface = self._font.render(str(self._number), True, "Black").convert_alpha()
        self._font_rect = Rect(Vector2(0, 0), self._font_surface.get_size())
        self._font_rect.center = self._rect.center

    def mid_top(self) -> Vector2:
        return Vector2(self._rect.midtop)

    def move_down(self, amount: int):
        self._rect.y += amount

    def move_up(self, amount: int):
        self._rect.y -= amount

    def render(self, surface: Surface):
        self._font_surface = self._font.render(str(self._number), True, "Black")
        surface.blit(self._surface, self._rect)
        pg.draw.rect(self._surface, self._color, self._rect, border_radius=6)
        self._surface.blit(self._font_surface, self._font_rect)

    def __str__(self):
        return f"Candy(Number={self._number}, Color={self._color})"
