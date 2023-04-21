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

        old_states = set()
        new_states = copy(self._states)

        while len(old_states) != len(new_states):  # This will keep running until no ε-transitions can be found anymore

            old_states = copy(new_states)
            new_states = set()

            for s in old_states:

                new_states.add(s)

                for t in self._nfae.find_epsilon_transitions(s):
                    new_states.add(t)

        self._states = new_states


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
