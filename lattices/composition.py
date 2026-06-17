"""
Lattice constructors built from other lattices.
"""

from .lattice import Lattice

__all__ = [
    "product_lattice",
    "sub_lattice",
    "interval",
]


def product_lattice(lattice_a, lattice_b):
    """
    Construct the Cartesian product of two lattices.

    ``(a, b) <= (c, d)`` iff ``a <= c`` in ``lattice_a`` and ``b <= d`` in
    ``lattice_b``.

    Parameters
    ----------
    lattice_a, lattice_b : Lattice
        The factor lattices.

    Returns
    -------
    lattice : Lattice
        The product lattice.
    """
    nodes = {(a, b) for a in lattice_a for b in lattice_b}
    le_a = lattice_a._relationship
    le_b = lattice_b._relationship

    def relationship(pair_a, pair_b):
        return le_a(pair_a[0], pair_b[0]) and le_b(pair_a[1], pair_b[1])

    return Lattice(nodes, relationship)


def sub_lattice(lattice, nodes):
    """
    Restrict a lattice to a subset of nodes that forms a sublattice.

    Parameters
    ----------
    lattice : Lattice
        The parent lattice.
    nodes : collection
        Nodes to retain. The induced subposet must be a lattice.

    Returns
    -------
    sub : Lattice
        The sublattice.

    Raises
    ------
    ValueError
        If the subset does not form a lattice.
    """
    nodes = set(nodes)
    sub = Lattice(nodes, lattice._relationship, symbols=lattice._symbols)
    if not sub.validate():
        msg = "The given nodes do not form a sublattice."
        raise ValueError(msg)
    return sub


def interval(lattice, lo, hi):
    """
    Construct the closed order interval ``[lo, hi]``.

    Parameters
    ----------
    lattice : Lattice
        The parent lattice.
    lo, hi : node
        The least and greatest elements of the interval.

    Returns
    -------
    sub : Lattice
        The interval sublattice.
    """
    le = lattice._relationship
    nodes = {n for n in lattice if le(lo, n) and le(n, hi)}
    return sub_lattice(lattice, nodes)
