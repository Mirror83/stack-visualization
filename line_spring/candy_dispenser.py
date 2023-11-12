import pygame as pg
from pygame import Vector2, Surface, Rect

from line_spring.candy import Candy
from stack import Stack


class CandyDispenser:
    def __init__(self, top_left: Vector2, size: Vector2):
        self._capacity = 13  # Arbitrarily defined
        self._container_surface = Surface(size)
        self._container_rect = Rect(top_left, size)
        self._container_color = "Black"

        self._spring_surface = Surface(Vector2(100, 400))
        self._spring_rect = Rect(Vector2(0, 0), self._spring_surface.get_size())
        self._spring_rect.midbottom = self._container_rect.midbottom
        self._points: list[Vector2] = []
        self._y_separation = 30
        self._compression_rate = 30
        for i in range(0, self._spring_rect.bottom, self._y_separation):
            self._points.append(Vector2(0, i))
            self._points.append(Vector2(self._spring_rect.w, i))

        self._candies: Stack[Candy] = Stack()

    def render(self, screen: Surface):
        screen.blit(self._container_surface, self._container_rect)
        self._container_surface.fill(self._container_color)

        self._container_surface.blit(self._spring_surface, self._spring_rect)
        self._spring_surface.fill("Purple")
        pg.draw.lines(self._spring_surface, "Black", False, self._points, width=5)

        if not self._candies.is_empty():
            for candy in self._candies:
                candy.render(self._spring_surface)

    def _is_full(self) -> bool:
        return len(self._candies) == self._capacity

    def add_candy(self) -> str:
        if not self._is_full():
            for i in range(len(self._points) - 2):
                self._points[i].y += self._compression_rate

            if self._candies.is_empty():
                self._candies.push(Candy(
                    Vector2(((self._points[0].x + self._points[1].x) / 2), self._points[0].y - 2),
                    Vector2(self._spring_rect.w - 2, self._y_separation - 2)
                ))
            else:
                for candy in self._candies:
                    candy.move_down(self._y_separation)
                self._candies.push(
                    Candy(
                        Vector2(self._candies.peek().mid_top().x, self._candies.peek().mid_top().y - 2),
                        Vector2(self._spring_rect.w - 2, self._y_separation - 2)
                    )
                )
            Candy.CURRENT_COLOR_INDEX += 1

            return ""
        else:
            return "Candy dispenser is full"

    def remove_candy(self) -> str:
        if self._candies.is_empty():
            return "No candy to remove"
        else:
            for i in range(len(self._points) - 2):
                self._points[i].y -= self._compression_rate

            for candy in self._candies:
                candy.move_up(self._y_separation)

            popped_candy = self._candies.pop()
            Candy.CURRENT_COLOR_INDEX -= 1
            return str(popped_candy)

    def peek(self) -> str:
        if self._candies.is_empty():
            return "Candy dispenser is empty"
        return str(self._candies.peek())

    def is_empty(self) -> str:
        return str(self._candies.is_empty())

    def number_of_candies(self) -> str:
        return str(len(self._candies))
