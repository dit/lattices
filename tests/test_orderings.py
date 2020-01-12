"""
Tests for lattices.orderings
"""

import pytest

from lattices.orderings import antichain_le, refinement_le


@pytest.mark.parametrize(('a', 'b'), [
    ({frozenset({0}), frozenset({1})}, {frozenset({0})}),
    ({frozenset({0}), frozenset({1}), frozenset({2})}, {frozenset({0, 1}), frozenset({1, 2})}),
])
def test_antichain_le_1(a, b):
    """
    Test that a <= b.
    """
    assert antichain_le()(a, b)


@pytest.mark.parametrize(('a', 'b'), [
    ({frozenset({0}), frozenset({1})}, {frozenset({2})}),
    ({frozenset({0, 1}), frozenset({1, 2})}, {frozenset({0}), frozenset({1})}),
    ({frozenset({0})}, {frozenset({1})}),
])
def test_antichain_le_2(a, b):
    """
    Test that a !<= b.
    """
    assert not antichain_le()(a, b)


@pytest.mark.parametrize(('a', 'b'), [
    ({frozenset({0}), frozenset({1})}, {frozenset({0, 1})}),
    ({frozenset({0, 1}), frozenset({0, 2}), frozenset({1, 2})}, {frozenset({0, 1, 2})}),
])
def test_refinement_le_1(a, b):
    """
    Test that a <= b.
    """
    assert refinement_le()(a, b)


@pytest.mark.parametrize(('a', 'b'), [
    ({frozenset({0}), frozenset({1})}, {frozenset({2})}),
    ({frozenset({0, 1}), frozenset({2})}, {frozenset({0}), frozenset({1}), frozenset({2})}),
    ({frozenset({0, 1}), frozenset({2})}, {frozenset({0, 2}), frozenset({1})}),
])
def test_refinement_le_2(a, b):
    """
    Test that a !<= b.
    """
    assert not refinement_le()(a, b)
