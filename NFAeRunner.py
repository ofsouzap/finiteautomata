from typing import Set
from NFAe import NFAe, Symbol, State


class NFAeRunner:

    def __init__(self,
                 nfae: NFAe):

        self._nfae = nfae
        self._states: Set[State] = {nfae.initial_state}

    def read_symbol(self, sym: Symbol) -> None:

        next_states = set()

        for s in self._states:
            for t in self._nfae.get_next_states(s, sym):
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
            if s in self._nfae.accepting_states:
                return True

        return False
