from typing import List, Set
from NFAe import NFAe, State
from RegularExpression import *
from _merge_nfae import merge as merge_nfae
from _merge_nfae import MergeTransitions
from functools import reduce as foldl
from copy import copy


def _convert_null(node: RENull) -> NFAe:
    return NFAe(
        state_count=1,
        accepting_states=set(),
        alphabet=set(),
        transitions={},
        initial_state=0
    )


def _convert_empty(node: REEmpty) -> NFAe:
    return NFAe(
        state_count=1,
        accepting_states={0},
        alphabet=set(),
        transitions={},
        initial_state=0
    )


def _convert_conc(node: REConc) -> NFAe:

    xs: List[NFAe] = []

    for child in node.nodes:
        xs.append(_convert_node(child))

    # Fold along all the NFAes created keeping track of the merged automaton and the initial state

    def aux(a: NFAe, b: NFAe) -> NFAe:

        # Create merging transitions

        a_to_b: MergeTransitions = {}

        for s in a.accepting_states:
            a_to_b[(s, None)] = {b.initial_state}

        # Perform merge

        new, _, b_mapping = merge_nfae(a, b,
                         a_to_b,
                         {},
                         a.initial_state, False)

        # Update accepting states

        new_accepting_states: Set[State] = set()

        for s in b.accepting_states:
            new_accepting_states.add(b_mapping[s])

        new.accepting_states = new_accepting_states

        # Return new NFAe

        return new

    res: NFAe = foldl(aux, xs)

    return res


def _convert_sym(node: RESym) -> NFAe:

    sym = node.sym

    return NFAe(
        state_count=2,
        accepting_states={1},
        alphabet={sym},
        transitions={
            (0, sym): {1}
        },
        initial_state=0
    )


def _convert_repeat(node: RERepeat) -> NFAe:

    nfae = _convert_node(node.node)

    # Add new state

    nfae.state_count += 1
    new_state = nfae.state_count - 1

    # Add ε-transition into original initial state

    nfae.transitions[(new_state, None)] = {nfae.initial_state}

    # Update initial state

    nfae.initial_state = new_state

    # Add ε-transitions from original accepting states

    for s in nfae.accepting_states:

        key = (s, None)

        if key in nfae.transitions:
            nfae.transitions[key].add(new_state)
        else:
            nfae.transitions[key] = {new_state}

    # Update accepting state

    nfae.accepting_states = {new_state}

    # Return output

    return nfae


def _convert_union(node: REUnion) -> NFAe:

    xs: List[NFAe] = []

    for child in node.nodes:
        xs.append(_convert_node(child))

    def aux(a: NFAe, b: NFAe) -> NFAe:

        a_to_b: MergeTransitions = {
            (a.initial_state, None): {b.initial_state}
        }

        return merge_nfae(
            a, b,
            a_to_b,
            {},
            a.initial_state,
            False
        )[0]

    base = NFAe(
        state_count=1,
        accepting_states=set(),
        alphabet=set(),
        transitions={},
        initial_state=0
    )

    res: NFAe = foldl(
        aux,
        xs,
        base
    )

    return res


def _convert_node(node: RENode) -> NFAe:

    match node:
        case RENull():
            return _convert_null(node)
        case REEmpty():
            return _convert_empty(node)
        case REConc():
            return _convert_conc(node)
        case RESym():
            return _convert_sym(node)
        case RERepeat():
            return _convert_repeat(node)
        case REUnion():
            return _convert_union(node)
        case _:
            raise ValueError("Unknown RENode type provided")


def convert(regex: RegularExpression) -> NFAe:

    nfae = _convert_node(regex.root)

    assert nfae.alphabet.issubset(regex.alphabet), "Regular expression alphabet doesn't match it's nodes"

    nfae.alphabet = copy(regex.alphabet)

    return nfae
