from NFA import NFA
from DFA import DFA

from _merge_nfae import merge as merge_nfaes
from _regular_expression_to_nfae import convert as regular_expression_to_nfae
from _nfae_to_dfa import convert as nfae_to_dfa
from _nfa_to_nfae import convert as nfa_to_nfae

def nfa_to_dfa(nfa: NFA) -> DFA:
    return nfae_to_dfa(nfa_to_nfae(nfa))
