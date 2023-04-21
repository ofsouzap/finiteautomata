from typing import List, Set, Iterable
from abc import ABC, abstractmethod, abstractproperty


State = int
Symbol = str
Alphabet = Set[Symbol]


class String:

    def __init__(self, *syms: Symbol):
        self.__syms: List[Symbol] = list(syms)

    def __str__(self) -> str:
        return "".join(self.__syms)

    def __len__(self) -> int:
        return len(self.__syms)

    def __add__(self, other) -> "String":

        if isinstance(other, String):

            return String(*self.__syms, *other.__syms)

        elif isinstance(other, Symbol):

            return String(*self.__syms, other)

        else:
            raise ValueError(other)

    def __iter__(self):
        return iter(self.__syms)
