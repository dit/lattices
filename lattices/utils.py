"""
Utilities for constructing and working with lattices.
"""

from collections.abc import Iterable
from itertools import chain, combinations


__all__ = [
    'flatten',
    'powerset',
]


def flatten(l, levels=None):
    """
    Flatten an irregular list of lists.

    Parameters
    ----------
    l : iterable
       The object to be flattened.

    Yields
    ------
    el : object
        The non-iterable items in `l`.
    """
    if levels == 0:
        yield from l
    else:
        for el in l:
            if isinstance(el, Iterable) and not (isinstance(el, str) and len(el) == 1):
                levels = levels if levels is None else levels - 1
                for sub in flatten(el, levels):
                    yield sub
            else:
                yield el


def powerset(iterable, size_limit=0):
    """
    powerset([1,2,3]) --> {} {1} {2} {3} {1,2} {1,3} {2,3} {1,2,3}

    Parameters
    ----------
    iterable : iterable
        The elements of the set from which the powerset is to be computed.
    size_limit : int >= 0
        Yield only subsets of at least this size. For example, if `size_limit`
        is 1, only non-empty subsets are yielded.

    Yields
    ------
    subset : frozenset
        A subset of `iterable`.
    """
    s = list(iterable)
    for set_ in chain.from_iterable(combinations(s, r) for r in range(size_limit, len(s) + 1)):
        yield frozenset(set_)
