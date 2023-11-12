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

        self.height_change = 30

    def set_height_change(self, height_change: float):
        self.height_change = height_change

    def reset_rect(self):
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.base

    def shrink(self):
        self.image = pg.transform.scale(self.original_image, Vector2(self.rect.size[0], self.rect.size[1] - 30))
        self.reset_rect()

    def grow(self):
        self.image = pg.transform.scale(self.original_image, Vector2(self.rect.size[0], self.rect.size[1] + 30))
        self.reset_rect()

    def render(self, surface: Surface):
        surface.blit(self.image, self.rect)


class Candy:
    CANDY_COLORS = ["Red", "Green", "Pink", "Yellow"]
    CURRENT_COLOR_INDEX = 0

    def __init__(self, mid_bottom: Vector2, size: Vector2 = Vector2(200, 30)):
        self.size = size
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
        return f"Candy(number={self.number}, color={self.color})"

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
    def __init__(self, mid_bottom: Vector2, candy_size: Vector2 | None = None):
        self.spring = Spring(Vector2(mid_bottom.x, mid_bottom.y - 10))
        self.container_rect = Rect(Vector2(0, 0), Vector2(250, self.spring.rect.height + 20))
        self.container_rect.midbottom = Vector2(mid_bottom)

        if candy_size:
            self.candy_size = candy_size
        else:
            self.candy_size = Vector2(self.container_rect.width - 30, 30)

        self.spring.set_height_change(self.candy_size.y)

        self.candies = Stack[Candy]()
        self.max_candies = 11

    def push_candy(self) -> tuple[str, bool]:
        if len(self.candies) < self.max_candies:
            self.spring.shrink()
            if self.candies.is_empty():
                self.candies.push(Candy(self.spring.rect.midtop, self.candy_size))
            else:
                previous_candy = self.candies.peek()
                self.candies.push(Candy(previous_candy.rect.midtop, self.candy_size))
                for i in range(len(self.candies)):
                    if i == 0:
                        self.candies[i].rect.midbottom = self.spring.rect.midtop
                    else:
                        self.candies[i].rect.midbottom = self.candies[i - 1].rect.midtop

            Candy.CURRENT_COLOR_INDEX += 1
            print(self.candies)
            return "", False
        else:
            print(self.candies)
            return "Candy dispenser is full!", True

    def pop_candy(self) -> tuple[str, bool]:
        if not self.candies.is_empty():
            self.spring.grow()

            popped_candy = self.candies.pop()
            for i in range(len(self.candies)):
                if i == 0:
                    self.candies[i].rect.midbottom = self.spring.rect.midtop
                else:
                    self.candies[i].rect.midbottom = self.candies[i - 1].rect.midtop

            Candy.CURRENT_COLOR_INDEX -= 1
            print(self.candies)
            return str(popped_candy), False
        else:
            print(self.candies)
            return "Candy dispenser is empty!", True

    def peek(self) -> tuple[str, bool]:
        if not self.candies.is_empty():
            return str(self.candies.peek()), False
        else:
            return "Candy dispenser is empty!", True

    def len(self) -> str:
        return str(len(self.candies))

    def is_empty(self) -> str:
        return str(self.candies.is_empty())

    def render(self, surface: Surface):
        pg.draw.rect(surface, "White", self.container_rect)
        pg.draw.rect(surface, "Darkgrey", self.container_rect, 10)
        self.spring.render(surface)

        for candy in self.candies:
            candy.render(surface)
