"""
Tests for lattices.constraints
"""

import pytest

from lattices.constraints import (is_antichain,
                                  is_connected,
                                  is_cover,
                                  is_partition)


@pytest.mark.parametrize('set_of_sets', [
    {frozenset({0})},
    {frozenset({0}), frozenset({1})},
    {frozenset({0, 1}), frozenset({1, 2})},
])
def test_is_antichain_1(set_of_sets):
    """
    Test that specific sets of sets are antichains.
    """
    assert is_antichain(set_of_sets)


@pytest.mark.parametrize('set_of_sets', [
    {frozenset({0}), frozenset({0, 1})},
    {frozenset({0, 1}), frozenset({0, 1, 2})},
    {frozenset({0}), frozenset({1}), frozenset({0, 1})},
])
def test_is_antichain_2(set_of_sets):
    """
    Test that specific sets of sets are not anitchains.
    """
    assert not is_antichain(set_of_sets)


@pytest.mark.parametrize('set_of_sets', [
    {frozenset({0})},
    {frozenset({0}), frozenset({1, 2})},
    {frozenset({0, 1}), frozenset({1, 2})},
    {frozenset({0, 1, 2}), frozenset({2, 3})},
])
def test_is_connected_1(set_of_sets):
    """
    Test that specific sets of sets are connected.
    """
    assert is_connected(set_of_sets)


@pytest.mark.parametrize('set_of_sets', [
    {frozenset({0, 1}), frozenset({2, 3})},
    {frozenset({0, 1, 2}), frozenset({3, 4})},
])
def test_is_connected_2(set_of_sets):
    """
    Test that specific sets of sets are not connected.
    """
    assert not is_connected(set_of_sets)


@pytest.mark.parametrize(('set_of_sets', 'alphabet'), [
    ({frozenset({0})}, [0]),
    ({frozenset({0}), frozenset({1, 2})}, [0, 1, 2]),
    ({frozenset({0, 1}), frozenset({1, 2})}, [0, 1, 2]),
    ({frozenset({0, 1, 2}), frozenset({2, 3})}, [0, 1, 2, 3]),
])
def test_is_cover_1(set_of_sets, alphabet):
    """
    Test that specific sets of sets are a covering.
    """
    assert is_cover(set_of_sets, alphabet)


@pytest.mark.parametrize(('set_of_sets', 'alphabet'), [
    ({frozenset({0, 1})}, [0, 1, 2]),
    ({frozenset({0, 1}), frozenset({2})}, [0, 1]),
])
def test_is_cover_2(set_of_sets, alphabet):
    """
    Test that specific sets of sets are not a covering.
    """
    assert not is_cover(set_of_sets, alphabet)


@pytest.mark.parametrize(('set_of_sets', 'alphabet'), [
    ({frozenset({0})}, [0]),
    ({frozenset({0}), frozenset({1, 2})}, [0, 1, 2]),
    ({frozenset({0, 1}), frozenset({2})}, [0, 1, 2]),
    ({frozenset({0, 1}), frozenset({2, 3})}, [0, 1, 2, 3]),
])
def test_is_partition_1(set_of_sets, alphabet):
    """
    Test that specific sets of sets are a partition.
    """
    assert is_partition(set_of_sets, alphabet)


@pytest.mark.parametrize(('set_of_sets', 'alphabet'), [
    ({frozenset({0, 1}), frozenset({1, 2})}, [0, 1, 2]),
    ({frozenset({0, 1})}, [0, 1, 2]),
])
def test_is_partition_2(set_of_sets, alphabet):
    """
    Test that specific sets of sets are not a partition.
    """
    assert not is_partition(set_of_sets, alphabet)
