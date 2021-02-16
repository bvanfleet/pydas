"""
The stock Data Acquisition Service (sDAS) package contains the modules
necessary for performing data acquisition and dataset generation. There
are two modes of operation: CLI and REST API.

Command-Line Interface (CLI)
----------------------------
The CLI mode of operation allows for single-use acquisitions of data
utilizing a config.json file. This file must include all features,
their associate handler metadata, and company symbols to properly
acquire data and save a dataset.

REST API Server
---------------
The REST API mode of operation supports storing metadata within a
pre-configured database. This allows for multiple data acquisitions
using the same configuration by different users. This mode of
operation also supports advanced data processing and event handling.

.. note:: Additional configuration is required to support the REST API
   mode of operation, e.g. a SQLite or MySQL database needs to be
   created and initialized.
"""

__version__ = "1.0.0"
