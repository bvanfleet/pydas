FeatureToggle
=============

.. autoclass:: metadata.models.FeatureToggle
   :members:

Example
-------

.. code-block:: python
   :linenos:
   :caption: This example shows a basic example of to use a feature toggle to limit code
             functionality at runtime.

   from metadata.contexts import DatabaseContext
   from metadata.models import FeatureToggle

   context = DatabaseContext()
   session_maker = context.get_session_maker()
   session = session_maker()

   toggle = session.query(FeatureToggle).filter(FeatureToggle.name=="my-toggle").one()
   
   if toggle.is_enabled:
     # Feature logic is executed here
