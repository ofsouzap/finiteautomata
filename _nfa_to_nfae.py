from typing import Dict, Optional
from FiniteAutomaton import Symbol
from NFA import NFA
from NFAe import NFAe


def convert(nfa: NFA) -> NFAe:

    nfae_transitions: NFAe.Transitions = {}

    for key in nfa.transitions:
        nfae_transitions[key] = nfa.transitions[key]

    return NFAe(
        state_count=nfa.state_count,
        accepting_states=nfa.accepting_states,
        alphabet=nfa.alphabet,
        transitions=nfae_transitions,
        initial_state=nfa.initial_state
    )
