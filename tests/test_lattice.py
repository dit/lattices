"""
Tests for lattices.lattice
"""

import pytest

from lattices.lattice import Lattice, stringify
from lattices.lattices import M3, N5, free_distributive_lattice, powerset_lattice


@pytest.mark.parametrize(('a', 'b', 'c'), [
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


@pytest.mark.parametrize(('lattice', 'node', 'parents'), [
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


@pytest.mark.parametrize(('lattice', 'node'), [
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


@pytest.mark.parametrize(('lattice', 'node', 'parents'), [
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


@pytest.mark.parametrize(('lattice', 'node'), [
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


@pytest.mark.parametrize(('lattice', 'a', 'b', 'true'), [
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


@pytest.mark.parametrize(('lattice', 'a', 'b', 'predicate', 'trues'), [
    (free_distributive_lattice(range(3)),
     frozenset({frozenset({0}), frozenset({1})}),
     frozenset({frozenset({0}), frozenset({2})}),
     lambda n: len(n) == 1,
     [frozenset({frozenset({0})}),
      frozenset({frozenset({1, 2})}),
      ],
     ),
])
def test_lattice_join_2(lattice, a, b, predicate, trues):
    """
    Test finding the join of two nodes.
    """
    assert lattice.join(a, b, predicate=predicate) in trues


@pytest.mark.parametrize(('lattice', 'a', 'b', 'true'), [
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


@pytest.mark.parametrize(('lattice', 'a', 'b', 'predicate', 'true'), [
    (free_distributive_lattice(range(3)),
     frozenset({frozenset({0, 1})}),
     frozenset({frozenset({0, 2})}),
     lambda n: len(n) == 1,
     frozenset({frozenset({0})})),
])
def test_lattice_meet_2(lattice, a, b, predicate, true):
    """
    Test finding the meet of two nodes.
    """
    assert lattice.meet(a, b, predicate=predicate) == true


@pytest.mark.parametrize(('lattice', 'node', 'comp'), [
    (M3, frozenset({'a'}), {frozenset({'b'}), frozenset('c')}),
    (N5, frozenset({'a'}), {frozenset({'c'})}),
    (N5, frozenset({'c'}), {frozenset({'a'}), frozenset({'b'})}),
])
def test_lattice_complement(lattice, node, comp):
    """
    Test finding the complement of a node.
    """
    assert lattice.complement(node) == comp


@pytest.mark.parametrize(('lattice', 'join_irreducibles'), [
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


@pytest.mark.parametrize(('lattice', 'meet_irreducibles'), [
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
def test_lattice_meet_irreducibles(lattice, meet_irreducibles):
    """
    Test finding the meet irreducibles of the lattice.
    """
    assert lattice.meet_irreducibles() == meet_irreducibles


@pytest.mark.parametrize(('lattice', 'irreducibles'), [
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


bad_a_nodes = ['a', 'b', 'c', 'd']


def bad_a_order(a, b):
    """
    A partial order which is not a lattice.
    """
    return (a in ['a', 'b']) and (b in ['c', 'd'])


bad_a = Lattice(bad_a_nodes, bad_a_order)

bad_b_nodes = ['a', 'b', 'c', 'd', 'e', 'f']


def bad_b_order(a, b):
    """
    A partial order which is not a lattice.
    """
    if a == 'a' or b == 'f':
        return True
    elif a in ['b', 'c']:
        return b in ['d', 'e']
    else:
        return False


bad_b = Lattice(bad_b_nodes, bad_b_order)


bad_c_nodes = ['0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', '1']


def bad_c_order(a, b):
    """
    A partial order which is not a lattice.
    """
    if a == '0' or b == '1':
        return True
    elif a == 'd':
        return b in ['a', 'b']
    elif a == 'e':
        return b in ['a', 'c']
    elif a == 'f':
        return b in ['b', 'c']
    elif a == 'g':
        return b in ['d', 'e', 'a', 'b', 'c']
    elif a == 'h':
        return b in ['d', 'f', 'a', 'b', 'c']
    elif a == 'i':
        return b in ['e', 'f', 'a', 'b', 'c']
    else:
        return False


bad_c = Lattice(bad_c_nodes, bad_c_order)


@pytest.mark.parametrize(('lattice', 'truth'), [
    (M3, True),
    (N5, True),
    (free_distributive_lattice(range(3)), True),
    (bad_a, False),
    (bad_b, False),
    (bad_c, False),
])
def test_lattice_validate(lattice, truth):
    """
    Test that lattices validate, and non-lattices don't.
    """
    assert lattice._validate() == truth


@pytest.mark.parametrize(('lattice', 'truth'), [
    (M3, False),
    (N5, False),
    (free_distributive_lattice(range(2)), True),
    (free_distributive_lattice(range(3)), True),
    (powerset_lattice(range(3)), True),
])
def test_lattice_distributive(lattice, truth):
    """
    Test lattice distributivity
    """
    assert lattice.distributive == truth


@pytest.mark.parametrize(('lattice', 'truth'), [
    (M3, True),
    (N5, False),
    (free_distributive_lattice(range(2)), True),
    (free_distributive_lattice(range(3)), True),
    (powerset_lattice(range(3)), True),
])
def test_lattice_modular(lattice, truth):
    """
    Test lattice distributivity
    """
    assert lattice.modular == truth
