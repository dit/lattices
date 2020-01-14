"""
A collection of potential orderings among nodes.
"""

from operator import le


__all__ = [
    'antichain_le',
    'refinement_le',
]


def antichain_le(le=le):
    """
    Construct an order based on antichain containment.

    Parameters
    ----------
    le : func
        A function representing the "less than or equal" operator.
        Defaults to <=.

    Returns
    -------
    ac_le : func
        Function implementing antichain ordering with the specified `le`.
    """
    def ac_le(alpha, beta):
        """
        a <= b --> for all b in beta, there exists an a in alpha such that a <= b.
        """
        for b in beta:
            if not any(le(a, b) for a in alpha):
                return False
        return True

    return ac_le


def refinement_le(le=le):
    """
    Construct an order based on refinement.

    Parameters
    ----------
    le : func
        A function representing the "less than or equal" operator.
        Defaults to <=.

    Returns
    -------
    r_le : func
        Function implementing refinement ordering with the specified `le`.
    """
    def r_le(alpha, beta):
        """
        a <= b --> for all a in alpha, there exists a b in beta such that a <= b.
        """
        for a in alpha:
            if not any(le(a, b) for b in beta):
                return False
        return True

    return r_le
