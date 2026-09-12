Directory & Syntax
==================

The :class:`~edifactlib.Directory` and :class:`~edifactlib.Syntax` classes load the EDIFACT directory definitions and the syntax definitions for the corresponding EDIFACT version, respectively.

Both classes inherit their loading and lookup logic from :class:`~edifactlib.core.catalog.Catalog`.
This class is internal and not part of the public API.

.. autoclass:: edifactlib.Directory
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: edifactlib.Syntax
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: edifactlib.core.catalog.Catalog
   :members:
   :undoc-members:
   :show-inheritance:
