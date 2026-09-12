Command Line Interface
======================

Overview
--------

The ``edifact`` command can be used to load EDIFACT interchanges and display them in the terminal.
The interchange is displayed in the terminal in a human-readable format.

Arguments and options
---------------------

By default, the ``edifact`` command takes a positional argument, which is a file to load.

``--from-string``: Allows an EDIFACT interchange to be loaded as a string.
Example ``docs/source/quickstart.rst``.

``--print-json``: Outputs the interchange as a JSON object in the terminal, instead of formatted output.

``--version``: Displays the currently installed version.

Output formats
--------------

The output is in a human-readable format.
All sections are displayed, with the header and trailer combined and formatted.
Some elements of the headers are not displayed.
The JSON output is not affected by this.
