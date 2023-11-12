import pygame as pg
from pygame import Vector2, Surface, Rect
from pygame.font import Font

from stack import Stack


class Spring:
    def __init__(self, mid_bottom: Vector2):
        self.original_image = pg.image.load("../assets/spring.png").convert_alpha()
        self.original_image = pg.transform.scale_by(self.original_image, 0.85)
        self.image = self.original_image

        self.rect = self.image.get_rect()
        self.base = mid_bottom
        self.rect.midbottom = self.base

        self.resize_factor = 0.88
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


class Candy:
    CANDY_COLORS = ["Red", "Green", "Pink", "Yellow"]
    CURRENT_COLOR_INDEX = 0

    def __init__(self, mid_bottom: Vector2):
        self.size = Vector2(200, 30)
        self.surface = Surface(self.size).convert_alpha()
        self.surface.fill("Limegreen")
        self.surface.set_colorkey("Limegreen")
        self.rect = self.surface.get_rect()
        self.rect.midbottom = mid_bottom

        self.color_rect = Rect(Vector2(0, 0), Vector2(self.rect.size))

        self.color = self.CANDY_COLORS[self.CURRENT_COLOR_INDEX % len(self.CANDY_COLORS)]
        self.number = self.CURRENT_COLOR_INDEX
        self.font = Font(None, 22)
        self.font_surface = self.font.render(str(self.number), True, "Black").convert_alpha()
        self.font_rect = Rect(Vector2(0, 0), self.font_surface.get_size())
        self.font_rect.center = self.color_rect.center

    def __str__(self):
        return f"Candy({self.number=}, {self.color=})"

    def __repr__(self):
        return f"Candy({self.number=}, {self.color=})"

    def set_font(self):
        self.font_surface = self.font.render(str(self.number), True, "Black").convert_alpha()

    def render(self, surface: Surface):
        self.set_font()
        surface.blit(self.surface, self.rect)
        pg.draw.rect(self.surface, self.color, self.color_rect, border_radius=10)
        self.surface.blit(self.font_surface, self.font_rect)


class CandyDispenser:
    def __init__(self, spring_mid_bottom: Vector2):
        self.spring = Spring(spring_mid_bottom)
        self.candies = Stack[Candy]()

    def push_candy(self):
        self.spring.shrink()
        if self.candies.is_empty():
            self.candies.push(Candy(self.spring.rect.midtop))
        else:
            previous_candy = self.candies.peek()
            self.candies.push(Candy(previous_candy.rect.midtop))
            for i in range(len(self.candies)):
                if i == 0:
                    self.candies[i].rect.midbottom = self.spring.rect.midtop
                else:
                    self.candies[i].rect.midbottom = self.candies[i - 1].rect.midtop

        Candy.CURRENT_COLOR_INDEX += 1

        print(self.candies)

    def pop_candy(self):
        if not self.candies.is_empty():
            self.spring.grow()

            self.candies.pop()
            for i in range(len(self.candies)):
                if i == 0:
                    self.candies[i].rect.midbottom = self.spring.rect.midtop
                else:
                    self.candies[i].rect.midbottom = self.candies[i - 1].rect.midtop

            Candy.CURRENT_COLOR_INDEX -= 1

        print(self.candies)

    def render(self, surface: Surface):
        self.spring.render(surface)

        for candy in self.candies:
            candy.render(surface)
