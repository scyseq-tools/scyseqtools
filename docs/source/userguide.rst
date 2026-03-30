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

Editing test from Maissane

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


Launching Codix
^^^^^^^^^^^^^^

• Open the Terminal.
• In the terminal, type:

.. code-block:: bash

   ./codix

• A small window opens (**Choose working directory**):
   * Check that the displayed directory corresponds to the desired one.
   * Click **OK**.  

Creating a Code File
~~~~~~~~~~~~~~~~~~~~

• In the menu bar: **Actions → Create a new code**
..
• In **Name**, enter the name of the code file.
..
• In **Description**, enter a description of the code file.
..
• In **Code name**, enter the name of the code (example: *movement*).
..
• In **List of items**, enter the items associated with the code (example: *small*, *large*) and click **Record**.
..
• In **Recording site**, enter the name of the site (example: *mother*). 
   - Select the codes to assign to the site and click **Record**.

• Once the code file is complete, click **Save all specifications and quit**.
..
• Save the code file in the desired folder.

Starting a New Coding Session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

• In the menu bar: **Actions → Start a new session**  
..
• **Load the video:**  
   - Click **Load** in the **Media file** section.
   - In the corresponding folder, select the video to code.
..
• **Load the code file:**  
   - Click **Load** in the **Code file** section.
   - In **File type**, select **Code file (*.cod)** or **New code (*.jod)** depending on the code.
   - In the corresponding folder, select the desired code file.

Analyser guide
--------------

Launch codix analyser using the icon? or the command

.. code-block:: bash

   codix-analyser
