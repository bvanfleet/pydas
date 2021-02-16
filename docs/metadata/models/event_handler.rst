EventHandler
============

.. autoclass:: metadata.models.EventHandler
   :members:

Example
-------

This example shows how an EventHandler can be configure. The basic requirement
for this to work properly is a function that can be imported at runtime. The
following shows a sample file for printing :class:`metadata.models.Feature`
data to the console.

It is assumed that this function will be stored at the following location
``my_module/funcs.py``.

.. code-block:: python
   :linenos:
   :caption: funcs.py

   import json

   def print_feature(*args, **kwargs):
     if "feature" not in kwargs:
       raise KeyError("A feature is required!")

     feature = kwargs["feature"]
     print(json.dumps(feature.__json__()))


One an event handler function is created, it can then be tracked by an EventHandler
object. The following shows how this might be done with our ``print_feature``
function.

.. code-block:: python
   :linenos:
   :caption: handlers.py

   from metadata.contexts import DatabaseContext
   from metadata.models import EventHandler

   context = DatabaseContext("mydatabase", "myuser")
   session_maker = context.get_session_maker()
   session = session_maker()

   handler = EventHandler(name="Display Feature String",
                          description="Prints out the feature JSON representation",
                          path="my_module.funcs:print_feature",
                          type="POST_FEATURE")
   session.add(handler)
   session.commit()

.. tip:: During development, it may be important to test that an EventHandler
   is able to call the function. This can be tested at any time by either
   calling the handler itself (i.e. ``EventHandler(*args, **kwargs)``), or
   by accessing it's ``function`` property.
