from typing import Any


class Stack:
    class EmptyStackException(Exception):
        def __init__(self):
            super().__init__("Stack is empty")

    def __init__(self):
        self.elements = []

    def __len__(self) -> int:
        return len(self.elements)

    def is_empty(self):
        return len(self) == 0

    def push(self, element: Any) -> None:
        self.elements.append(element)

    def pop(self) -> Any:
        if self.is_empty():
            raise Stack.EmptyStackException()
        return self.elements.pop()

    def peek(self) -> Any:
        if self.is_empty():
            raise Stack.EmptyStackException()
        return self.elements[len(self) - 1]
