Developer Guide
===============

Database Design
---------------

**explain the database design of your project**

**include the E/R diagram(s)**

Code
----

**explain the technical structure of your code**

**to include a code listing, use the following example**::

   .. code-block:: python

      class Foo:

         def __init__(self, x):
            self.x = x

We created a domain called scores to define score. All tables are created in "INIT_STATEMENTS"

.. code-block:: sql

	 CREATE DOMAIN SCORES AS FLOAT
            DEFAULT 0.0
            CHECK((VALUE>=0.0) AND (VALUE<=10.0)); 
            
.. toctree::

   neslihan
   muruvvet
