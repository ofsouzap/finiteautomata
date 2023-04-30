from typing import Set
from NFAe import NFAe, Symbol, State
from copy import copy


class NFAeRunner:

    def __init__(self,
                 nfae: NFAe):

        self._nfae = nfae
        self._states: Set[State] = {nfae.initial_state}

        self.__refresh_curr_states()

    def __refresh_curr_states(self) -> None:
        """Checks for and applies any ε-transitions in the current subset of states"""

        # This function uses a breadth-first search to build a list of states the runner should be in

        # Create queue and add initial states

        q = []

        for s in self._states:
            q.append(s)

        # Perform search

        i = 0

        while i < len(q):

            s = q[i]

            ts = self._nfae.find_epsilon_transitions(s)

            for t in ts:
                if t not in q:
                    q.append(t)

            i += 1

        self._states = set(q)


    def read_symbol(self, sym: Symbol) -> None:

        next_states = set()

        for s in self._states:
            next_states |= self._nfae.get_next_states(s, sym)

        self._states = next_states

        self.__refresh_curr_states()

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
