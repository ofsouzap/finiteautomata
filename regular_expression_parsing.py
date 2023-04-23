from typing import Set, Optional
from RegularExpression import *


def _is_valid_parse_sym(c: str) -> bool:
    return \
        (ord("A") <= ord(c) <= ord("Z")) or \
        (ord("a") <= ord(c) <= ord("z")) or \
        (ord("0") <= ord(c) <= ord("9"))


def _is_valid_parse_char(c: str) -> bool:
    return \
        _is_valid_parse_sym(c) or \
        c in ["(", ")", "*", "|"]


class _StringStream:

    def __init__(self, s: str):
        self.__s = s
        self.__i = 0

    @property
    def can_read(self) -> bool:
        return self.__i < len(self.__s)

    def read(self) -> str:
        assert self.can_read
        out = self.__s[self.__i]
        self.__i += 1
        return out

    def __bool__(self) -> bool:
        return self.can_read


GroupList = List[Union["GroupList", str]]


def _read_group(stream: _StringStream) -> GroupList:

    curr: GroupList = []

    while stream:

        c = stream.read()

        if c == "(":

            curr.append(_read_group(stream))

        elif c == ")":

            return curr

        elif _is_valid_parse_char(c):

            curr.append(str(c))

        else:
            raise ValueError(f"Invalid character {c}")

    return curr


def _groups_to_re_tree(groups: GroupList) -> RENode:

    # Special case for an empty node

    if groups == []:
        return REEmpty()

    # Normal case

    union_parts: List[List[RENode]] = []
    stack: List[RENode] = []

    for x in groups:

        match x:

            case str() as c:

                if c == "*":

                    if not stack:
                        raise ValueError("Repeat character without anything to repeat")

                    repeatee = stack.pop()
                    repeat = RERepeat(repeatee)
                    stack.append(repeat)

                elif c == "|":

                    if stack:
                        union_parts.append(stack)
                        stack = []
                    else:
                        union_parts.append([REEmpty()])

                elif _is_valid_parse_sym(c):

                    stack.append(RESym(c))

                else:
                    raise ValueError(f"Unexpected character {c}")

            case list() as ys:

                stack.append(_groups_to_re_tree(ys))

    union_parts.append(stack)
    del stack

    union_nodes: List[RENode] = [REConc(*nodes) for nodes in union_parts]

    if len(union_nodes) == 1:

        # Return the only node in union_nodes

        return union_nodes[0]

    elif len(union_nodes) > 1:

        # Put the nodes of union_nodes into a union

        return REUnion(*union_nodes)

    else:
        raise Exception("Unexpected situation")


def __re_node_alphabet(n: RENode) -> Alphabet:

    match n:

        case RESym() as n_sym:
            return {n_sym.sym}

        case REConc() as n_conc:
            al: Alphabet = set()
            for child in n_conc.nodes:
                al |= __re_node_alphabet(child)
            return al

        case REUnion() as n_union:
            al: Alphabet = set()
            for child in n_union.nodes:
                al |= __re_node_alphabet(child)
            return al

        case RERepeat() as n_repeat:
            return __re_node_alphabet(n_repeat.node)

        case RENull() | REEmpty():
            return set()

        case _:
            raise ValueError(f"Unexpected RENode type for {n}")


def parse(s: str, alphabet: Optional[Alphabet] = None) -> RegularExpression:

    # Group the parts of the string by brackets

    str_stream: _StringStream = _StringStream(s)
    groups: GroupList = _read_group(str_stream)

    # Build the regular expression tree from the groups

    root: RENode = _groups_to_re_tree(groups)

    # Find alphabet

    re_alphabet: Alphabet

    if alphabet:
        re_alphabet = alphabet

    else:
        # Determine the alphabet from the set of symbols in the 
        re_alphabet = __re_node_alphabet(root)

    # Create output RegularExpression object

    regex = RegularExpression(re_alphabet, root)

    # Return output

    return regex
