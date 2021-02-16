Metadata Migrations and Database Versioning
===========================================

The `metadata.migrations` module is strictly used by the core development team
to build automated database upgrades and database versioning. This module uses
the alembic package to creation database versions that track next and previous
revisions.

.. DANGER:: This module should not be modified without in-depth knowledge of
   SQLAlchemy and Alembic. Also, modifications made are without support of 
   the interface and data engineering development team.
