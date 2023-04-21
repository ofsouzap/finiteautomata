from typing import Set
from NFA import NFA, Symbol, State


class NFARunner:

    def __init__(self,
                 nfa: NFA):

        self._nfa = nfa
        self._states: Set[State] = {nfa.initial_state}

    def read_symbol(self, sym: Symbol) -> None:

        next_states = set()

        for s in self._states:
            for t in self._nfa.get_next_states(s, sym):
                next_states.add(t)

        self._states = next_states

    @property
    def states(self) -> Set[State]:
        return self._states

    def in_state(self, state: State) -> bool:
        return state in self.states

    @property
    def accepting(self) -> bool:

        for s in self.states:
            if s in self._nfa.accepting_states:
                return True

        return False
