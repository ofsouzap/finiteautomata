from DFA import DFA, Symbol, State


class DFARunner:

    def __init__(self,
                 dfa: DFA):

        self._dfa = dfa
        self._state: State = dfa.initial_state

    def read_symbol(self, sym: Symbol) -> None:
        self._state = self._dfa.get_next_state(self._state, sym)

    @property
    def state(self) -> State:
        return self._state

    @property
    def accepting(self) -> bool:
        return self._state in self._dfa.accepting_states
