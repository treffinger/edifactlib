Development
===========

Setting up a dev environment
----------------------------

First, clone the repository.
After the repository has been cloned, the dependencies should be installed.
edifactlib has a dev dependency that can be installed using the following command: ``pip install -e ".[dev]"``

Code style
----------

The code is formatted with `Black <https://github.com/psf/black>`_, which uses a line length of 120 characters.
In addition, `isort <https://github.com/PyCQA/isort>`_ is used to sort the imports.
Commands for formatting:

- ``black .``
- ``isort .``

You can install the appropriate Visual Studio Code extensions to automatically format the code.

Running the tests
-----------------

The tests use the pytest library, which can be run using the command ``pytest``.

Building the docs locally
-------------------------

If you want to expand the documentation, you must install the docs dependencies.
These can be installed using the command ``pip install -e ".[docs]"``.
