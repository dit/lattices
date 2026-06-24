"""
Lattices is a package for the construction of lattices from a set of nodes and
an ordering relation.
"""

__version__ = "0.5.1"

from .composition import interval, product_lattice, sub_lattice
from .lattice import Lattice, stringify
from .lattices import (
    FM3,
    L6,
    M3,
    N5,
    S7,
    boolean_lattice,
    chain_lattice,
    constraint_lattice,
    dependency_antichain_lattice,
    dependency_lattice,
    diamond,
    divisor_lattice,
    free_distributive_lattice,
    free_modular_lattice,
    partition_antichain_lattice,
    partition_lattice,
    pentagon,
    powerset_lattice,
)
from .orderings import antichain_le, constraint_le, refinement_le

__all__ = [
    "Lattice",
    "stringify",
    "powerset_lattice",
    "boolean_lattice",
    "partition_lattice",
    "free_distributive_lattice",
    "dependency_lattice",
    "dependency_antichain_lattice",
    "partition_antichain_lattice",
    "free_modular_lattice",
    "constraint_lattice",
    "chain_lattice",
    "divisor_lattice",
    "product_lattice",
    "sub_lattice",
    "interval",
    "M3",
    "N5",
    "diamond",
    "pentagon",
    "FM3",
    "S7",
    "L6",
    "antichain_le",
    "constraint_le",
    "refinement_le",
    "__version__",
]
