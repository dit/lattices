"""
Tests for lattices.lattices
"""

from itertools import combinations

import networkx as nx
import pytest

from lattices.composition import sub_lattice
from lattices.lattices import (
    constraint_lattice,
    dependency_antichain_lattice,
    dependency_lattice,
    free_distributive_lattice,
    information_loss_lattice,
    partition_antichain_lattice,
    partition_lattice,
    powerset_lattice,
)


@pytest.mark.parametrize("size", range(1, 5))
def test_powerset_lattice(size):
    """ """
    lattice = powerset_lattice(range(size))
    assert len(lattice._lattice) == 2**size
    assert lattice.top == set(range(size))
    assert lattice.bottom == set()


@pytest.mark.parametrize(
    ("size", "true"),
    [
        (1, 1),
        (2, 2),
        (3, 5),
        (4, 15),
    ],
)
def test_partition_lattice(size, true):
    """ """
    lattice = partition_lattice(range(size))
    assert len(lattice._lattice) == true
    assert lattice.top == {frozenset(range(size))}
    assert lattice.bottom == {frozenset({i}) for i in range(size)}


@pytest.mark.parametrize(
    ("size", "true"),
    [
        (1, 1),
        (2, 4),
        (3, 18),
        (4, 166),
    ],
)
def test_free_distributive_lattice(size, true):
    """ """
    lattice = free_distributive_lattice(range(size))
    assert len(lattice._lattice) == true
    assert lattice.top == {frozenset(range(size))}
    assert lattice.bottom == {frozenset({i}) for i in range(size)}


@pytest.mark.parametrize(
    ("size", "true"),
    [
        (1, 1),
        (2, 2),
        (3, 9),
        (4, 114),
    ],
)
def test_dependency_lattice_1(size, true):
    """ """
    lattice = dependency_lattice(range(size))
    assert len(lattice._lattice) == true
    assert lattice.top == {frozenset(range(size))}
    assert lattice.bottom == {frozenset({i}) for i in range(size)}


@pytest.mark.parametrize(
    ("size", "true"),
    [
        (1, 2),
        (2, 5),
        (3, 19),
        (4, 167),
    ],
)
def test_dependency_lattice_2(size, true):
    """ """
    lattice = dependency_lattice(range(size), cover=False)
    assert len(lattice._lattice) == true
    assert lattice.top == {frozenset(range(size))}
    assert lattice.bottom == frozenset()


@pytest.mark.parametrize(
    ("size", "true"),
    [
        (1, 2),
        (2, 5),
        (3, 19),
        (4, 164),
    ],
)
def test_dependency_lattice_3(size, true):
    """ """
    lattice = dependency_lattice(range(size), cover=False, connected=True)
    assert len(lattice._lattice) == true
    assert lattice.top == {frozenset(range(size))}
    assert lattice.bottom == frozenset()


@pytest.mark.parametrize(
    ("size", "true"),
    [
        (1, 2),
        (2, 6),
        (3, 82),
    ],
)
def test_dependency_antichain_lattice_1(size, true):
    """ """
    lattice = dependency_antichain_lattice(range(size), cover=False, connected=False)
    assert len(lattice._lattice) == true


@pytest.mark.parametrize(
    ("size", "true"),
    [
        (1, 2),
        (2, 6),
        (3, 82),
    ],
)
def test_dependency_antichain_lattice_2(size, true):
    """ """
    lattice = dependency_antichain_lattice(range(size), cover=False, connected=True)
    assert len(lattice._lattice) == true


@pytest.mark.parametrize(
    ("size", "true"),
    [
        (1, 1),
        (2, 2),
        (3, 20),
    ],
)
def test_dependency_antichain_lattice_3(size, true):
    """ """
    lattice = dependency_antichain_lattice(range(size), cover=True, connected=False)
    assert len(lattice._lattice) == true


@pytest.mark.parametrize(
    ("size", "true"),
    [
        (1, 1),
        (2, 2),
        (3, 20),
    ],
)
def test_dependency_antichain_lattice_4(size, true):
    """ """
    lattice = dependency_antichain_lattice(range(size), cover=True, connected=True)
    assert len(lattice._lattice) == true


@pytest.mark.parametrize(
    ("size", "true"),
    [
        (1, 1),
        (2, 2),
        (3, 9),
        (4, 346),
    ],
)
def test_partition_antichain_lattice(size, true):
    """ """
    lattice = partition_antichain_lattice(range(size))
    assert len(lattice._lattice) == true


@pytest.mark.parametrize(
    ("size", "true"),
    [
        (1, 1),
        (2, 4),
        (3, 18),
        (4, 166),
    ],
)
def test_information_loss_lattice(size, true):
    """ """
    lattice = information_loss_lattice(range(size))
    assert len(lattice._lattice) == true
    assert lattice.top == frozenset()
    assert lattice.bottom == {frozenset(sub) for sub in combinations(range(size), size - 1) if sub}


def _collection(label):
    """
    Parse Chicharro and Panzeri's notation: "12.3" is {{1, 2}, {3}}.
    """
    return frozenset(frozenset(map(int, source)) for source in label.split(".") if source != "∅")


# Figure 3B of Chicharro and Panzeri: each collection and the collections it covers.
FIGURE_3B_COVERS = {
    "∅": ["1", "2", "3"],
    "1": ["1.2", "1.3"],
    "2": ["1.2", "2.3"],
    "3": ["1.3", "2.3"],
    "1.2": ["12", "1.2.3"],
    "1.3": ["13", "1.2.3"],
    "2.3": ["23", "1.2.3"],
    "12": ["3.12"],
    "13": ["2.13"],
    "23": ["1.23"],
    "1.2.3": ["3.12", "2.13", "1.23"],
    "3.12": ["12.13", "12.23"],
    "2.13": ["12.13", "13.23"],
    "1.23": ["12.23", "13.23"],
    "12.13": ["12.13.23"],
    "12.23": ["12.13.23"],
    "13.23": ["12.13.23"],
}


def test_information_loss_lattice_figure_3():
    """
    The trivariate loss lattice is Figure 3B of Chicharro and Panzeri, with Figure 3D as a sublattice.
    """
    lattice = information_loss_lattice([1, 2, 3])
    covers = {
        (_collection(upper), _collection(lower)) for upper, lowers in FIGURE_3B_COVERS.items() for lower in lowers
    }
    assert set(lattice.cover_edges()) == covers
    assert lattice.validate()

    univariate = {node for node in lattice if all(len(source) == 1 for source in node)}
    sub = sub_lattice(lattice, univariate)
    assert set(sub.cover_edges()) == {(upper, lower) for upper, lower in covers if {upper, lower} <= univariate}


@pytest.mark.parametrize("size", range(2, 5))
def test_information_loss_lattice_dual_to_gain_lattice(size):
    """
    The full gain and loss lattices are dual: either Hasse diagram is the other upside down.
    """
    loss = information_loss_lattice(range(size))
    gain = free_distributive_lattice(range(size))
    assert nx.is_isomorphic(loss.hasse_diagram(), gain.hasse_diagram().reverse())


@pytest.mark.parametrize("size", range(1, 4))
def test_information_loss_lattice_is_constraint_lattice_without_bottom(size):
    """ """
    loss = information_loss_lattice(range(size))
    constraint = constraint_lattice(range(size))
    assert set(loss) == set(constraint) - {constraint.bottom}
    assert set(loss.cover_edges()) == {edge for edge in constraint.cover_edges() if constraint.bottom not in edge}
