from typing import Generic, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    """
    This is a software stack that stores elements in LIFO.
    Generics were added purely for type hinting; assuming that items of the
    same type will be stored in the stack.
    The Python interpreter, however, does not enforce this at runtime.
    """
    class EmptyStackException(Exception):
        def __init__(self):
            super().__init__("Stack is empty")

    class _StackIterator(Generic[T]):
        def __init__(self, elements: list[T]):
            self._elements = elements
            self._index = 0

        def __iter__(self):
            return self

        def __next__(self) -> T:
            if self._index >= len(self._elements):
                raise StopIteration
            else:
                element = self._elements[self._index]
                self._index += 1
                return element

    def __init__(self):
        self.elements: list[T] = []

    def __len__(self) -> int:
        return len(self.elements)

    def is_empty(self):
        """Returns `True` if the stack has no elements"""
        return len(self) == 0

    def push(self, element: T) -> None:
        """Adds an element to the top of the stack"""
        self.elements.append(element)

    def pop(self) -> T:
        """
        Removes and returns the element at the top of the stack
        :raises EmptyStackException If the stack is empty
        """
        if self.is_empty():
            raise Stack.EmptyStackException()
        return self.elements.pop()

    def peek(self) -> T:
        """
        Returns (but does not remove) the element at the top of the stack
        :raises EmptyStackException if the stack is empty
        """
        if self.is_empty():
            raise Stack.EmptyStackException()
        return self.elements[len(self) - 1]

    def __iter__(self):
        return Stack._StackIterator(self.elements)
