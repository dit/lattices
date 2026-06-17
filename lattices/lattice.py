"""
The fundimental Lattice class.
"""

from collections.abc import Iterable
from copy import deepcopy
from itertools import combinations, permutations

import networkx as nx

__all__ = [
    'Lattice',
]


def stringify(symbols='•꞉⋮'):
    """
    Construct a function to convert a set (of sets [of sets {...}]) into a string.

    Parameters
    ----------
    symbols : str
        The symbols to utilize to separate elements.

    Returns
    -------
    strinifier : func
        A function which stringifies.
    """
    def stringifier(things):
        """
        Convert a set (of sets [of sets {...}]) into a string.

        Parameters
        ----------
        things : (frozen)set
            The set (of sets [of sets {...}]) to stringify.

        Returns
        -------
        string : str
            The string representation of `things`.
        """
        try:
            things = list(things)
        except TypeError:  # pragma: no cover
            return str(things)

        try:
            if isinstance(things[0], Iterable) and not isinstance(things[0], str):
                stringer = stringify(symbols[1:])
                string = symbols[0].join(sorted((stringer(thing) for thing in things), key=lambda t: (-len(t), t)))
            else:
                raise IndexError
        except IndexError:
            string = ''.join(map(str, sorted(things)))

        return string if string else '∅'

    return stringifier


