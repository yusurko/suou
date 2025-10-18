
sqlalchemy helpers
==================

.. currentmodule:: suou.sqlalchemy

SUOU provides several helpers to make sqlalchemy learning curve less steep.

In fact, there are pre-made column presets for a specific purpose.


Columns
-------

.. autofunction:: id_column

.. warning::
   ``id_column()`` expects SIQ's!

.. autofunction:: snowflake_column

.. autofunction:: match_column

.. autofunction:: secret_column

.. autofunction:: bool_column

.. autofunction:: unbound_fk
.. autofunction:: bound_fk

Column pairs
------------

.. autofunction:: age_pair
.. autofunction:: author_pair
.. autofunction:: parent_children

Misc
----

.. autofunction:: BitSelector
.. autofunction:: match_constraint
.. autofunction:: a_relationship
.. autofunction:: declarative_base
.. autofunction:: want_column