Exceptions
==========

Error handling
--------------
All error classes inherit from the :class:`~edifactlib.EdifactError` class.
During validation, an error can also have an instance of :class:`~edifactlib.ErrorDetails`, which indicates where in the interchange the error occurred.
This object can be accessed via the instance variable ``details``.
If ``details`` is set, printing the error also displays the interchange on the console, with the faulty part highlighted in red.

Exception classes
-----------------

.. autoclass:: edifactlib.EdifactError
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: edifactlib.ParsingError
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: edifactlib.CatalogError
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: edifactlib.InterchangeError
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: edifactlib.MessageError
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: edifactlib.SegmentError
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: edifactlib.DataElementError
   :members:
   :undoc-members:
   :show-inheritance:
