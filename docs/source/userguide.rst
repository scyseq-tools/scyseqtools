User Guide
==========

ScySeqTools provides tools for coding behaviours from media and analysing the
resulting coded data. The public commands are ``scyseq-encoder`` and
``scyseq-analyser``.

Installation
------------

The common requirements are `Python <https://www.python.org>`_ and
`VLC <https://www.videolan.org/vlc/>`_. VLC is required by the encoder through
``python-vlc``.

Install ScySeqTools with:

.. code-block:: bash

   python -m pip install scyseqtools

For local development from a cloned repository, install the project in editable
mode instead:

.. code-block:: bash

   python -m pip install -e .

Encoder Guide
-------------

Launch the encoder from a terminal with:

.. code-block:: bash

   scyseq-encoder

The encoder opens a graphical interface and asks you to choose a working
directory. ScySeqTools expects or creates ``media`` and ``data`` folders inside
that working directory.

Project Setup
^^^^^^^^^^^^^

When starting work, decide whether you are creating a new project or continuing
an existing one.

For a new project:

* Define the project structure.
* Define the coding frame with the new-code workflow.

For an existing project:

* Load the project structure and coding frame.
* Start a new coding session or retrieve an unfinished session.

New Code
^^^^^^^^

Create a code file from **Actions > Create a new code**.

Fill in the requested fields:

* *Name*: name of the code file.
* *Description*: description of the code file.
* *Code name*: name of the code, for example ``movement``.
* *List of items*: items associated with the code, for example ``small`` and
  ``large``.
* *Recording site*: name of the site, for example ``mother``.

Record each code, item list, and recording site. When the code file is complete,
choose **Save all specifications and quit**, then save the code file in the
desired folder.

New Session
^^^^^^^^^^^

Start a new coding session from **Actions > Start a new session**.

1. Click **Load** in the *Media file* section and select the video to code.
2. Click **Load** in the *Code file* section and select the code file.
3. Use **Play/Pause** to start and stop the video.
4. Set the coding interval in *By period of (..) sec.* if interval-based coding
   is needed.
5. Click **Start processing** and enter the coder name.
6. Code the segment, click **Record**, and repeat the play, code, record cycle.

To edit previous codes, click **Back** to reach the desired segment, restart the
video if needed, correct the selected items, and click **Record**.

To exit the session, use **Actions > Quit**.

Resume Session
^^^^^^^^^^^^^^

Resume an unfinished coding session from **Actions > Retrieve a session**.

1. Click **Load** in *Data file*.
2. Select the desired coding file.
3. Click **Start processing**.
4. Enter the coder name used for the original session.

The video and coding window reopen and the session resumes from the last saved
position.

Analysis Guide
--------------

Launch the analysis interface from a terminal with:

.. code-block:: bash

   scyseq-analyser

Analysis Workflow
^^^^^^^^^^^^^^^^^

.. image:: ../images/diagramme.svg
   :align: center
   :width: 80%

+---------------------------+
| Principal steps           |
+===========================+
| 1. Organize folders       |
+---------------------------+
| 2. Choose directory       |
+---------------------------+
| 3. Select variables       |
|    or participants of     |
|    interest               |
+---------------------------+


+--------------------------+---------------------------+---------------------------------+
| Statistics               | Mutual Information        | Transition Probabilities        |
+==========================+===========================+=================================+
| Select variables         | Prepare folders carefully | Set correct time interval       |
+--------------------------+---------------------------+---------------------------------+
| Launch analysis          | Launch analysis           | Launch analysis                 |
+--------------------------+---------------------------+---------------------------------+
| Save results             | Save results              | Save results                    |
+--------------------------+---------------------------+---------------------------------+


Window Statistics
^^^^^^^^^^^^^^^^^

Use the statistics workflow to summarize coded variables.

.. note::

   Before you begin, make sure your folders are properly organized. If you have
   multiple measurement times, create one folder per time point.

Steps
"""""

1. Organize your folders.
2. Click **Choose directory** to select the folder containing your data.
3. Let ScySeqTools list the measured or coded variables.
4. Select the variables of interest.
5. Click **Launch** to run the analysis.
6. Choose the folder where results will be saved.


Window Mutual Information
^^^^^^^^^^^^^^^^^^^^^^^^^

Use mutual information to compute relationships between variables.

.. tip::

   Careful folder preparation saves time and helps prevent analysis errors.

Steps
"""""

1. Prepare your folders.
2. Click **Choose directory** to select the data folder.
3. Let ScySeqTools list the measured or coded variables.
4. Select the variables of interest.
5. Click **Launch** to start the computation.
6. Choose the folder where results will be saved.


Window Transition Probabilities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use transition probabilities to compute how often one state transitions into
another.

.. important::

   Check the time interval before calculating transition probabilities.

Steps
"""""

1. Organize your folders, with one folder per measurement time if needed.
2. Click **Choose directory** to select your data.
3. Let ScySeqTools list the measured or coded variables.
4. Select the variables of interest.
5. Set the time interval in seconds.
6. Click **Launch** to start the computation.
7. Choose the folder where results will be saved.


Practical Tips
^^^^^^^^^^^^^^

* Always verify your folder organization before running an analysis.
* Use consistent file names to make results easier to read.
* Regularly back up your original data.
