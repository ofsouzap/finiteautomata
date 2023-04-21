from typing import Union
from abc import ABC, abstractmethod
from FiniteAutomaton import Symbol, Alphabet, String


class RENode(ABC):

    @abstractmethod
    def __str__(self):
        raise NotImplementedError()

    @abstractmethod
    def _check_alphabet(self, alphabet: Alphabet):
        raise NotImplementedError()


class RENull(RENode):

    def __init__(self):
        pass

    def __str__(self):
        return "∅"

    def _check_alphabet(self, alphabet: Alphabet):
        return True


class REEmpty(RENode):

    def __init__(self):
        pass

    def __str__(self):
        return "ε"

    def _check_alphabet(self, alphabet: Alphabet):
        return True


class REConc(RENode):

    def __init__(self, *nodes: RENode):
        self.nodes = nodes

    def __str__(self):
        return "(" + ")(".join([str(n) for n in self.nodes]) + ")"

    def _check_alphabet(self, alphabet: Alphabet):
        return all([n._check_alphabet(alphabet) for n in self.nodes])


class RESym(RENode):

    def __init__(self, sym: Symbol):
        self.sym = sym

    def __str__(self):
        return self.sym

    def _check_alphabet(self, alphabet: Alphabet):
        return self.sym in alphabet


class RERepeat(RENode):

    def __init__(self, node: RENode):
        self.node = node

    def __str__(self):
        return f"({str(self.node)})*"

    def _check_alphabet(self, alphabet: Alphabet):
        return self.node._check_alphabet(alphabet)


class REUnion(RENode):

    def __init__(self, *opts: RENode):
        self.nodes = opts

    def __str__(self):
        return "(" + ")|(".join([str(n) for n in self.nodes]) + ")"

    def _check_alphabet(self, alphabet: Alphabet):
        return all([n._check_alphabet(alphabet) for n in self.nodes])


def re_lit_string(string: Union[String, str]) -> RENode:
    return REConc(*[RESym(sym) for sym in string])


class RegularExpression:

    def __init__(self, alphabet: Alphabet, root: RENode):

        self.alphabet: Alphabet = alphabet
        self.root: RENode = root

        assert self.__check_alphabet()

    def __check_alphabet(self) -> bool:

        return self.root._check_alphabet(self.alphabet)

    def __str__(self) -> str:
        return str(self.root)
