"""
Several specific types of lattices.
"""

from operator import le

from .constraints import is_antichain, is_connected, is_cover, is_partition
from .lattice import Lattice
from .orderings import antichain_le, refinement_le
from .utils import powerset


__all__ = [
    'powerset_lattice',
    'partition_lattice',
    'free_distributive_lattice',
    'dependency_lattice',
    'dependency_antichain_lattice',
    'partition_antichain_lattice',
    'free_modular_lattice',
    'M3',
    'N5',
]


def powerset_lattice(elements):
    """
    Construct the powerset lattice, representing all subsets of `elements`
    ordered by inclusion.

    Parameters
    ----------
    elements : collection
        The elements to use to construct the lattice.

    Returns
    -------
    lattice : Lattice
        The corresponding lattice.
    """
    return Lattice(powerset(elements), le)


def partition_lattice(elements):
    """
    Construct the partition lattice, representing all partitions of `elements`
    ordered by refinement.

    Parameters
    ----------
    elements : collection
        The elements to use to construct the lattice.

    Returns
    -------
    lattice : Lattice
        The corresponding lattice.
    """
    partitions = [part for part in powerset(powerset(elements, 1), 1) if is_partition(part, elements)]
    return Lattice(partitions, refinement_le(), symbols='|')


def free_distributive_lattice(elements):
    """
    Construct the free distributive lattice over `elements`, that is the lattice
    of antichains of the powerset of `elements`, ordered by containment.

    Parameters
    ----------
    elements : collection
        The elements to use to construct the lattice.

    Returns
    -------
    lattice : Lattice
        The corresponding lattice.
    """
    antichains = [ac for ac in powerset(powerset(elements, 1), 1) if is_antichain(ac)]
    return Lattice(antichains, antichain_le())


def dependency_lattice(elements, cover=True, connected=False):
    """
    Construct the lattice of antichains of the powerset of `elements`, ordered
    by refinement.

    Parameters
    ----------
    elements : collection
        The elements to use to construct the lattice.
    cover : bool
        Whether the antichains should be covers. Defaults to True.
    connected : bool
        Whether the antichains should represent a connected component. Defaults
        to False.

    Returns
    -------
    lattice : Lattice
        The corresponding lattice.
    """
    dependencies = [dep for dep in powerset(powerset(elements, 1)) if is_antichain(dep)]
    if cover:
        dependencies = [dep for dep in dependencies if is_cover(dep, elements)]
    if connected:
        dependencies = [dep for dep in dependencies if is_connected(dep)]
    return Lattice(dependencies, refinement_le(), '꞉⋮•')


def dependency_antichain_lattice(elements, cover=True, connected=False):
    """
    Construct the lattice of antichains of dependencies of the powerset of
    `elements`, ordered by containment.

    Parameters
    ----------
    elements : collection
        The elements to use to construct the lattice.
    cover : bool
        Whether the dependencies should be covers. Defaults to True.
    connected : bool
        Whether the dependencies should represent a connected component. Defaults
        to False.

    Returns
    -------
    lattice : Lattice
        The corresponding lattice.
    """
    dependencies = [dep for dep in powerset(powerset(elements, 1)) if is_antichain(dep)]
    if cover:
        dependencies = [dep for dep in dependencies if is_cover(dep, elements)]
    if connected:
        dependencies = [dep for dep in dependencies if is_connected(dep)]
    dependency_acs = [dep_ac for dep_ac in powerset(dependencies, 1) if is_antichain(dep_ac, refinement_le())]
    return Lattice(dependency_acs, antichain_le(refinement_le()))


def partition_antichain_lattice(elements):
    """
    Construct the lattice of antichains of partitions of the powerset of
    `elements`, ordered by refinement.

    Parameters
    ----------
    elements : collection
        The elements to use to construct the lattice.

    Returns
    -------
    lattice : Lattice
        The corresponding lattice.
    """
    partitions = [part for part in powerset(powerset(elements, 1), 1) if is_partition(part, elements)]
    partitions_acs = [part_ac for part_ac in powerset(partitions, 1) if is_antichain(part_ac, refinement_le())]
    return Lattice(partitions_acs, antichain_le(refinement_le()))


def free_modular_lattice(elements):
    """
    """
    raise NotImplementedError


################################################################################
# Some special lattices


nodes = {frozenset([0]),
         frozenset([1]),
         frozenset(['a']),
         frozenset(['b']),
         frozenset(['c']),
         }


def m3_order(a, b):
    """
    The smallest non-distributive lattice.
    """
    if a == {0} or b == {1}:
        return True
    else:
        return False


M3 = Lattice(nodes, m3_order)


def n5_order(a, b):
    """
    The smallest non-modular lattice.
    """
    if a == {0} or b == {1}:
        return True
    elif a == {'a'} and b == {'b'}:
        return True
    else:
        return False


N5 = Lattice(nodes, n5_order)
