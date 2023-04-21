from typing import List
from abc import ABC, abstractmethod
from FiniteAutomaton import Symbol, String


class RENode(ABC):

    @abstractmethod
    def __str__(self):
        raise NotImplementedError()


class RENull(RENode):

    def __init__(self):
        pass

    def __str__(self):
        return "∅"


class REEmpty(RENode):

    def __init__(self):
        pass

    def __str__(self):
        return "ε"


class REConc(RENode):

    def __init__(self, *nodes: RENode):
        self.nodes = nodes

    def __str__(self):
        return "(" + ")(".join([str(n) for n in self.nodes]) + ")"


class RESym(RENode):

    def __init__(self, sym: Symbol):
        self.sym = sym

    def __str__(self):
        return self.sym


class RERepeat(RENode):

    def __init__(self, node: RENode):
        self.node = node

    def __str__(self):
        return f"({str(self.node)})*"


class REUnion(RENode):

    def __init__(self, *opts: RENode):
        self.nodes = opts

    def __str__(self):
        return "(" + ")|(".join([str(n) for n in self.nodes]) + ")"


class RegularExpression:

    def __init__(self, root: RENode):
        self.root: RENode = root

    def __str__(self) -> str:
        return str(self.root)
