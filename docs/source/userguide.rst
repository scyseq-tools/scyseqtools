User's guide
============

This is the user's guide

Installation
------------

The common requirements are `Python <https://www.python.org>`_ and 
`vlc <https://www.videolan.org/vlc/>`_

Then, *when avalaible on pypi*, the installation should reduce to:

.. code-block:: bash

   pip install codix

Initialisation (TODO)
---------------------

Test de subsubsection
^^^^^^^^^^^^^^^^^^^^^

Before using the encoder or the analyser, codix configuration has to be
initialised using:

.. code-block:: bash

   codix init

asks the following questions:

- Choose codix working directory (default: USER/codix_projects or
  USER/codix_wd):

- Choose theme (default: XXX)

  The themes are provided by the ttk-themes url?

- Other configurations?

Encoder guide
-------------

Launch codix encoder using the icon? or the command

.. code-block:: bash

   codix-encoder

1. Is it a new project?

   - if "Yes":

      * Define the structure of the project (**TODO**)
      * Define the coding frame of the project (newcode)

   - if "No":

      * Get project definitions: structure (**TODO**), coding frame
      * Start a new session?

        - if "No": resume session

            * Get session name and location in the project structure?
            * Get media from the defined place
            * Get metadata
            * Get data

        - if "Yes": start new session

            * Define session location in the project structure?
            * Define media (and save media in correct place **TODO**)



Analyser guide
--------------

Editing test from Elisa

New test for other pc

Launch codix analyser using the icon? or the command

.. code-block:: bash

   codix-analyser
