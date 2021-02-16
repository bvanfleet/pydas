Dataset Archive
===============

.. automodule:: sdas.archive
   :members:


IPFS
----

.. automodule:: sdas.archive.ipfs
   :members:


Example
^^^^^^^

The following shows how to upload a dataset to IPFS using the IPFS archive functions:

.. code-block:: python
   :linenos:

   from metadata.contexts import DatabaseContext
   from sdas.archive import upload_archive
   
   dataset = {
     "headers": ["a", "b", "c"]
     "rows": [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]]
     }
   
   context = DatabaseContext('my_database', 'my_user')
   connection_string = '/dns/ipfs.infura.io/tcp/5001/https'

   archive = upload_archive(dataset, connection_string, context, company_symbols='aapl')

