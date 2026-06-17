"""
Tests for orderings.constraint_le
"""

from lattices.orderings import constraint_le


def test_constraint_le_empty():
    assert constraint_le(frozenset(), frozenset({frozenset({0})}))
    assert not constraint_le(frozenset({frozenset({0})}), frozenset())


def test_constraint_le_refinement():
    alpha = frozenset({frozenset({0})})
    beta = frozenset({frozenset({0, 1})})
    assert constraint_le(alpha, beta)
    assert not constraint_le(beta, alpha)
