Lattices
========

|build| |codecov| |readthedocs|

``Lattices`` is a package for the construction of lattices from a set of nodes
and an (partial) ordering relation.

Drawing
-------

Lattices optionally utilizes `nxpd` to draw a lattice. This package is somewhat
out of date at this point, and you install a modified version:

.. code-block:: bash

   pip install git+https://git@github.com/chebee7i/nxpd.git@refs/pull/15/merge#egg=nxpd


.. |build| image:: https://github.com/dit/lattices/workflows/Build/badge.svg
   :target: https://github.com/dit/lattices/actions?query=workflow%3A%22Build%22
   :alt: build status

.. |codecov| image:: https://codecov.io/gh/Autoplectic/lattices/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/Autoplectic/lattices
  :alt: test coverage

.. |readthedocs| image:: https://readthedocs.org/projects/lattices/badge/?version=latest
  :target: https://lattices.readthedocs.io/en/latest/?badge=latest
  :alt: documentation status
