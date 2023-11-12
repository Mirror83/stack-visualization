from typing import Callable, Literal

from pygame import Surface, Vector2, Rect, SYSTEM_CURSOR_HAND, SYSTEM_CURSOR_ARROW, Cursor
from pygame.font import Font
import pygame as pg


class Menu:
    """
    A very specific menu that is used to display buttons that invoke operations on a stack
    and output, if any
    """

    # The values below are default values. They are meant to be reset in the main
    # application as needed
    FONT_SIZE = 50
    MOUSE_OFFSET = 600

    class TextButton:
        def __init__(self, text: str, top_left: Vector2, on_click_handler: Callable[[], None], font_size: int):
            self.text = text
            self.font = Font(None, font_size)
            self.color: Literal["Black", "Purple", "Red"] = "Black"
            self.font_surface = self.font.render(self.text, True, self.color).convert_alpha()
            self.rect = Rect(top_left, self.font_surface.get_size())
            self.on_click_handler = on_click_handler
            self.cursors = [Cursor(SYSTEM_CURSOR_ARROW), Cursor(SYSTEM_CURSOR_HAND)]
            self.cursor = self.cursors[0]

        def render(self, menu: Surface):
            self.check_hover()
            self.font_surface = self.font.render(self.text, True, self.color).convert_alpha()
            menu.blit(self.font_surface, self.rect)
            # pygame.draw.rect(menu, "Red", self.rect, width=1)

        def is_hover(self):
            mouse_pos = Vector2(pg.mouse.get_pos())
            mouse_pos.x -= Menu.MOUSE_OFFSET  # To account for positioning relative to menu Surface
            is_hover = self.rect.collidepoint(mouse_pos)
            return is_hover

        def check_hover(self):
            if self.is_hover():
                self.color = "Purple"
                if self.cursor != self.cursors[1]:
                    self.cursor = self.cursors[1]
                    pg.mouse.set_cursor(self.cursor)

                event = pg.event.wait()
                if event.type == pg.MOUSEBUTTONUP:
                    if event.button == pg.BUTTON_LEFT:
                        self.click()

            else:
                self.color = "Black"
                if self.cursor != self.cursors[0]:
                    self.cursor = self.cursors[0]
                    pg.mouse.set_cursor(self.cursor)

        def click(self):
            self.on_click_handler()

    class CommandOutput:
        def __init__(self, text: str, top_left: Vector2):
            self.text = text
            self.font = Font(None, Menu.FONT_SIZE)
            self.color: Literal["Red", "Green"] = "Green"

            self.top_left = top_left

        def update(self, text: str):
            self.text = text

        def render(self, menu: Surface):
            menu.blit(self.font.render(self.text, True, self.color), self.top_left)

    def __init__(self, buttons: list[TextButton], size: Vector2, font_size: int = 50, mouse_offset: float = 600):
        Menu.FONT_SIZE = font_size
        Menu.MOUSE_OFFSET = mouse_offset
        self.image = Surface(size).convert_alpha()
        self.image.fill("White")
        self.rect = self.image.get_rect()
        self.command_output = Menu.CommandOutput("", Vector2(self.rect.left + 20, 150))
        self.buttons = buttons

    def update_command_output(self, text: str):
        self.image.fill("White", Rect(0, 0, 600, 300))
        self.command_output.update(text)

    def render(self, screen: Surface):
        screen_rect = screen.get_rect()
        screen.blit(self.image, screen_rect.midtop)
        self.command_output.render(self.image)
        pg.draw.line(screen,
                         "Black",
                         Vector2(screen_rect.centerx, 350),
                         Vector2(screen_rect.right, 350),
                         width=4)

        for button in self.buttons:
            button.render(self.image)
