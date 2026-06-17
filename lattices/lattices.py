"""
Several specific types of lattices.
"""

from operator import le

from ._fm3 import FM3_NODES, fm3_lattice, lattice_from_covers
from .composition import interval
from .constraints import is_antichain, is_connected, is_cover, is_partition
from .lattice import Lattice
from .orderings import antichain_le, constraint_le, refinement_le
from .utils import powerset


__all__ = [
    'powerset_lattice',
    'boolean_lattice',
    'partition_lattice',
    'free_distributive_lattice',
    'dependency_lattice',
    'dependency_antichain_lattice',
    'partition_antichain_lattice',
    'free_modular_lattice',
    'constraint_lattice',
    'chain_lattice',
    'divisor_lattice',
    'M3',
    'N5',
    'diamond',
    'pentagon',
    'FM3',
    'S7',
    'L6',
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


boolean_lattice = powerset_lattice


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
    return Lattice(dependencies, refinement_le(), '•꞉⋮')


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


def constraint_lattice(sources):
    """
    Construct the extended constraint lattice used in synergistic disclosure.

    The lattice is oriented with the empty antichain (no constraints) at the
    top and the most constrained node at the bottom.

    Parameters
    ----------
    sources : collection
        The source variable groups used to build the underlying antichain
        lattice, e.g. ``((0,), (1,))``.

    Returns
    -------
    lattice : Lattice
        The constraint lattice.
    """
    fdl = free_distributive_lattice(sources)
    nodes = set(fdl) | {frozenset()}
    return Lattice(nodes, constraint_le).inverse()


def chain_lattice(n):
    """
    Construct a chain lattice with `n` elements.

    Parameters
    ----------
    n : int
        The number of elements. Must be at least 1.

    Returns
    -------
    lattice : Lattice
        The chain ``0 < 1 < ... < n-1``.
    """
    if n < 1:
        msg = "Chain lattices require at least one element."
        raise ValueError(msg)
    nodes = list(range(n))

    def relationship(a, b):
        return a <= b

    return Lattice(nodes, relationship)


def divisor_lattice(n):
    """
    Construct the divisor lattice of `n`.

    Nodes are positive divisors of `n`, ordered by divisibility.

    Parameters
    ----------
    n : int
        A positive integer.

    Returns
    -------
    lattice : Lattice
        The divisor lattice.
    """
    if n < 1:
        msg = "n must be a positive integer."
        raise ValueError(msg)
    nodes = [d for d in range(1, n + 1) if n % d == 0]

    def relationship(a, b):
        return b % a == 0

    return Lattice(nodes, relationship)


def _free_modular_lattice_two_generators():
    nodes = {'bot', 'x', 'y', 'top'}

    def relationship(a, b):
        order = {'bot': 0, 'x': 1, 'y': 1, 'top': 2}
        return order[a] <= order[b]

    return Lattice(nodes, relationship)


def free_modular_lattice(elements):
    """
    Construct the free modular lattice on `elements`.

    Free modular lattices with four or more generators are infinite, so only
    ``len(elements) <= 3`` is supported.

    Parameters
    ----------
    elements : collection
        The generators. Length 1 gives a 2-element chain, length 2 gives a
        4-element lattice, and length 3 gives Dedekind's 28-element lattice.

    Returns
    -------
    lattice : Lattice
        The corresponding free modular lattice.

    Raises
    ------
    ValueError
        If more than three generators are requested.
    """
    elements = list(elements)
    size = len(elements)
    if size >= 4:
        msg = "The free modular lattice on four or more generators is infinite."
        raise ValueError(msg)
    if size == 0:
        return chain_lattice(1)
    if size == 1:
        return chain_lattice(2)
    if size == 2:
        return _free_modular_lattice_two_generators()
    return fm3_lattice()


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
diamond = M3


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
pentagon = N5


FM3 = fm3_lattice()

S7 = interval(FM3, FM3_NODES[10], FM3_NODES[21])


_L6_COVERS = [
    ('1', 'b'), ('1', 'c'), ('b', 'd'), ('b', 'a'), ('d', 'a'), ('c', '0'), ('a', '0'),
]
L6 = lattice_from_covers(['0', 'a', 'b', 'c', 'd', '1'], _L6_COVERS)
