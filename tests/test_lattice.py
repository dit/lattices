"""
Tests for lattices.lattice
"""

import pytest

from lattices.lattice import stringify, Lattice
from lattices.lattices import M3, N5, free_distributive_lattice


@pytest.mark.parametrize(['a', 'b', 'c'], [
    ({frozenset({0, 1}), frozenset({1, 2})}, '01•12', '•꞉⋮'),
    ({frozenset({frozenset({0}), frozenset({1})}), frozenset({1, 2})}, '0꞉1•12', '•꞉⋮'),
    ({frozenset({frozenset({0}), frozenset({1})}), frozenset({1, 2})}, '0⋮1꞉12', '꞉⋮•'),
])
def test_stringify(a, b, c):
    """
    Test that stringifying nodes works.
    """
    f = stringify(symbols=c)
    assert f(a) == b


@pytest.mark.parametrize(['lattice', 'node', 'parents'], [
    (M3, frozenset({0}), {frozenset({'a'}), frozenset({'b'}), frozenset({'c'}), frozenset({1})}),
    (M3, frozenset({'a'}), {frozenset({1})}),
    (M3, frozenset({1}), set()),
    (N5, frozenset({'c'}), {frozenset({1})}),
    (N5, frozenset({'a'}), {frozenset({'b'}), frozenset({1})}),
])
def test_lattice_ascendants_1(lattice, node, parents):
    """
    Test ascendants.
    """
    assert lattice.ascendants(node) == parents


@pytest.mark.parametrize(['lattice', 'node'], [
    (M3, frozenset({0})),
    (M3, frozenset({'a'})),
    (M3, frozenset({1})),
    (N5, frozenset({'c'})),
    (N5, frozenset({'a'})),
])
def test_lattice_ascendants_2(lattice, node):
    """
    Test that the `include` option works
    """
    assert node in lattice.ascendants(node, include=True)



@pytest.mark.parametrize(['lattice', 'node', 'parents'], [
    (M3, frozenset({0}), set()),
    (M3, frozenset({'a'}), {frozenset({0})}),
    (M3, frozenset({1}), {frozenset({'a'}), frozenset({'b'}), frozenset({'c'}), frozenset({0})}),
    (N5, frozenset({'c'}), {frozenset({0})}),
    (N5, frozenset({'b'}), {frozenset({'a'}), frozenset({0})}),
])
def test_lattice_decendants_1(lattice, node, parents):
    """
    Test decendants.
    """
    assert lattice.descendants(node) == parents


@pytest.mark.parametrize(['lattice', 'node'], [
    (M3, frozenset({0})),
    (M3, frozenset({'a'})),
    (M3, frozenset({1})),
    (N5, frozenset({'c'})),
    (N5, frozenset({'a'})),
])
def test_lattice_decendants_2(lattice, node):
    """
    Test that the `include` option works
    """
    assert node in lattice.descendants(node, include=True)


@pytest.mark.parametrize(['lattice', 'a', 'b', 'true'], [
    (M3, frozenset({0}), frozenset({'a'}), frozenset({'a'})),
    (M3, frozenset({'a'}), frozenset({'b'}), frozenset({1})),
    (M3, frozenset({'a'}), frozenset({1}), frozenset({1})),
    (N5, frozenset({'a'}), frozenset({'c'}), frozenset({1})),
    (N5, frozenset({'b'}), frozenset({'c'}), frozenset({1})),
    (N5, frozenset({'a'}), frozenset({'b'}), frozenset({'b'})),
])
def test_lattice_join_1(lattice, a, b, true):
    """
    Test finding the join of two nodes.
    """
    assert lattice.join(a, b) == true


@pytest.mark.parametrize(['lattice', 'a', 'b', 'predicate', 'true'], [
    (free_distributive_lattice(range(3)), frozenset({frozenset({0}), frozenset({1})}), frozenset({frozenset({0}), frozenset({2})}), lambda n: len(n) == 1, frozenset({frozenset({0})})),
])
def test_lattice_join_2(lattice, a, b, predicate, true):
    """
    Test finding the join of two nodes.
    """
    assert lattice.join(a, b, predicate=predicate) == true


