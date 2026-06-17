"""
Tests for new lattice API and constructors.
"""

import pytest

from lattices import (
    FM3,
    L6,
    M3,
    N5,
    S7,
    chain_lattice,
    constraint_lattice,
    divisor_lattice,
    free_modular_lattice,
    interval,
    product_lattice,
)
from lattices.lattice import Lattice
from lattices.lattices import powerset_lattice
from lattices.orderings import constraint_le


def test_len_and_contains():
    lattice = chain_lattice(4)
    assert len(lattice) == 4
    assert 2 in lattice
    assert 9 not in lattice
    assert len(lattice.nodes) == 4


def test_validate_public():
    assert M3.validate()
    invalid = Lattice(['a', 'b', 'c', 'd'], lambda a, b: (a in ['a', 'b']) and (b in ['c', 'd']))
    assert not invalid.validate()


def test_validate_on_init_raises():
    with pytest.raises(ValueError):
        Lattice(['a', 'b', 'c', 'd'], lambda a, b: (a in ['a', 'b']) and (b in ['c', 'd']), validate=True)


def test_inverse_and_dual():
    lattice = chain_lattice(3)
    inverse = lattice.inverse()
    assert inverse.top == 0
    assert inverse.bottom == 2
    assert lattice.dual().top == inverse.top


def test_covers():
    lattice = chain_lattice(3)
    assert lattice.covers(2) == {1}
    assert lattice.covers(1) == {0}


def test_mobius_chain():
    lattice = chain_lattice(3)
    cumulative = {0: 1.0, 1: 3.0, 2: 6.0}
    atoms = lattice.mobius_invert_descendants(cumulative)
    assert atoms == {0: 1.0, 1: 2.0, 2: 3.0}


def test_zeta_mobius_roundtrip():
    lattice = powerset_lattice([0, 1])
    values = {node: float(len(node)) for node in lattice}
    cumulative = lattice.zeta_transform(values)
    recovered = lattice.mobius_transform(cumulative)
    for node in lattice:
        assert recovered[node] == pytest.approx(values[node])


def test_incidence_matrix():
    lattice = chain_lattice(2)
    matrix, ordering = lattice.incidence_matrix()
    assert ordering == [1, 0]
    assert matrix == [[1, 1], [0, 1]]


def test_lookup_tables():
    lattice = M3
    assert lattice.lookup_meet(frozenset({'a'}), frozenset({'b'})) == frozenset({0})
    assert lattice.lookup_join(frozenset({'a'}), frozenset({'b'})) == frozenset({1})


def test_height_width_rank():
    lattice = powerset_lattice([0, 1, 2])
    assert lattice.height() == 4
    assert lattice.width() == 3
    assert lattice.is_ranked()
    assert lattice.rank_function()[lattice.top] == 3


def test_atoms_coatoms_complemented_boolean():
    lattice = powerset_lattice([0, 1])
    assert lattice.atoms() == {frozenset({0}), frozenset({1})}
    assert lattice.coatoms() == {frozenset({0}), frozenset({1})}
    assert lattice.is_complemented()
    assert lattice.is_boolean()


def test_cover_edges_and_hasse():
    lattice = chain_lattice(2)
    assert lattice.cover_edges() == ((1, 0),)
    assert len(lattice.hasse_diagram()) == 2


def test_product_lattice():
    product = product_lattice(chain_lattice(2), chain_lattice(2))
    assert len(product) == 4
    assert product.top == (1, 1)
    assert product.bottom == (0, 0)


def test_interval():
    lattice = powerset_lattice([0, 1, 2])
    sub = interval(lattice, frozenset({0}), frozenset({0, 1}))
    assert len(sub) == 2


def test_chain_lattice():
    assert len(chain_lattice(5)) == 5


def test_divisor_lattice():
    lattice = divisor_lattice(12)
    assert len(lattice) == 6
    assert lattice.bottom == 1
    assert lattice.top == 12


def test_constraint_lattice_matches_ordering():
    sources = ((0,), (1,))
    lattice = constraint_lattice(sources)
    assert lattice.top == frozenset()
    assert len(lattice) == 5
    assert constraint_le(frozenset({frozenset({0})}), frozenset({frozenset({0, 1})}))


def test_free_modular_small_n():
    assert len(free_modular_lattice([0])) == 2
    assert len(free_modular_lattice([0, 1])) == 4
    assert len(free_modular_lattice([0, 1, 2])) == 28
    with pytest.raises(ValueError):
        free_modular_lattice([0, 1, 2, 3])


def test_named_lattice_properties():
    assert M3.modular and not M3.distributive
    assert N5.modular is False
    assert len(FM3) == 28
    assert len(S7) == 7
    assert S7.validate()
    assert L6.modular is False
    assert len(L6) == 6
