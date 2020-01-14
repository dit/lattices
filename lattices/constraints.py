"""
Various conditions one might employ in defining a lattice.
"""

from itertools import combinations
from operator import le

import networkx as nx


__all__ = [
    'is_antichain',
    'is_cover',
    'is_partition',
    'is_connected',
]


def is_antichain(set_of_sets, le=le):
    """
    Determine whether `set_of_sets` represents an antichain; that is,
    whether all pairs of sets within `set_of_sets` are incomperable
    according to `le`.

    Parameters
    ----------
    set_of_sets : a (frozen)set of (frozen)sets
        The potential antichain.
    le : func
        A function which determines whether one set is "less than" another.
        Defaults to operator.le (the built-in <=).

    Returns
    -------
    antichain : bool
        Whether set_of_sets represents an antichain or not.
    """
    for i, j in combinations(set_of_sets, 2):
        if le(i, j) or le(j, i):
            return False
    return True


def is_cover(set_of_sets, alphabet):
    """
    Determine whether `set_of_sets` is a cover of `alphabet`; that is,
    is every element of `alphabet` represented somewhere in `set_of_sets`?

    Parameters
    ----------
    set_of_sets : a (frozen)set of (frozen)sets
        The potential covering.
    alphabet : set
        The full alphabet.

    Returns
    -------
    cover : bool
        Whether set_of_sets is a cover or not.
    """
    return set().union(*set_of_sets) == set(alphabet)


def is_partition(set_of_sets, alphabet):
    """
    Determine whether `set_of_sets` partitions `alphabet`; that is,
    is every element of `alphabet` represented exactly once in `set_of_sets`?

    Parameters
    ----------
    set_of_sets : a (frozen)set of (frozen)sets
        The potential partition.
    alphabet : set
        The full alphabet.

    Returns
    -------
    partition : bool
        Whether set_of_sets is a partition or not.
    """
    pairwise_disjoint = not any(i & j for i, j in combinations(set_of_sets, 2))
    return pairwise_disjoint and is_cover(set_of_sets, alphabet)


def is_connected(set_of_sets):
    """
    Determine whether `set_of_sets` forms a connected set.

    Parameters
    ----------
    set_of_sets : a (frozen)set of (frozen)sets
        The potentially connected set.

    Returns
    -------
    connected : bool
        Whether set_of_sets is connected or not.
    """
    graph = nx.Graph()
    for set_ in set_of_sets:
        graph.add_edges_from(combinations(set_, 2))

    return len(list(nx.connected_components(graph))) <= 1
