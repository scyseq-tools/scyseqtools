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

.. code-block:: bash

   codix-analyser

Window Statistics
=================

Analyze your data simply and efficiently.

.. note::
Before you begin, make sure your folders are properly organized.
If you have multiple measurement times, create one folder per time point.

Steps
-----

1. **Organize your folders**.  
2. Click **Choose directory** 📂 to select the folder containing your data.
3. The measured or coded variables will automatically appear in the window.
4. Select the **variables of interest** 🎯.
5. Click **Launch** ▶️ to run the analysis.
6. Choose the folder where the **results will be saved** 💾.

---

Window Mutual Information
==================

Compute relationships between your variables using mutual information.

.. Advice::
   Good folder preparation will save you time and help prevent errors.

Steps
-----

1. **Prepare your folders**.  
2. Click **Choose directory** 📂 to select the data folder.
3. The measured or coded variables will appear in the window.
4. Select the **variables of interest** 🎯.
5. Click **Launch** ▶️ to start the computation.
6. Choose the folder where the **results will be saved** 💾.

---

Window Transition Probabilities
========================

Compute the probabilities that one state transitions into another.

.. important::
Check the time interval for which you want to calculate the probabilities.

Steps
-----

1. **Organize your folders** (one folder per measurement time if needed).
2. Click **Choose directory** 📂 to select your data.
3. The measured or coded variables will appear in the window.
4. Select the **variables of interest** 🎯.
5. Set the **time interval** (in seconds) ⏱️.
6. Click **Launch** ▶️ to start the computation.
7. Choose the folder where the **results wiil be saved** 💾.

---
Analysis Workflow
=================

.. graphviz::

   digraph workflow {
       rankdir=TB;
       node [shape=box, style=rounded];

       step1 [label="Organize folders"];
       step2 [label="Choose directory"];
       step3 [label="Select variables of interest"];
       step4 [label="Set additional options"];
       step5 [label="Launch analysis"];
       step6 [label="Save results"];

       step1 -> step2 -> step3 -> step4 -> step5 -> step6;

       # Conditional notes
       note1 [shape=note, label="Statistics: just select variables"];
       note2 [shape=note, label="Mutual Information: prepare folders carefully to avoid errors"];
       note3 [shape=note, label="Transition Probabilities: set correct time interval"];

       step4 -> note1 [style=dashed, color=blue];
       step4 -> note2 [style=dashed, color=green];
       step4 -> note3 [style=dashed, color=red];
   }


Pratical Tips
------------------
- Always verify your folder organization before running an analysis.
- Use consistent file names to make results easier to read.
- Regularly back up your original data.