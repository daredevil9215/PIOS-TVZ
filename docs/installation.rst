Installation
============

To install required dependencies, you can use pip:

.. code-block:: bash

   pip install -r requirements.tInstallation
============

Run the following commands to start the application:

.. code-block:: bash

  source venv/bin/activate
  pip3 install -r requirements.txt
  flask run

After installing the package, you can run the application by executing:

.. code-block:: bash

   flask run


To populate MySQL database with sample data, you can execute the following command:
.. code-block:: bash

  python3 seed.py


To reset MySQL database, you can execute the following command:
.. code-block:: bash

  python3 reset-database.py
