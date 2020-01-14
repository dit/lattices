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

    def __init__(self, nodes, relationship, symbols='•꞉⋮'):
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

        Returns
        -------
        lattice : nx.DiGraph
            The lattice representing `relationship` over `nodes`.
        """
        nodes = list(nodes)
        lattice = nx.DiGraph()
        lattice.add_nodes_from(nodes)

        self._relationship = relationship

        self._stringify = stringify(symbols=symbols)

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

    def __iter__(self):
        """
        Return an iterator over the nodes of the lattice.

        Returns
        -------
        iter : iterator
            An iterator over `self._lattice`.
        """
        return iter(self._ts)

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

        return inverse

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
        return self._lattice[node]

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

    def draw(self):  # pragma: no cover
        """
        Draw a pretty version of the lattice.
        """
        from nxpd import draw

        draw(self._pretty_lattice())

    def _repr_png_(self):  # pragma: no cover
        """
        Use an image as repr if in IPython.

        Returns
        -------
        repr : bytes
            The data content of a png representation.
        """
        from nxpd import draw

        return draw(self._pretty_lattice(), show='ipynb').data
