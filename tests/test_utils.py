"""
Tests for lattices.utils
"""

import pytest

from lattices.utils import flatten, powerset


@pytest.mark.parametrize(('stuff', 'min_size', 'size'), [
    ([0, 1, 2], 0, 8),
    ([0, 1, 2], 1, 7),
    ([0, 1, 2], 2, 4),
    ([0], 0, 2),
])
def test_powerset_1(stuff, min_size, size):
    """
    Test the size of the powerset.
    """
    assert len(list(powerset(stuff, size_limit=min_size))) == size


@pytest.mark.parametrize(('stuff', 'min_size', 'thing'), [
    ([0, 1, 2], 0, frozenset({})),
    ([0, 1, 2], 1, frozenset({0})),
    ([0, 1, 2], 2, frozenset({0, 1})),
    ([0], 0, frozenset({})),
])
def test_powerset_2(stuff, min_size, thing):
    """
    Test that certain elements are in the powerset.
    """
    assert thing in list(powerset(stuff, size_limit=min_size))


@pytest.mark.parametrize(('stuff', 'min_size', 'thing'), [
    ([0, 1, 2], 0, frozenset({3})),
    ([0, 1, 2], 1, frozenset({})),
    ([0, 1, 2], 2, frozenset({0})),
    ([0], 0, frozenset({1})),
])
def test_powerset_3(stuff, min_size, thing):
    """
    Test that certain elements are not in the powerset.
    """
    assert thing not in list(powerset(stuff, size_limit=min_size))


@pytest.mark.parametrize(('nested', 'flat', 'levels'), [
    ([[[1], 2], 3], [1, 2, 3], None),
    ([[[1], 2], 3], [[1], 2, 3], 1),
    ([[[1], 2], 3], [1, 2, 3], 2),
    ([[[1], 2], [[3]]], [[1], 2, [3]], 1),
])
def test_flatten_1(nested, flat, levels):
    """
    Test some flattenings.
    """
    list(flatten(nested, levels=levels)) == flat