@pytest.mark.parametrize(['lattice', 'a', 'b', 'true'], [
    (M3, frozenset({0}), frozenset({'a'}), frozenset({0})),
    (M3, frozenset({'a'}), frozenset({'b'}), frozenset({0})),
    (M3, frozenset({'a'}), frozenset({1}), frozenset({'a'})),
    (N5, frozenset({'a'}), frozenset({'c'}), frozenset({0})),
    (N5, frozenset({'b'}), frozenset({'c'}), frozenset({0})),
    (N5, frozenset({'a'}), frozenset({'b'}), frozenset({'a'})),
])
def test_lattice_meet_1(lattice, a, b, true):
    """
    Test finding the meet of two nodes.
    """
    assert lattice.meet(a, b) == true


@pytest.mark.parametrize(['lattice', 'a', 'b', 'predicate', 'true'], [
    (free_distributive_lattice(range(3)), frozenset({frozenset({0, 1})}), frozenset({frozenset({0, 2})}), lambda n: len(n) == 1, frozenset({frozenset({0})})),
])
def test_lattice_meet_2(lattice, a, b, predicate, true):
    """
    Test finding the meet of two nodes.
    """
    assert lattice.meet(a, b, predicate=predicate) == true


@pytest.mark.parametrize(['lattice', 'node', 'comp'], [
    (M3, frozenset({'a'}), {frozenset({'b'}), frozenset('c')}),
    (N5, frozenset({'a'}), {frozenset({'c'})}),
    (N5, frozenset({'c'}), {frozenset({'a'}), frozenset({'b'})}),
])
def test_lattice_complement(lattice, node, comp):
    """
    Test finding the complement of a node.
    """
    assert lattice.complement(node) == comp


@pytest.mark.parametrize(['lattice', 'join_irreducibles'], [
    (M3, {frozenset({'a'}), frozenset({'b'}), frozenset({'c'})}),
    (N5, {frozenset({'a'}), frozenset({'b'}), frozenset({'c'})}),
    (free_distributive_lattice(range(3)), {frozenset({frozenset({0})}),
                                           frozenset({frozenset({1})}),
                                           frozenset({frozenset({2})}),
                                           frozenset({frozenset({0}), frozenset({1})}),
                                           frozenset({frozenset({0}), frozenset({2})}),
                                           frozenset({frozenset({1}), frozenset({2})}),
                                           }),
])
def test_lattice_join_irreducibles(lattice, join_irreducibles):
    """
    Test finding the join irreducibles of the lattice.
    """
    assert lattice.join_irreducibles() == join_irreducibles



@pytest.mark.parametrize(['lattice', 'meet_irreducibles'], [
    (M3, {frozenset({'a'}), frozenset({'b'}), frozenset({'c'})}),
    (N5, {frozenset({'a'}), frozenset({'b'}), frozenset({'c'})}),
    (free_distributive_lattice(range(3)), {frozenset({frozenset({0})}),
                                           frozenset({frozenset({1})}),
                                           frozenset({frozenset({2})}),
                                           frozenset({frozenset({0, 1})}),
                                           frozenset({frozenset({0, 2})}),
                                           frozenset({frozenset({1, 2})}),
                                           }),
])
def test_lattice_mmet_irreducibles(lattice, meet_irreducibles):
    """
    Test finding the meet irreducibles of the lattice.
    """
    assert lattice.meet_irreducibles() == meet_irreducibles



@pytest.mark.parametrize(['lattice', 'irreducibles'], [
    (M3, {frozenset({'a'}), frozenset({'b'}), frozenset({'c'})}),
    (N5, {frozenset({'a'}), frozenset({'b'}), frozenset({'c'})}),
    (free_distributive_lattice(range(3)), {frozenset({frozenset({0})}),
                                           frozenset({frozenset({1})}),
                                           frozenset({frozenset({2})}),
                                           }),
])
def test_lattice_irreducibles(lattice, irreducibles):
    """
    Test finding the irreducibles of the lattice.
    """
    assert lattice.irreducibles() == irreducibles
