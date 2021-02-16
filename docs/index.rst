.. We're skipping the header on this file because we import from the README
   which starts with a level-1 header as well. Ignore any linter warnings
   because of this decision.

sDAS Developer's Documentation
==============================

This documentation is for any developer interested in utilizing either the sDAS or metadata packages within their
applications. The information found here assumes a basic understanding of how the sDAS functions and ETL
pipelining.

sDAS is developed entirely in Python to support ease of integration with many machine
learning systems, such as those using TensorFlow. Use the following navigation to
understand how this project is organized and find additional documentation.

.. toctree::
   :maxdepth: 5
   :caption: Packages:

   metadata/index.rst
   sdas/index.rst

.. mdinclude:: ../readme.md

.. note:: This documentation was developed using the `python-docs-theme <https://github.com/python/python-docs-theme/>`_
   for sphinx. This decision comes with an element of trust, as this solution is not a part of the Python distribution,
   but a third-party package. Any issues with this system should first be troubleshooted with the interface and data
   engineering development team. If it is determined that the issue is with the core Python language, then an issue will
   be created by the development team.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
