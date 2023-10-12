from typing import Callable, Literal

import pygame.mouse
from pygame import Surface, Vector2, Rect, Cursor, SYSTEM_CURSOR_HAND, SYSTEM_CURSOR_ARROW
from pygame.font import Font


class Menu:
    """
    A very specific menu that is used to display buttons that invoke operations on a stack
    and output, if any
    """

    class TextButton:
        def __init__(self, text: str, top_left: Vector2, on_click_handler: Callable[[], None]):
            self.text = text
            self.rect = Rect(top_left, Vector2(100, 100))
            self.font = Font(None, 50)
            self.color: Literal["Black", "Purple", "Red"] = "Black"
            self.on_click_handler = on_click_handler

        def render(self, menu: Surface):
            menu.blit(self.font.render(self.text, True, self.color).convert_alpha(), self.rect)

            self.listen_for_click()

        def listen_for_click(self):
            pressed = pygame.mouse.get_pressed()
            mouse_pos = Vector2(pygame.mouse.get_pos())
            mouse_pos.x -= 600  # To account for positioning relative to menu Surface

            if self.rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(Cursor(SYSTEM_CURSOR_HAND))
                self.color = "Purple"
                if pressed[0]:
                    self.on_click_handler()
                    self.color = "Red"
            else:
                self.color = "Black"
                pygame.mouse.set_cursor(Cursor(SYSTEM_CURSOR_ARROW))

    class CommandOutput:
        def __init__(self, text: str, top_left: Vector2):
            self.text = text
            self.font = Font(None, 50)
            self.color: Literal["Red", "Green"] = "Green"

            self.top_left = top_left

        def update(self, text: str):
            self.text = text

        def render(self, menu: Surface):
            menu.blit(self.font.render(self.text, True, self.color), self.top_left)

    def __init__(self, buttons: list[TextButton]):
        self.image = Surface(Vector2(600, 800)).convert_alpha()
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
        pygame.draw.line(screen,
                         "Black",
                         Vector2(screen_rect.centerx, 350),
                         Vector2(screen_rect.right, 350),
                         width=4)
        for button in self.buttons:
            button.render(self.image)
