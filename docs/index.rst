.. We're skipping the header on this file because we import from the README
   which starts with a level-1 header as well. Ignore any linter warnings
   because of this decision.

pyDAS Developer's Documentation
===============================

This documentation is for any developer interested in utilizing either the sDAS or metadata packages within their
applications. The information found here assumes a basic understanding of how the sDAS functions and ETL
pipelining.

pyDAS is developed entirely in Python to support ease of integration with many machine
learning systems, such as those using TensorFlow. Use the following navigation to
understand how this project is organized and find additional documentation.

.. toctree::
   :maxdepth: 5
   :caption: Packages:

   metadata/index.rst
   pydas/index.rst

.. image:: ArchitectureLayerDiagram.png
   :scale: 40 %
   :align: center

.. mdinclude:: ../readme.md

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
