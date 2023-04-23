from typing import Set, Iterator
from FiniteAutomaton import String, Symbol


def generate_strings(alphabet: Set[Symbol],
                     prev: String,
                     N: int) -> Iterator[String]:

    yield prev

    if N == 0:

        return

    else:

        for c in alphabet:

            new = prev + c

            for out in generate_strings(alphabet, new, N-1):
                yield out  # Yield with greater lengths