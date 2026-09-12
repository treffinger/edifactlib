Quickstart
==========

Using edifactlib as a library
-----------------------------

The main class ``Parser`` allows EDIFACT Interchanges to be parsed using the ``parse`` method.
By default, the parser validates all messages.
However, this behavior can also be disabled.
The method returns an :class:`~edifactlib.Interchange` object, which can be populated with additional details by using the ``resolve`` method of the :class:`~edifactlib.InterchangeResolver` class.
These details include, for example, the official name and description of the elements.

.. code-block:: python

   from edifactlib import Parser, InterchangeResolver

   message = """
   UNA:+.? '
   UNB+UNOC:3+5412345000013:14+4012345000006:14+260704:1200+REF00001'
   UNH+1+ORDERS:D:24A:UN'
   BGM+220+PO123456+9'
   DTM+137:20260704:102'
   NAD+BY+5412345000013::9'
   NAD+SU+4012345000006::9'
   LIN+1++4712345:EN'
   QTY+21:100'
   LIN+2++4798765:EN'
   QTY+21:50'
   UNS+S'
   UNT+11+1'
   UNZ+1+REF00001'
   """

   parser = Parser()
   interchange = parser.parse(message)

   resolver = InterchangeResolver()
   resolver.resolve(interchange)


Using the CLI
-------------

After installing the package, the ``edifact`` command is also available, which can be used to display formatted EDIFACT interchanges in the terminal.

Read and inspect an EDIFACT file:

.. code-block:: bash

   edifact /path/to/message.edi



Read and inspect an EDIFACT string:

.. code-block:: bash

   edifact --from-string "UNA:+.? 'UNB+UNOC:3+...'"



Use ``--print-json`` to output the interchange as a JSON object.

.. code-block:: bash

   edifact /path/to/message.edi --print-json


Where to go next
----------------

See :doc:`cli` for the full CLI documentation or :doc:`api/index` for the API documentation.
