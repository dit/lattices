"""
Tests for lattices.lattices
"""

import pytest

from lattices.lattices import (dependency_antichain_lattice,
                               dependency_lattice,
                               free_distributive_lattice,
                               partition_antichain_lattice,
                               partition_lattice,
                               powerset_lattice,
                               )


@pytest.mark.parametrize('size', range(1, 5))
def test_powerset_lattice(size):
    """
    """
    lattice = powerset_lattice(range(size))
    assert len(lattice._lattice) == 2**size
    assert lattice.top == set(range(size))
    assert lattice.bottom == set()


@pytest.mark.parametrize(('size', 'true'), [
    (1, 1),
    (2, 2),
    (3, 5),
    (4, 15),
])
def test_partition_lattice(size, true):
    """
    """
    lattice = partition_lattice(range(size))
    assert len(lattice._lattice) == true
    assert lattice.top == {frozenset(range(size))}
    assert lattice.bottom == {frozenset({i}) for i in range(size)}


@pytest.mark.parametrize(('size', 'true'), [
    (1, 1),
    (2, 4),
    (3, 18),
    (4, 166),
])
def test_free_distributive_lattice(size, true):
    """
    """
    lattice = free_distributive_lattice(range(size))
    assert len(lattice._lattice) == true
    assert lattice.top == {frozenset(range(size))}
    assert lattice.bottom == {frozenset({i}) for i in range(size)}


@pytest.mark.parametrize(('size', 'true'), [
    (1, 1),
    (2, 2),
    (3, 9),
    (4, 114),
])
def test_dependency_lattice_1(size, true):
    """
    """
    lattice = dependency_lattice(range(size))
    assert len(lattice._lattice) == true
    assert lattice.top == {frozenset(range(size))}
    assert lattice.bottom == {frozenset({i}) for i in range(size)}


@pytest.mark.parametrize(('size', 'true'), [
    (1, 2),
    (2, 5),
    (3, 19),
    (4, 167),
])
def test_dependency_lattice_2(size, true):
    """
    """
    lattice = dependency_lattice(range(size), cover=False)
    assert len(lattice._lattice) == true
    assert lattice.top == {frozenset(range(size))}
    assert lattice.bottom == frozenset()


@pytest.mark.parametrize(('size', 'true'), [
    (1, 2),
    (2, 5),
    (3, 19),
    (4, 164),
])
def test_dependency_lattice_3(size, true):
    """
    """
    lattice = dependency_lattice(range(size), cover=False, connected=True)
    assert len(lattice._lattice) == true
    assert lattice.top == {frozenset(range(size))}
    assert lattice.bottom == frozenset()


@pytest.mark.parametrize(('size', 'true'), [
    (1, 2),
    (2, 6),
    (3, 82),
])
def test_dependency_antichain_lattice_1(size, true):
    """
    """
    lattice = dependency_antichain_lattice(range(size), cover=False, connected=False)
    assert len(lattice._lattice) == true


@pytest.mark.parametrize(('size', 'true'), [
    (1, 2),
    (2, 6),
    (3, 82),
])
def test_dependency_antichain_lattice_2(size, true):
    """
    """
    lattice = dependency_antichain_lattice(range(size), cover=False, connected=True)
    assert len(lattice._lattice) == true


@pytest.mark.parametrize(('size', 'true'), [
    (1, 1),
    (2, 2),
    (3, 20),
])
def test_dependency_antichain_lattice_3(size, true):
    """
    """
    lattice = dependency_antichain_lattice(range(size), cover=True, connected=False)
    assert len(lattice._lattice) == true


@pytest.mark.parametrize(('size', 'true'), [
    (1, 1),
    (2, 2),
    (3, 20),
])
def test_dependency_antichain_lattice_4(size, true):
    """
    """
    lattice = dependency_antichain_lattice(range(size), cover=True, connected=True)
    assert len(lattice._lattice) == true


@pytest.mark.parametrize(('size', 'true'), [
    (1, 1),
    (2, 2),
    (3, 9),
    (4, 346),
])
def test_partition_antichain_lattice(size, true):
    """
    """
    lattice = partition_antichain_lattice(range(size))
    assert len(lattice._lattice) == true
