# TODO: Create an over-arching class to hold the objects required for the simulation

from sys import exit

import pygame
from pygame import Vector2, MOUSEBUTTONUP
from pygame.event import Event

from candy_utils.candy import Candy
from candy_utils.candy_group import CandyGroup
from candy_utils.menu import Menu
from candy_utils.spring import Spring
from stack import Stack

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800

screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stack Visualization")

candy_stack = Stack()

push_event = Event(pygame.event.custom_type())
pop_event = Event(pygame.event.custom_type())
top_event = Event(pygame.event.custom_type())
is_empty_event = Event(pygame.event.custom_type())
len_event = Event(pygame.event.custom_type())

spring = Spring()
candy_group = CandyGroup()
last_candy: Candy | None = None


# Click handlers for the TextButtons

def on_push():
    pygame.time.delay(100)
    pygame.event.post(push_event)


def on_pop():
    pygame.time.delay(100)
    pygame.event.post(pop_event)


def on_top():
    pygame.time.delay(100)
    pygame.event.post(top_event)


def on_is_empty():
    pygame.time.delay(100)
    pygame.event.post(is_empty_event)


def on_len():
    pygame.time.delay(100)
    pygame.event.post(len_event)


buttons = [
    Menu.TextButton("S.push()", Vector2(20, 450), on_push),
    Menu.TextButton("S.pop()", Vector2(20, 550), on_pop),
    Menu.TextButton("S.top()", Vector2(200, 450), on_top),
    Menu.TextButton("S.isEmpty()", Vector2(200, 550), on_is_empty),
    Menu.TextButton("len(S)", Vector2(380, 450), on_len)
]
menu = Menu(buttons)

Candy.VERTICAL_START = Candy.BASE_VERTICAL_START = SCREEN_HEIGHT - Spring.SIZE.y - 120

clock = pygame.time.Clock()
MAX_FPS = 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event == push_event:
            is_done_shifting = candy_group.is_done_shifting()
            if Candy.VERTICAL_START > 0 and is_done_shifting:
                candy = Candy()
                candy_stack.push(candy)
                candy_group.add(candy)
                candy_group.shift_after_addition()
                spring.move_down()
                menu.update_command_output("")
                print(len(candy_stack))
            elif not is_done_shifting:
                # print("Still shifting")
                menu.update_command_output("")
            else:
                menu.update_command_output("Stack full")
                print("Stack full")
        elif event == pop_event:
            print(event)
            is_done_shifting = candy_group.is_done_shifting()
            if not candy_stack.is_empty() and is_done_shifting:
                if len(candy_stack) == 1:
                    last_candy = popped_candy = candy_stack.pop()
                else:
                    popped_candy = candy_stack.pop()

                candy_group.remove(popped_candy)
                candy_group.shift_after_removal()
                spring.move_up()
                menu.update_command_output(str(popped_candy))
                print(len(candy_stack))
            elif not is_done_shifting:
                if last_candy is not None:
                    menu.update_command_output(str(last_candy))
                # print("Still shifting")
            else:
                if last_candy is not None:
                    print(last_candy)
                    menu.update_command_output(str(last_candy))
                else:
                    menu.update_command_output("Nothing to remove")
                    print("Nothing to remove")
                last_candy = None

        elif event == top_event:
            if not candy_stack.is_empty():
                menu.update_command_output(str(candy_stack.peek()))
                print(candy_stack.peek())
            else:
                menu.update_command_output("Candy stack is empty")
                print("Candy stack is empty")

        elif event == is_empty_event:
            menu.update_command_output(str(candy_stack.is_empty()))
            print(candy_stack.is_empty())

        elif event == len_event:
            menu.update_command_output(str(len(candy_stack)))
            print(len(candy_stack))

    screen.fill("Black")  # Erase the screen so that trails of objects at previous positions are not seen

    spring.render(screen)

    candy_group.draw(screen)
    candy_group.update()

    menu.render(screen)

    pygame.display.flip()
    clock.tick(MAX_FPS)
