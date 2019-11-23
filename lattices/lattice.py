"""
"""

from itertools import combinations

import networkx as nx

from nxpd import draw


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
        things = list(things)
        try:
            if type(things[0]) is frozenset:
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

    def _validate(self):
        """
        Validate that the elements and partial order form a lattice.

        Returns
        -------
        valid : bool
            True if the partial order is a lattice, False otherwise.
        """
        raise NotImplementedError

    @property
    def distributive(self):
        """
        Determine whether the lattice is distributive or not.

        Returns
        -------
        distributed : bool
            Whether the lattice is distributive or not.
        """
        raise NotImplementedError

    @property
    def modular(self):
        """
        Determine whether the lattice is modular or not.

        Returns
        -------
        distributed : bool
            Whether the lattice is modular or not.
        """
        raise NotImplementedError

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

    def join(self, *nodes, predicate=None):
        """
        Return the join of `nodes`, that is the least element which is greater
        than all `nodes`.

        Parameters
        ----------
        nodes : {{elements}}
            The nodes to compute the join of.

        Returns
        -------
        join : {{elements}}
            The join of `nodes`.
        """
        parentss = [self.ascendants(node, include=True) for node in nodes]
        joins = [n for n in self._ts if all(n in parents for parents in parentss)]
        if predicate:
            joins = [n for n in joins if predicate(n)]
        return joins[-1]

    def meet(self, *nodes, predicate=None):
        """
        Return the meet of `nodes`, that is the greatest element which is less
        than all `nodes`.

        Parameters
        ----------
        nodes : {{elements}}
            The nodes to compute the meet of.

        Returns
        -------
        meet : {{elements}}
            The meet of `nodes`.
        """
        childrens = [self.descendants(node, include=True) for node in nodes]
        meets = [n for n in self._ts if all(n in children for children in childrens)]
        if predicate:
            print(meets)
            meets = [n for n in meets if predicate(n)]
        return meets[0]

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
        comps = {n for n in self._lattice if (self.join(n, node) == self.top)
                                         and (self.meet(n, node) == self.bottom)}
        return comps

    def join_irreducibles(self):
        """
        The join-irreducible elements of the lattice.

        Returns
        -------
        jis : {{{elements}}}
            The list of join-irreducible elements of the lattice.
        """
        jis = {n for n in self._lattice if len(self._lattice[n]) == 1}
        return jis

    def meet_irreducibles(self):
        """
        The meet-irreducible elements of the lattice.

        Returns
        -------
        mis : {{{elements}}}
            The list of meet-irreducible elements of the lattice.
        """
        reverse = self._lattice.reverse()
        mis = {n for n in reverse if len(reverse[n]) == 1}
        return mis

    def irreducibles(self):
        """
        The irreducible elements of the lattice.

        Returns
        -------
        irrs : {{{elements}}}

        """
        irrs = self.join_irreducibles() & self.meet_irreducibles()
        return irrs

    def draw(self):  # pragma: no cover
        """
        Draw a pretty version of the lattice.
        """
        edges = [(self._stringify(a), self._stringify(b)) for a, b in self._lattice.edges()]
        pretty_lattice = nx.from_edgelist(edges, nx.DiGraph)
        draw(pretty_lattice)

    def _repr_png_(self):  # pragma: no cover
        """
        Use an image as repr if in IPython.

        Returns
        -------
        repr : bytes
            The data content of a png representation.
        """
        edges = [(self._stringify(a), self._stringify(b)) for a, b in self._lattice.edges()]
        pretty_lattice = nx.from_edgelist(edges, nx.DiGraph)
        return draw(pretty_lattice, show='ipynb').data
