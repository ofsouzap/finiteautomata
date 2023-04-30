from typing import List, Optional, Set
from _mathutil import ipow
from DFA import DFA, State, State, Alphabet
from RegularExpression import *


class __DFARegexComputer:

    def __init__(self, dfa: DFA):

        self.__dfa = dfa

        # The regex tree to get from `s` to `t` using nodes forming the binary mask with binary unsigned integer representation `b` is stored at self.__dp[s][t][b]

        self.__dp: List[List[List[Optional[RENode]]]] = [
            [
                [None for _ in range(ipow(2, self.__dfa.state_count))]
                for _ in range(self.__dfa.state_count)
            ]
            for _ in range(self.__dfa.state_count)
        ]

    @staticmethod
    def __subset_to_int(subset: Set[State]) -> int:

        out = 0

        for q in subset:
            out += 1 << q

        return out

    @property
    def __alphabet(self) -> Alphabet:
        return self.__dfa.alphabet

    def compute(self, s: State, t: State, _acp_states: Optional[Set[State]] = None) -> RENode:
        """Computes a regular expression to represent the paths between nodes in the DFA

Parameters:

    s: `State` - the starting state

    t: `State` - the destination state

    _acp_states: `Set[State]` (optional) - the states that the path is allowed to use. Defaults to allowing any states

Returns:

    root: `RENode` - the root node of the regular expression tree created
"""

        # Determine accepted intermediate states

        acp_states: Set[State]

        if _acp_states is None:
            acp_states = set()
            for q in range(self.__dfa.state_count):
                acp_states.add(q)
        else:
            acp_states = set(_acp_states)  # Copy it for safety

        acp_int: int = self.__subset_to_int(acp_states)

        # Check dp results for precomputed result

        curr_res: Optional[RENode] = self.__dp[s][t][acp_int]
        if curr_res is not None:
            return curr_res
        del curr_res

        # Compute regex tree

        result: RENode

        if len(acp_states) == 0:

            # Can't pass through any intermediate states. Only can use transitions directly between `s` and `t`

            union_nodes: List[RENode] = []

            for sym in self.__alphabet:

                key = (s, sym)

                if (key in self.__dfa.transitions) and (self.__dfa.transitions[key] == t):
                    union_nodes.append(RESym(sym))

            if s == t:
                union_nodes.append(REEmpty())

            if len(union_nodes) == 1:
                result = union_nodes[0]
            elif len(union_nodes) > 1:
                result = REUnion(*union_nodes)
            else:
                result = RENull()

        else:

            # Pick any element to use to remove for the later steps

            removed: State = 0  # Just to help VS Code type-checking

            for removed in acp_states: break  # Will find an arbitrary element in acp_states without removing it

            new_acp_states = acp_states - {removed}

            # Compute getting from `s` to `t` without using `removed`

            node_without: RENode = self.compute(s, t, new_acp_states)

            # Compute getting from `s` to `t` going through `removed` in 3 steps:
            #     1. getting to `removed`
            #     2. any looping that may or may not be done from `removed` back to `removed`
            #     3. getting from `removed` to `t`

            node_with_start: RENode = self.compute(s, removed, new_acp_states)
            node_with_looping: RENode = self.compute(removed, removed, new_acp_states)
            node_with_end: RENode = self.compute(removed, t, new_acp_states)

            # Combine the results as a|b(c*)d where a is `node_without`, b is `node_with_start`, c is `node_with_looping` and d is `node_with end`

            result = REUnion(
                node_without,
                REConc(
                    node_with_start,
                    RERepeat(node_with_looping),
                    node_with_end
                )
            )

        # Store result

        self.__dp[s][t][acp_int] = result

        # Return result

        return result


def convert(dfa: DFA) -> RegularExpression:

    # The alphabets are the same

    alphabet: Alphabet = dfa.alphabet

    # Compute the regex tree

    root: RENode

    if len(dfa.accepting_states) > 0:

        computer: __DFARegexComputer = __DFARegexComputer(dfa)

        union_nodes: List[RENode] = []

        for accepting in dfa.accepting_states:
            union_nodes.append(computer.compute(dfa.initial_state, accepting))

        if len(union_nodes) == 1:
            root = union_nodes[0]
        else:
            root = REUnion(*union_nodes)

    else:
        root = RENull()  # If there are no accepting states then don't bother with the computation

    # Return regular expression object

    return RegularExpression(alphabet, root)