class Lattice(object):
    """
    A lattice.
    """

    def __init__(self, nodes, relationship, symbols='•꞉⋮', validate=False):
        """
        Given a set of nodes and an ordering, construct a lattice.

        Parameters
        ----------
        nodes : collection
            A collection of elements which are ordered by `relationship`.
        relationship : func
            A function implementing the ordering among `nodes`.
        symbols : str
            The symbols to use to separate elements of each node.
        validate : bool
            If True, raise ``ValueError`` when `relationship` does not define
            a lattice on `nodes`.

        Returns
        -------
        lattice : nx.DiGraph
            The lattice representing `relationship` over `nodes`.
        """
        nodes = list(nodes)
        if not nodes:
            msg = "Cannot construct a lattice with no nodes."
            raise ValueError(msg)
        lattice = nx.DiGraph()
        lattice.add_nodes_from(nodes)

        self._relationship = relationship
        self._symbols = symbols

        self._stringify = stringify(symbols=symbols)
        self._meet_table = None
        self._join_table = None
        self._mobius_cache = None

        for a, b in combinations(nodes, 2):
            if relationship(a, b):
                lattice.add_edge(b, a, weight=-1)
            elif relationship(b, a):
                lattice.add_edge(a, b, weight=-1)

        longest_paths = nx.algorithms.all_pairs_bellman_ford_path_length(lattice)

        new_lattice = nx.DiGraph()
        new_lattice.add_nodes_from(lattice.nodes())

        for i, paths in longest_paths:
            for j, weight in paths.items():
                if weight == -1:
                    new_lattice.add_edge(i, j)

        self._lattice = new_lattice

        self._ts = list(nx.topological_sort(new_lattice))

        self.top = self._ts[0]
        self.bottom = self._ts[-1]

        if validate and not self.validate():
            msg = "The partial order does not form a lattice."
            raise ValueError(msg)

    def __len__(self):
        """
        Return the number of nodes in the lattice.
        """
        return len(self._lattice)

    def __contains__(self, node):
        """
        Return whether `node` is in the lattice.
        """
        return node in self._lattice

    @property
    def nodes(self):
        """
        The nodes of the lattice in top-to-bottom order.
        """
        return tuple(self._ts)

    def __iter__(self):
        """
        Return an iterator over the nodes of the lattice.

        Returns
        -------
        iter : iterator
            An iterator over `self._lattice`.
        """
        return iter(self._ts)

    def validate(self):
        """
        Validate that the elements and partial order form a lattice.

        Returns
        -------
        valid : bool
            True if the partial order is a lattice, False otherwise.
        """
        return self._validate()

    def _validate(self):
        """
        Validate that the elements and partial order form a lattice.

        Returns
        -------
        valid : bool
            True if the partial order is a lattice, False otherwise.
        """
        def least_upper_bound(nodes):
            for node in nodes:
                if all(node in self.descendants(ub, include=True) for ub in nodes):
                    return node

        def greatest_lower_bound(nodes):
            for node in nodes:
                if all(node in self.ascendants(lb, include=True) for lb in nodes):
                    return node

        for a, b in combinations(self, 2):
            upper_bounds = self.ascendants(a, include=True) & self.ascendants(b, include=True)
            if not least_upper_bound(upper_bounds):
                return False
            lower_bounds = self.descendants(a, include=True) & self.descendants(b, include=True)
            if not greatest_lower_bound(lower_bounds):
                return False
        else:
            return True

    @property
    def distributive(self):
        """
        Determine whether the lattice is distributive or not:
            a ∨ (b ∧ c) = (a ∨ b) ∧ (a ∨ c)

        Returns
        -------
        distributed : bool
            Whether the lattice is distributive or not.
        """
        for a, b, c in permutations(self, 3):
            left = self.join(a, self.meet(b, c))
            right = self.meet(self.join(a, b), self.join(a, c))
            if not left == right:
                return False
        else:
            return True

    @property
    def modular(self):
        """
        Determine whether the lattice is modular or not:
            (a ∧ c) ∨ (b ∧ c) = ((a ∧ c) ∨ b) ∧ c.

        Returns
        -------
        distributed : bool
            Whether the lattice is modular or not.
        """
        for a, b, c in permutations(self, 3):
            left = self.join(self.meet(a, c), self.meet(b, c))
            right = self.meet(self.join(self.meet(a, c), b), c)
            if not left == right:
                return False
        else:
            return True

    def inverse(self):
        """
        Construct the inverse of the lattice.

        Returns
        -------
        inverse : Lattice
            The lattice inverse.
        """
        inverse = deepcopy(self)

        inverse._lattice = inverse._lattice.reverse()
        inverse._relationship = lambda a, b: self._relationship(b, a)
        inverse._ts = list(nx.topological_sort(inverse._lattice))
        inverse.top, inverse.bottom = inverse.bottom, inverse.top
        inverse._meet_table = None
        inverse._join_table = None
        inverse._mobius_cache = None

        return inverse

    def dual(self):
        """
        Return the dual lattice (alias for :meth:`inverse`).
        """
        return self.inverse()

    def ascendants(self, node, include=False):
        """
        Returns the nodes greater than `node`.

        Parameters
        ----------
        node : {{elements}}
            The node in the lattice.
        include : bool
            Whether `node` should be included or not.

        Returns
        -------
        nodes : {{{elements}}}
            A list of nodes greater than `node` in the lattice.
        """
        nodes = list(nx.bfs_tree(self._lattice.reverse(), node))
        if not include:
            nodes.remove(node)
        return set(nodes)

    def descendants(self, node, include=False):
        """
        Returns the nodes less than `node`.

        Parameters
        ----------
        node : {{elements}}
            The node in the lattice.
        include : bool
            Whether `node` should be included or not.

        Returns
        -------
        nodes : {{{elements}}}
            A list of nodes less than `node` in the lattice.
        """
        nodes = list(nx.bfs_tree(self._lattice, node))
        if not include:
            nodes.remove(node)
        return set(nodes)

    def covers(self, node):
        """
        Return the covers of `node`; the elements of the lattice immediately
        less than `node`.

        Parameters
        ----------
        node : {elements}
            The node of interest.

        Returns
        -------
        covers : {{elements}}
            The covers.
        """
        return set(self._lattice[node])

    def join(self, *nodes, predicate=None):
        """
        Return the join of `nodes`, that is the least element which is greater
        than all `nodes`.

        Parameters
        ----------
        nodes : {{elements}}
            The nodes to compute the join of.
        predicate : func
            A function for which the found join must satisfy.

        Returns
        -------
        join : {{elements}}
            The join of `nodes`.
        """
        parentss = [self.ascendants(node, include=True) for node in nodes]
        joins = {n for n in self._ts if all(n in parents for parents in parentss)}
        if predicate is not None:
            joins = {n for n in joins if predicate(n)}
        aboves = {n for n in joins if any(n in self.ascendants(ub) for ub in joins)}
        joins = list(joins - aboves)

        if joins:
            return joins[0]
        else:
            msg = "Join could not be found satisfying the predicate."
            raise ValueError(msg)

    def meet(self, *nodes, predicate=None):
        """
        Return the meet of `nodes`, that is the greatest element which is less
        than all `nodes`.

        Parameters
        ----------
        nodes : {{elements}}
            The nodes to compute the meet of.
        predicate : func
            A function for which the found meet must satisfy.

        Returns
        -------
        meet : {{elements}}
            The meet of `nodes`.
        """
        childrens = [self.descendants(node, include=True) for node in nodes]
        meets = {n for n in self._ts if all(n in children for children in childrens)}
        if predicate is not None:
            meets = {n for n in meets if predicate(n)}
        belows = {n for n in meets if any(n in self.descendants(ub) for ub in meets)}
        meets = list(meets - belows)

        if meets:
            return meets[0]
        else:
            msg = "Meet could not be found satisfying the predicate."
            raise ValueError(msg)

    def complement(self, node):
        """
        Find the complement(s) of `node`.

        Parameters
        ----------
        node : {{elements}}
            The node to find the complement(s) of.

        Returns
        -------
        complement : {{{elements}}}
            The complement(s) of `node`.
        """
        return {n for n in self._lattice if (self.join(n, node) == self.top) and
                                            (self.meet(n, node) == self.bottom)}

    def join_irreducibles(self):
        """
        The join-irreducible elements of the lattice.

        Returns
        -------
        jis : {{{elements}}}
            The list of join-irreducible elements of the lattice.
        """
        return {n for n in self._lattice if len(self._lattice[n]) == 1}

    def meet_irreducibles(self):
        """
        The meet-irreducible elements of the lattice.

        Returns
        -------
        mis : {{{elements}}}
            The list of meet-irreducible elements of the lattice.
        """
        reverse = self._lattice.reverse()
        return {n for n in reverse if len(reverse[n]) == 1}

    def irreducibles(self):
        """
        The irreducible elements of the lattice.

        Returns
        -------
        irrs : {{{elements}}}

        """
        return self.join_irreducibles() & self.meet_irreducibles()

    def chains(self):
        """
        Yield all the maximal chains of the lattice.

        Yields
        ------
        chain : list
            A maximal chain from bottom to top.
        """
        yield from nx.all_simple_paths(self._lattice.reverse(), self.bottom, self.top)

    def _build_meet_join_tables(self):
        if self._meet_table is not None:
            return
        meet_table = {}
        join_table = {}
        nodes = list(self)
        for a in nodes:
            for b in nodes:
                meet_table[(a, b)] = self.meet(a, b)
                join_table[(a, b)] = self.join(a, b)
        self._meet_table = meet_table
        self._join_table = join_table

    def lookup_meet(self, a, b):
        """
        Return the meet of `a` and `b` using a cached lookup table.
        """
        self._build_meet_join_tables()
        return self._meet_table[(a, b)]

    def lookup_join(self, a, b):
        """
        Return the join of `a` and `b` using a cached lookup table.
        """
        self._build_meet_join_tables()
        return self._join_table[(a, b)]

    def mobius_function(self):
        """
        Compute the Möbius function ``μ(a, b)`` for all ``a <= b``.

        Returns
        -------
        mu : dict
            A mapping ``(a, b) -> μ(a, b)``.
        """
        if self._mobius_cache is not None:
            return self._mobius_cache

        pairs = []
        for upper in self:
            for lower in self.descendants(upper, include=True):
                if lower == upper:
                    continue
                between = len(self.ascendants(lower, include=True) & self.descendants(upper)) - 2
                pairs.append((between, lower, upper))

        mu = {}
        for _, lower, upper in sorted(pairs):
            mu[(lower, upper)] = -sum(
                mu[(lower, mid)]
                for mid in self.descendants(upper, include=True)
                if mid != lower and mid != upper and self._relationship(lower, mid) and self._relationship(mid, upper)
            )

        for node in self:
            mu[(node, node)] = 1

        self._mobius_cache = mu
        return mu

    def zeta_transform(self, values):
        """
        Apply the zeta transform: ``g(b) = sum_{a <= b} f(a)``.

        Parameters
        ----------
        values : dict
            Mapping from lattice nodes to values ``f(a)``.

        Returns
        -------
        cumulative : dict
            The zeta-transformed values.
        """
        cumulative = {}
        for node in self:
            cumulative[node] = sum(values.get(n, 0) for n in self.descendants(node, include=True))
        return cumulative

    def mobius_transform(self, cumulative):
        """
        Apply Möbius inversion: recover ``f`` from ``g(b) = sum_{a <= b} f(a)``.

        Parameters
        ----------
        cumulative : dict
            Mapping from lattice nodes to cumulative values.

        Returns
        -------
        values : dict
            The inverted values.
        """
        values = {}
        for node in reversed(list(self)):
            values[node] = cumulative.get(node, 0) - sum(values.get(descendant, 0) for descendant in self.descendants(node))
        return values

    def mobius_invert_descendants(self, cumulative):
        """
        Invert cumulative values over descendants (PID convention).

        ``atom(b) = cumulative(b) - sum_{a in descendants(b)} atom(a)``

        Parameters
        ----------
        cumulative : dict
            Mapping from lattice nodes to cumulative redundancy values.

        Returns
        -------
        atoms : dict
            The Möbius-inverted atom values.
        """
        atoms = {}
        for node in reversed(list(self)):
            atoms[node] = cumulative.get(node, 0) - sum(atoms.get(n, 0) for n in self.descendants(node))
        return atoms

    def incidence_matrix(self, ordering=None):
        """
        Build the zeta (incidence) matrix for the lattice.

        Parameters
        ----------
        ordering : list, optional
            Node ordering for rows and columns. Defaults to top-to-bottom.

        Returns
        -------
        matrix : list of lists
            ``matrix[i][j] == 1`` iff ``ordering[i] <= ordering[j]``.
        ordering : list
            The node ordering used.
        """
        if ordering is None:
            ordering = list(self)
        index = {node: i for i, node in enumerate(ordering)}
        size = len(ordering)
        matrix = [[0] * size for _ in range(size)]
        for i, node_i in enumerate(ordering):
            for lower in self.descendants(node_i, include=True):
                matrix[i][index[lower]] = 1
        return matrix, ordering

    def height(self):
        """
        Return the length of a longest chain from bottom to top.
        """
        return max((len(chain) for chain in self.chains()), default=1)

    def width(self):
        """
        Return the size of a largest antichain.
        """
        nodes = list(self)
        best = 0
        for size in range(1, len(nodes) + 1):
            for subset in combinations(nodes, size):
                if all(
                    not self._relationship(a, b) and not self._relationship(b, a)
                    for a, b in combinations(subset, 2)
                ):
                    best = max(best, size)
        return best

    def is_ranked(self):
        """
        Return whether the lattice admits a rank function consistent with covers.
        """
        try:
            self.rank_function()
        except ValueError:
            return False
        return True

    def rank_function(self):
        """
        Return a rank function, if the lattice is ranked.

        Returns
        -------
        ranks : dict
            Mapping from nodes to their rank.

        Raises
        ------
        ValueError
            If the lattice is not ranked.
        """
        ranks = {self.bottom: 0}
        for node in reversed(self._ts):
            if node == self.bottom:
                continue
            covers = self.covers(node)
            cover_ranks = {ranks[cover] for cover in covers}
            if len(cover_ranks) != 1:
                msg = "Lattice is not ranked."
                raise ValueError(msg)
            ranks[node] = next(iter(cover_ranks)) + 1
        return ranks

    def atoms(self):
        """
        Return the atoms: elements covering the bottom.
        """
        return set(self._lattice.predecessors(self.bottom))

    def coatoms(self):
        """
        Return the coatoms: elements covered by the top.
        """
        return set(self.covers(self.top))

    def is_complemented(self):
        """
        Return whether every element has a complement.
        """
        return all(self.complement(node) for node in self)

    def is_boolean(self):
        """
        Return whether the lattice is a Boolean algebra.
        """
        return self.distributive and self.is_complemented()

    def cover_edges(self):
        """
        Return Hasse cover edges as ``(greater, lesser)`` pairs.
        """
        return tuple(self._lattice.edges())

    def hasse_diagram(self):
        """
        Return the Hasse diagram as a directed graph.
        """
        return self._lattice.copy()

    def _pretty_lattice(self):  # pragma: no cover
        """
        Construct a version of the lattice with nicer looking node labels.

        Returns
        -------
        pretty_lattice : nx.DiGraph
            A topologically-equivalent, but more nicely labeled, lattice.
        """
        edges = [(self._stringify(a), self._stringify(b)) for a, b in self._lattice.edges()]
        return nx.from_edgelist(edges, nx.DiGraph)

    def draw(self, ax=None):  # pragma: no cover
        """
        Draw a pretty version of the lattice using matplotlib.

        Parameters
        ----------
        ax : matplotlib.axes.Axes, optional
            Axes to draw on. If omitted, a new figure is created.

        Returns
        -------
        ax : matplotlib.axes.Axes
            The axes containing the drawing.
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError as exc:
            msg = "matplotlib is required for drawing; install lattices[plotting]."
            raise ImportError(msg) from exc

        graph = self._pretty_lattice()
        levels = {}
        for node in nx.topological_sort(graph.reverse()):
            preds = list(graph.predecessors(node))
            levels[node] = 0 if not preds else max(levels[p] for p in preds) + 1

        positions = {}
        by_level = {}
        for node, level in levels.items():
            by_level.setdefault(level, []).append(node)
        for level, level_nodes in by_level.items():
            width = len(level_nodes)
            for index, node in enumerate(sorted(level_nodes, key=str)):
                positions[node] = (index - (width - 1) / 2.0, -level)

        if ax is None:
            _, ax = plt.subplots(figsize=(max(6, len(self) / 4), max(4, self.height())))

        for parent, child in graph.edges():
            x1, y1 = positions[parent]
            x2, y2 = positions[child]
            ax.plot([x1, x2], [y1, y2], color='black', linewidth=0.8, zorder=1)

        for node, (x, y) in positions.items():
            ax.text(x, y, node, ha='center', va='center', bbox=dict(boxstyle='round', fc='white', ec='gray'), zorder=2)

        ax.axis('off')
        return ax

    def _repr_png_(self):  # pragma: no cover
        """
        Use an image as repr if in IPython.

        Returns
        -------
        repr : bytes
            The data content of a png representation.
        """
        try:
            import matplotlib.pyplot as plt
            from io import BytesIO
        except ImportError:
            return None

        ax = self.draw()
        buffer = BytesIO()
        ax.figure.savefig(buffer, format='png', bbox_inches='tight')
        plt.close(ax.figure)
        return buffer.getvalue()
