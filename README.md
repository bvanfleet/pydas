# Python Data Acquisition Service

A full python stack application for acquiring financial data and generating arbitrary data sets. Can be deployed as a REST API for dataset generation as a service, or run from the command line to create ad-hoc data sets for machine learning.

## Installation

Currently, the simplest method for installing is from source. This guide assumes that Python 3.7 or greater is installed with pip and virtualenv available. It is assumed and recommended that a virtual environment is created, and will be denoted in the scripts shown:

```shell
$> git clone https://github.com/UVU-PFP-Research/Personal-Financial-Planner
$> cd Personal-Financial-Planner/stock-data-acquisition
(env) $> python setup.py install
```

Once the installation has been completed, you'll want to run the installer to setup the database. The installer can be found within the sDAS package and can be run by calling:

```shell
(env) $> python -m pydas.install -h
usage: install.py [-h] [-a ALEMBIC] [-r REQUIREMENTS] [-u USERNAME]
                  [-p PASSWORD] [-d DATABASE] [--deploy-rest]

Stock Data Acquisition Service installation script for configuring the
metadata database and REST API on a server.

optional arguments:
  -h, --help            show this help message and exit
  -a ALEMBIC, --alembic ALEMBIC
                        Path to alembic configuration file (typically
                        alembic.ini)
  -r REQUIREMENTS, --requirements REQUIREMENTS
                        Path to project dependency file (typically
                        requirements.txt)
  -u USERNAME, --user USERNAME
                        Database username for opening connections
  -p PASSWORD, --password PASSWORD
                        Database password for opening connections
  -d DATABASE, --database DATABASE
                        Database name to deploy metadata database into
  --deploy-rest         Flag indicating whether the REST API server should be
                        deployed. DO NOT USE THIS OPTION! uWSGI support is not
                        currently supported and using this flag will result in
                        undefined/unsupported behavior.
```

Once the installer has been executed, the sDAS metadata database will be deployed, and (optionally) the REST API deployed.
